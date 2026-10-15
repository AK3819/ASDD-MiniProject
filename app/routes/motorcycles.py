from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models import Motorcycle, Customer, ServiceBooking

motorcycles_bp = Blueprint("motorcycles", __name__)


@motorcycles_bp.route("/")
@login_required
def index():
    search = request.args.get("q", "").strip()
    model_filter = request.args.get("model", "").strip()

    query = Motorcycle.query

    if search:
        query = query.filter(
            (Motorcycle.registration_number.ilike(f"%{search}%"))
            | (Customer.name.ilike(f"%{search}%"))
        ).join(Customer)

    if model_filter:
        query = query.filter(Motorcycle.model == model_filter)

    motorcycles = query.order_by(Motorcycle.created_at.desc()).all()
    return render_template(
        "motorcycles/index.html",
        motorcycles=motorcycles,
        search=search,
        selected_model=model_filter,
        models=Motorcycle.MODELS,
    )


@motorcycles_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    customers = Customer.query.order_by(Customer.name.asc()).all()
    preselected_customer_id = request.args.get("customer_id", type=int)

    if request.method == "POST":
        customer_id = request.form.get("customer_id", type=int)
        reg_number = request.form.get("registration_number", "").strip().upper()
        model = request.form.get("model", "").strip()
        year = request.form.get("manufacturing_year", type=int)
        odometer = request.form.get("odometer_reading", 0, type=int)

        if not customer_id or not reg_number or not model or not year:
            flash("All fields except odometer reading are required.", "danger")
            return render_template(
                "motorcycles/form.html",
                action="Add",
                motorcycle=None,
                customers=customers,
                models=Motorcycle.MODELS,
                preselected_customer_id=customer_id,
            )

        # Check unique registration number
        existing = Motorcycle.query.filter_by(registration_number=reg_number).first()
        if existing:
            flash(f"Motorcycle with Registration Number '{reg_number}' already exists.", "danger")
            return render_template(
                "motorcycles/form.html",
                action="Add",
                motorcycle=None,
                customers=customers,
                models=Motorcycle.MODELS,
                preselected_customer_id=customer_id,
            )

        customer = Customer.query.get(customer_id)
        if not customer:
            flash("Selected customer does not exist.", "danger")
            return redirect(url_for("motorcycles.add"))

        motorcycle = Motorcycle(
            customer_id=customer_id,
            registration_number=reg_number,
            model=model,
            manufacturing_year=year,
            odometer_reading=odometer if odometer else 0,
        )
        db.session.add(motorcycle)
        db.session.commit()

        flash(f"Motorcycle '{reg_number}' ({model}) added successfully!", "success")
        return redirect(url_for("motorcycles.index"))

    return render_template(
        "motorcycles/form.html",
        action="Add",
        motorcycle=None,
        customers=customers,
        models=Motorcycle.MODELS,
        preselected_customer_id=preselected_customer_id,
    )


@motorcycles_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    motorcycle = Motorcycle.query.get_or_404(id)
    customers = Customer.query.order_by(Customer.name.asc()).all()

    if request.method == "POST":
        customer_id = request.form.get("customer_id", type=int)
        reg_number = request.form.get("registration_number", "").strip().upper()
        model = request.form.get("model", "").strip()
        year = request.form.get("manufacturing_year", type=int)
        odometer = request.form.get("odometer_reading", 0, type=int)

        if not customer_id or not reg_number or not model or not year:
            flash("All fields except odometer reading are required.", "danger")
            return render_template(
                "motorcycles/form.html",
                action="Edit",
                motorcycle=motorcycle,
                customers=customers,
                models=Motorcycle.MODELS,
            )

        # Check unique registration number against others
        existing = Motorcycle.query.filter(
            Motorcycle.registration_number == reg_number,
            Motorcycle.id != motorcycle.id
        ).first()
        if existing:
            flash(f"Another motorcycle already has Registration Number '{reg_number}'.", "danger")
            return render_template(
                "motorcycles/form.html",
                action="Edit",
                motorcycle=motorcycle,
                customers=customers,
                models=Motorcycle.MODELS,
            )

        motorcycle.customer_id = customer_id
        motorcycle.registration_number = reg_number
        motorcycle.model = model
        motorcycle.manufacturing_year = year
        motorcycle.odometer_reading = odometer if odometer is not None else 0

        db.session.commit()
        flash(f"Motorcycle '{reg_number}' updated successfully!", "success")
        return redirect(url_for("motorcycles.index"))

    return render_template(
        "motorcycles/form.html",
        action="Edit",
        motorcycle=motorcycle,
        customers=customers,
        models=Motorcycle.MODELS,
    )


@motorcycles_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    motorcycle = Motorcycle.query.get_or_404(id)

    # Safe deletion check: prevent deletion if active service bookings exist
    active_bookings = ServiceBooking.query.filter(
        ServiceBooking.motorcycle_id == motorcycle.id,
        ServiceBooking.status.in_(["Pending", "In Progress"])
    ).count()

    if active_bookings > 0:
        flash(
            f"Cannot delete motorcycle '{motorcycle.registration_number}'. It has {active_bookings} active service bookings.",
            "danger"
        )
        return redirect(url_for("motorcycles.index"))

    reg_number = motorcycle.registration_number
    db.session.delete(motorcycle)
    db.session.commit()
    flash(f"Motorcycle '{reg_number}' deleted safely.", "success")
    return redirect(url_for("motorcycles.index"))


@motorcycles_bp.route("/by-customer/<int:customer_id>")
@login_required
def get_by_customer(customer_id):
    """API endpoint for dynamic cascading dropdown in booking form."""
    motorcycles = Motorcycle.query.filter_by(customer_id=customer_id).all()
    return jsonify([
        {
            "id": m.id,
            "registration_number": m.registration_number,
            "model": m.model,
            "odometer": m.odometer_reading,
        }
        for m in motorcycles
    ])
