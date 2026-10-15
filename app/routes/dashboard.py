from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from app.models import Customer, Motorcycle, ServiceBooking, SparePart, Invoice

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Real database statistics
    total_customers = Customer.query.count()
    total_motorcycles = Motorcycle.query.count()
    total_bookings = ServiceBooking.query.count()

    pending_services = ServiceBooking.query.filter_by(status="Pending").count()
    in_progress_services = ServiceBooking.query.filter_by(status="In Progress").count()
    completed_services = ServiceBooking.query.filter_by(status="Completed").count()
    cancelled_services = ServiceBooking.query.filter_by(status="Cancelled").count()

    # Revenue calculation from paid invoices
    revenue_result = (
        Invoice.query.with_entities(func.sum(Invoice.grand_total))
        .filter_by(status="Paid")
        .scalar()
    )
    total_revenue = float(revenue_result) if revenue_result else 0.0

    # Low stock items
    low_stock_parts = SparePart.query.filter(
        SparePart.quantity <= SparePart.minimum_stock
    ).all()
    low_stock_count = len(low_stock_parts)

    # Recent 6 bookings
    recent_bookings = (
        ServiceBooking.query.order_by(ServiceBooking.created_at.desc())
        .limit(6)
        .all()
    )

    # Recent 5 invoices
    recent_invoices = (
        Invoice.query.order_by(Invoice.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        total_customers=total_customers,
        total_motorcycles=total_motorcycles,
        total_bookings=total_bookings,
        pending_services=pending_services,
        in_progress_services=in_progress_services,
        completed_services=completed_services,
        cancelled_services=cancelled_services,
        total_revenue=total_revenue,
        low_stock_count=low_stock_count,
        low_stock_parts=low_stock_parts,
        recent_bookings=recent_bookings,
        recent_invoices=recent_invoices,
    )
