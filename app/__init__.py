from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_by_name

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access RE Garage portal."
    login_manager.login_message_category = "warning"

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.customers import customers_bp
    from app.routes.motorcycles import motorcycles_bp
    from app.routes.bookings import bookings_bp
    from app.routes.inventory import inventory_bp
    from app.routes.billing import billing_bp
    from app.routes.history import history_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(motorcycles_bp, url_prefix="/motorcycles")
    app.register_blueprint(bookings_bp, url_prefix="/bookings")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(billing_bp, url_prefix="/billing")
    app.register_blueprint(history_bp, url_prefix="/history")

    @app.context_processor
    def inject_global_data():
        from app.models import SparePart, ServiceBooking
        try:
            low_stock_count = SparePart.query.filter(SparePart.quantity <= SparePart.minimum_stock).count()
            pending_count = ServiceBooking.query.filter_by(status="Pending").count()
        except Exception:
            low_stock_count = 0
            pending_count = 0
        return {
            "app_title": "RE Garage",
            "app_tagline": "Royal Enfield Specialist Workshop",
            "global_low_stock_count": low_stock_count,
            "global_pending_count": pending_count,
        }

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app
