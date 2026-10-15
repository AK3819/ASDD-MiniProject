from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import ServiceBooking, Customer, Motorcycle

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/")
@login_required
def index():
    status_filter = request.args.get("status", "").strip()
    search = request.args.get("q", "").strip()

    query = ServiceBooking.query

    if status_filter and status_filter in ServiceBooking.STATUS_CHOICES:
        query = query.filter(ServiceBooking.status == status_filter)

    if search:
        query = query.join(Customer).join(Motorcycle).filter(
            (Customer.name.ilike(f"%{search}%"))
            | (Motorcycle.registration_number.ilike(f"%{search}%"))
            | (ServiceBooking.service_type.ilike(f"%{search}%"))
        )

    bookings = query.order_by(ServiceBooking.booking_date.desc(), ServiceBooking.id.desc()).all()

    # Counts for status badges
    status_counts = {
        "All": ServiceBooking.query.count(),
        "Pending": ServiceBooking.query.filter_by(status="Pending").count(),
        "In Progress": ServiceBooking.query.filter_by(status="In Progress").count(),
        "Completed": ServiceBooking.query.filter_by(status="Completed").count(),
        "Cancelled": ServiceBooking.query.filter_by(status="Cancelled").count(),
    }

    return render_template(
        "bookings/index.html",
        bookings=bookings,
        selected_status=status_filter,
        search=search,
        status_counts=status_counts,
    )


@bookings_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    customers = Customer.query.order_by(Customer.name.asc()).all()
    motorcycles = Motorcycle.query.order_by(Motorcycle.registration_number.asc()).all()

    preselected_customer_id = request.args.get("customer_id", type=int)
    preselected_motorcycle_id = request.args.get("motorcycle_id", type=int)

    if request.method == "POST":
        customer_id = request.form.get("customer_id", type=int)
        motorcycle_id = request.form.get("motorcycle_id", type=int)
        service_type = request.form.get("service_type", "").strip()
        booking_date_str = request.form.get("booking_date", "").strip()
        problem_description = request.form.get("problem_description", "").strip()
        estimated_cost = request.form.get("estimated_cost", 0.0, type=float)
        status = request.form.get("status", "Pending").strip()

        if not customer_id or not motorcycle_id or not service_type or not booking_date_str:
            flash("Customer, Motorcycle, Service Type, and Booking Date are required.", "danger")
            return render_template(
                "bookings/form.html",
                action="Create",
                booking=None,
                customers=customers,
                motorcycles=motorcycles,
                service_types=ServiceBooking.SERVICE_TYPES,
                status_choices=ServiceBooking.STATUS_CHOICES,
                preselected_customer_id=customer_id,
                preselected_motorcycle_id=motorcycle_id,
            )

        # Validate motorcycle belongs to customer
        bike = Motorcycle.query.get(motorcycle_id)
        if not bike or bike.customer_id != customer_id:
            flash("Selected motorcycle does not belong to the selected customer.", "danger")
            return render_template(
                "bookings/form.html",
                action="Create",
                booking=None,
                customers=customers,
                motorcycles=motorcycles,
                service_types=ServiceBooking.SERVICE_TYPES,
                status_choices=ServiceBooking.STATUS_CHOICES,
                preselected_customer_id=customer_id,
                preselected_motorcycle_id=motorcycle_id,
            )

        try:
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
        except ValueError:
            booking_date = date.today()

        booking = ServiceBooking(
            customer_id=customer_id,
            motorcycle_id=motorcycle_id,
            service_type=service_type,
            booking_date=booking_date,
            problem_description=problem_description if problem_description else None,
            estimated_cost=estimated_cost if estimated_cost else 0.0,
            status=status if status in ServiceBooking.STATUS_CHOICES else "Pending",
        )
        db.session.add(booking)
        db.session.commit()

        flash(f"Service Booking #{booking.id} created successfully!", "success")
        return redirect(url_for("bookings.index"))

    return render_template(
        "bookings/form.html",
        action="Create",
        booking=None,
        customers=customers,
        motorcycles=motorcycles,
        service_types=ServiceBooking.SERVICE_TYPES,
        status_choices=ServiceBooking.STATUS_CHOICES,
        preselected_customer_id=preselected_customer_id,
        preselected_motorcycle_id=preselected_motorcycle_id,
    )


@bookings_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    booking = ServiceBooking.query.get_or_404(id)
    customers = Customer.query.order_by(Customer.name.asc()).all()
    motorcycles = Motorcycle.query.filter_by(customer_id=booking.customer_id).all()

    if request.method == "POST":
        service_type = request.form.get("service_type", "").strip()
        booking_date_str = request.form.get("booking_date", "").strip()
        problem_description = request.form.get("problem_description", "").strip()
        estimated_cost = request.form.get("estimated_cost", 0.0, type=float)
        status = request.form.get("status", booking.status).strip()

        if not service_type or not booking_date_str:
            flash("Service Type and Booking Date are required.", "danger")
            return render_template(
                "bookings/form.html",
                action="Edit",
                booking=booking,
                customers=customers,
                motorcycles=motorcycles,
                service_types=ServiceBooking.SERVICE_TYPES,
                status_choices=ServiceBooking.STATUS_CHOICES,
            )

        try:
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
        except ValueError:
            booking_date = booking.booking_date

        booking.service_type = service_type
        booking.booking_date = booking_date
        booking.problem_description = problem_description if problem_description else None
        booking.estimated_cost = estimated_cost if estimated_cost is not None else 0.0
        booking.status = status if status in ServiceBooking.STATUS_CHOICES else booking.status

        db.session.commit()
        flash(f"Service Booking #{booking.id} updated successfully!", "success")
        return redirect(url_for("bookings.index"))

    return render_template(
        "bookings/form.html",
        action="Edit",
        booking=booking,
        customers=customers,
        motorcycles=motorcycles,
        service_types=ServiceBooking.SERVICE_TYPES,
        status_choices=ServiceBooking.STATUS_CHOICES,
    )


@bookings_bp.route("/<int:id>/update-status", methods=["POST"])
@login_required
def update_status(id):
    booking = ServiceBooking.query.get_or_404(id)
    new_status = request.form.get("status", "").strip()

    if new_status in ServiceBooking.STATUS_CHOICES:
        booking.status = new_status
        db.session.commit()
        flash(f"Booking #{booking.id} status changed to '{new_status}'.", "info")
    else:
        flash("Invalid status selected.", "danger")

    return redirect(request.referrer or url_for("bookings.index"))


@bookings_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    booking = ServiceBooking.query.get_or_404(id)

    # Safe deletion check: prevent deletion if invoice already exists
    if booking.invoice:
        flash(
            f"Cannot delete booking #{booking.id}. It has an associated invoice ({booking.invoice.invoice_number}).",
            "danger"
        )
        return redirect(url_for("bookings.index"))

    booking_id = booking.id
    db.session.delete(booking)
    db.session.commit()
    flash(f"Service Booking #{booking_id} deleted successfully.", "success")
    return redirect(url_for("bookings.index"))
