from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Invoice, InvoiceItem, ServiceBooking, SparePart, Customer, Motorcycle

billing_bp = Blueprint("billing", __name__)


def generate_invoice_number():
    year = datetime.now().year
    count = Invoice.query.count() + 1
    return f"RE-{year}-{count:04d}"


@billing_bp.route("/")
@login_required
def index():
    status_filter = request.args.get("status", "").strip()
    search = request.args.get("q", "").strip()

    query = Invoice.query

    if status_filter and status_filter in Invoice.STATUS_CHOICES:
        query = query.filter(Invoice.status == status_filter)

    if search:
        query = query.join(Customer).join(Motorcycle).filter(
            (Invoice.invoice_number.ilike(f"%{search}%"))
            | (Customer.name.ilike(f"%{search}%"))
            | (Motorcycle.registration_number.ilike(f"%{search}%"))
        )

    invoices = query.order_by(Invoice.invoice_date.desc(), Invoice.id.desc()).all()

    # Calculate summary metrics
    total_invoices_count = Invoice.query.count()
    paid_count = Invoice.query.filter_by(status="Paid").count()
    unpaid_count = Invoice.query.filter_by(status="Unpaid").count()

    total_billed = sum(i.grand_total for i in invoices)

    return render_template(
        "billing/index.html",
        invoices=invoices,
        selected_status=status_filter,
        search=search,
        total_invoices_count=total_invoices_count,
        paid_count=paid_count,
        unpaid_count=unpaid_count,
        total_billed=total_billed,
    )


@billing_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # Only service bookings that do NOT yet have an invoice
    eligible_bookings = (
        ServiceBooking.query.filter(
            ~ServiceBooking.id.in_(db.session.query(Invoice.booking_id))
        )
        .order_by(ServiceBooking.booking_date.desc())
        .all()
    )
    spare_parts = SparePart.query.order_by(SparePart.name.asc()).all()

    preselected_booking_id = request.args.get("booking_id", type=int)

    if request.method == "POST":
        booking_id = request.form.get("booking_id", type=int)
        labour_charge = request.form.get("labour_charge", 0.0, type=float)
        payment_method = request.form.get("payment_method", "Cash").strip()
        status = request.form.get("status", "Unpaid").strip()
        notes = request.form.get("notes", "").strip()

        if not booking_id:
            flash("Please select a valid service booking.", "danger")
            return render_template(
                "billing/form.html",
                eligible_bookings=eligible_bookings,
                spare_parts=spare_parts,
                preselected_booking_id=preselected_booking_id,
                payment_methods=Invoice.PAYMENT_METHODS,
                status_choices=Invoice.STATUS_CHOICES,
            )

        # Check duplicate invoice for the same booking
        existing_invoice = Invoice.query.filter_by(booking_id=booking_id).first()
        if existing_invoice:
            flash(f"Invoice already exists for Booking #{booking_id}: {existing_invoice.invoice_number}", "danger")
            return redirect(url_for("billing.view", id=existing_invoice.id))

        booking = ServiceBooking.query.get(booking_id)
        if not booking:
            flash("Selected booking does not exist.", "danger")
            return redirect(url_for("billing.create"))

        # Process selected spare parts from form
        # Form inputs: part_ids[], quantities[]
        part_ids = request.form.getlist("part_id[]")
        quantities = request.form.getlist("quantity[]")

        parts_total = 0.0
        invoice_items = []

        # Validate parts and stock availability
        for pid_str, qty_str in zip(part_ids, quantities):
            if not pid_str:
                continue
            try:
                pid = int(pid_str)
                qty = int(qty_str)
            except ValueError:
                continue

            if qty <= 0:
                continue

            part = SparePart.query.get(pid)
            if not part:
                flash(f"Invalid spare part selected (ID {pid}).", "danger")
                return render_template(
                    "billing/form.html",
                    eligible_bookings=eligible_bookings,
                    spare_parts=spare_parts,
                    preselected_booking_id=booking_id,
                    payment_methods=Invoice.PAYMENT_METHODS,
                    status_choices=Invoice.STATUS_CHOICES,
                )

            if part.quantity < qty:
                flash(
                    f"Insufficient stock for '{part.name}'. Available: {part.quantity}, Requested: {qty}.",
                    "danger"
                )
                return render_template(
                    "billing/form.html",
                    eligible_bookings=eligible_bookings,
                    spare_parts=spare_parts,
                    preselected_booking_id=booking_id,
                    payment_methods=Invoice.PAYMENT_METHODS,
                    status_choices=Invoice.STATUS_CHOICES,
                )

            line_total = round(qty * part.unit_price, 2)
            parts_total += line_total

            invoice_items.append({
                "part": part,
                "part_name": part.name,
                "quantity": qty,
                "unit_price": part.unit_price,
                "total_price": line_total,
            })

        labour_charge = max(0.0, labour_charge if labour_charge is not None else 0.0)
        grand_total = round(labour_charge + parts_total, 2)

        invoice_number = generate_invoice_number()

        invoice = Invoice(
            invoice_number=invoice_number,
            booking_id=booking.id,
            customer_id=booking.customer_id,
            motorcycle_id=booking.motorcycle_id,
            invoice_date=date.today(),
            labour_charge=labour_charge,
            parts_total=parts_total,
            grand_total=grand_total,
            status=status if status in Invoice.STATUS_CHOICES else "Unpaid",
            payment_method=payment_method if payment_method in Invoice.PAYMENT_METHODS else "Cash",
            notes=notes if notes else None,
        )
        db.session.add(invoice)
        db.session.flush()  # generates invoice.id

        # Deduct inventory safely and create invoice items
        for item_data in invoice_items:
            part = item_data["part"]
            part.quantity -= item_data["quantity"]  # deduct inventory

            item = InvoiceItem(
                invoice_id=invoice.id,
                spare_part_id=part.id,
                part_name=item_data["part_name"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["total_price"],
            )
            db.session.add(item)

        # Automatically mark service booking as completed if not already
        if booking.status != "Completed":
            booking.status = "Completed"

        db.session.commit()

        flash(f"Invoice {invoice.invoice_number} created successfully!", "success")
        return redirect(url_for("billing.view", id=invoice.id))

    return render_template(
        "billing/form.html",
        eligible_bookings=eligible_bookings,
        spare_parts=spare_parts,
        preselected_booking_id=preselected_booking_id,
        payment_methods=Invoice.PAYMENT_METHODS,
        status_choices=Invoice.STATUS_CHOICES,
    )


@billing_bp.route("/<int:id>")
@login_required
def view(id):
    invoice = Invoice.query.get_or_404(id)
    return render_template("billing/view.html", invoice=invoice)


@billing_bp.route("/<int:id>/toggle-status", methods=["POST"])
@login_required
def toggle_status(id):
    invoice = Invoice.query.get_or_404(id)
    new_status = request.form.get("status")

    if new_status in Invoice.STATUS_CHOICES:
        invoice.status = new_status
        db.session.commit()
        flash(f"Invoice {invoice.invoice_number} marked as {new_status}.", "success")
    else:
        flash("Invalid status.", "danger")

    return redirect(url_for("billing.view", id=invoice.id))
