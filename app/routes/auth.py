from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Admin

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    has_admin = Admin.query.first() is not None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = bool(request.form.get("remember"))

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template("auth/login.html", has_admin=has_admin)

        admin = Admin.query.filter(
            (Admin.username == username) | (Admin.email == username)
        ).first()

        if admin and admin.check_password(password):
            login_user(admin, remember=remember)
            flash(f"Welcome back, {admin.username}!", "success")
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith("/"):
                next_page = url_for("dashboard.index")
            return redirect(next_page)
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template("auth/login.html", has_admin=has_admin)


@auth_bp.route("/init-admin", methods=["GET", "POST"])
def init_admin():
    """Safe initial admin setup helper if no admin exists in the database."""
    admin_count = Admin.query.count()
    if admin_count > 0:
        flash("Admin account already exists. Please login.", "info")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/init_admin.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/init_admin.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("auth/init_admin.html")

        admin = Admin(username=username, email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        flash("Initial Admin account created successfully! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/init_admin.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out safely.", "info")
    return redirect(url_for("auth.login"))
