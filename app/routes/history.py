from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import ServiceBooking, Customer, Motorcycle

history_bp = Blueprint("history", __name__)


@history_bp.route("/")
@login_required
def index():
    search = request.args.get("q", "").strip()

    # Base query for completed services
    query = ServiceBooking.query.filter(ServiceBooking.status == "Completed")

    if search:
        query = query.join(Customer).join(Motorcycle).filter(
            (Motorcycle.registration_number.ilike(f"%{search}%"))
            | (Customer.name.ilike(f"%{search}%"))
            | (Customer.mobile.ilike(f"%{search}%"))
            | (Motorcycle.model.ilike(f"%{search}%"))
        )

    # Order newest service first
    completed_bookings = query.order_by(
        ServiceBooking.booking_date.desc(),
        ServiceBooking.id.desc()
    ).all()

    # Total completed services count
    total_completed = ServiceBooking.query.filter_by(status="Completed").count()

    return render_template(
        "history/index.html",
        bookings=completed_bookings,
        search=search,
        total_completed=total_completed,
    )
