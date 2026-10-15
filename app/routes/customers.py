from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Customer, ServiceBooking

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/")
@login_required
def index():
    search = request.args.get("q", "").strip()
    query = Customer.query

    if search:
        query = query.filter(
            (Customer.name.ilike(f"%{search}%"))
            | (Customer.mobile.ilike(f"%{search}%"))
            | (Customer.email.ilike(f"%{search}%"))
        )

    customers = query.order_by(Customer.created_at.desc()).all()
    return render_template("customers/index.html", customers=customers, search=search)


@customers_bp.route("/add", methods=["GET", "POST"])
@customers_bp.route("/create", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not mobile:
            flash("Customer Name and Mobile Number are required.", "danger")
            return render_template("customers/form.html", action="Add", customer=None)

        if len(mobile) < 10:
            flash("Please enter a valid mobile number (at least 10 digits).", "danger")
            return render_template("customers/form.html", action="Add", customer=None)

        customer = Customer(
            name=name,
            mobile=mobile,
            email=email if email else None,
            address=address if address else None,
        )
        db.session.add(customer)
        db.session.commit()
        flash(f"Customer '{name}' added successfully!", "success")
        return redirect(url_for("customers.index"))

    return render_template("customers/form.html", action="Add", customer=None)


@customers_bp.route("/<int:id>")
@login_required
def detail(id):
    customer = Customer.query.get_or_404(id)
    return render_template("customers/detail.html", customer=customer)


@customers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()

        if not name or not mobile:
            flash("Customer Name and Mobile Number are required.", "danger")
            return render_template("customers/form.html", action="Edit", customer=customer)

        customer.name = name
        customer.mobile = mobile
        customer.email = email if email else None
        customer.address = address if address else None

        db.session.commit()
        flash(f"Customer '{name}' updated successfully!", "success")
        return redirect(url_for("customers.detail", id=customer.id))

    return render_template("customers/form.html", action="Edit", customer=customer)


@customers_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    customer = Customer.query.get_or_404(id)

    # Safe deletion check: prevent deletion if customer has active service bookings (Pending / In Progress)
    active_bookings = ServiceBooking.query.filter(
        ServiceBooking.customer_id == customer.id,
        ServiceBooking.status.in_(["Pending", "In Progress"])
    ).count()

    if active_bookings > 0:
        flash(
            f"Cannot delete customer '{customer.name}'. There are {active_bookings} active (Pending/In-Progress) service bookings.",
            "danger"
        )
        return redirect(url_for("customers.index"))

    customer_name = customer.name
    db.session.delete(customer)
    db.session.commit()
    flash(f"Customer '{customer_name}' and associated records deleted safely.", "success")
    return redirect(url_for("customers.index"))
