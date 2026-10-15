from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app import db
from app.models import SparePart, InvoiceItem

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
@login_required
def index():
    search = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "").strip()
    low_stock_only = request.args.get("low_stock") == "1"

    query = SparePart.query

    if search:
        query = query.filter(SparePart.name.ilike(f"%{search}%"))

    if category_filter:
        query = query.filter(SparePart.category == category_filter)

    if low_stock_only:
        query = query.filter(SparePart.quantity <= SparePart.minimum_stock)

    parts = query.order_by(SparePart.name.asc()).all()

    total_parts_count = SparePart.query.count()
    low_stock_count = SparePart.query.filter(SparePart.quantity <= SparePart.minimum_stock).count()

    return render_template(
        "inventory/index.html",
        parts=parts,
        search=search,
        selected_category=category_filter,
        low_stock_only=low_stock_only,
        categories=SparePart.CATEGORIES,
        total_parts_count=total_parts_count,
        low_stock_count=low_stock_count,
    )


@inventory_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        quantity = request.form.get("quantity", 0, type=int)
        unit_price = request.form.get("unit_price", 0.0, type=float)
        min_stock = request.form.get("minimum_stock", 5, type=int)

        if not name or not category or unit_price is None:
            flash("Part Name, Category, and Unit Price are required.", "danger")
            return render_template(
                "inventory/form.html",
                action="Add",
                part=None,
                categories=SparePart.CATEGORIES,
            )

        if quantity < 0 or unit_price < 0 or min_stock < 0:
            flash("Quantities and prices cannot be negative.", "danger")
            return render_template(
                "inventory/form.html",
                action="Add",
                part=None,
                categories=SparePart.CATEGORIES,
            )

        existing = SparePart.query.filter(SparePart.name.ilike(name)).first()
        if existing:
            flash(f"Spare part '{name}' already exists in inventory.", "danger")
            return render_template(
                "inventory/form.html",
                action="Add",
                part=None,
                categories=SparePart.CATEGORIES,
            )

        part = SparePart(
            name=name,
            category=category,
            quantity=quantity,
            unit_price=unit_price,
            minimum_stock=min_stock,
        )
        db.session.add(part)
        db.session.commit()

        flash(f"Spare Part '{name}' added successfully!", "success")
        return redirect(url_for("inventory.index"))

    return render_template(
        "inventory/form.html",
        action="Add",
        part=None,
        categories=SparePart.CATEGORIES,
    )


@inventory_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    part = SparePart.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        quantity = request.form.get("quantity", 0, type=int)
        unit_price = request.form.get("unit_price", 0.0, type=float)
        min_stock = request.form.get("minimum_stock", 5, type=int)

        if not name or not category or unit_price is None:
            flash("Part Name, Category, and Unit Price are required.", "danger")
            return render_template(
                "inventory/form.html",
                action="Edit",
                part=part,
                categories=SparePart.CATEGORIES,
            )

        if quantity < 0 or unit_price < 0 or min_stock < 0:
            flash("Quantities and prices cannot be negative.", "danger")
            return render_template(
                "inventory/form.html",
                action="Edit",
                part=part,
                categories=SparePart.CATEGORIES,
            )

        existing = SparePart.query.filter(
            SparePart.name.ilike(name),
            SparePart.id != part.id
        ).first()
        if existing:
            flash(f"Another part named '{name}' already exists.", "danger")
            return render_template(
                "inventory/form.html",
                action="Edit",
                part=part,
                categories=SparePart.CATEGORIES,
            )

        part.name = name
        part.category = category
        part.quantity = quantity
        part.unit_price = unit_price
        part.minimum_stock = min_stock

        db.session.commit()
        flash(f"Spare Part '{name}' updated successfully!", "success")
        return redirect(url_for("inventory.index"))

    return render_template(
        "inventory/form.html",
        action="Edit",
        part=part,
        categories=SparePart.CATEGORIES,
    )


@inventory_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    part = SparePart.query.get_or_404(id)

    # Safe deletion check: prevent deletion if part has been used in past invoices
    usage_count = InvoiceItem.query.filter_by(spare_part_id=part.id).count()
    if usage_count > 0:
        flash(
            f"Cannot delete part '{part.name}'. It is linked to {usage_count} past invoice item(s). Consider setting quantity to 0 instead.",
            "danger"
        )
        return redirect(url_for("inventory.index"))

    part_name = part.name
    db.session.delete(part)
    db.session.commit()
    flash(f"Spare Part '{part_name}' deleted safely.", "success")
    return redirect(url_for("inventory.index"))


@inventory_bp.route("/api/list")
@login_required
def api_list():
    """API endpoint returning available spare parts for dynamic billing form."""
    parts = SparePart.query.order_by(SparePart.name.asc()).all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "quantity": p.quantity,
            "unit_price": p.unit_price,
            "is_low_stock": p.is_low_stock,
        }
        for p in parts
    ])
