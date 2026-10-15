import os
from app import create_app, db
from app.models import Admin, Customer, Motorcycle, ServiceBooking, SparePart, Invoice, InvoiceItem

env_mode = os.getenv("FLASK_ENV", "development")
app = create_app(env_mode)

# Ensure database tables exist
with app.app_context():
    db.create_all()
    # Ensure default admin exists for immediate demonstration
    if not Admin.query.first():
        try:
            default_admin = Admin(username="admin", email="admin@regarage.com")
            default_admin.set_password("admin123")
            db.session.add(default_admin)
            db.session.commit()
            print("[*] Created default admin account: admin / admin123")
        except Exception:
            db.session.rollback()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = env_mode == "development"
    print(f"[*] Starting RE Garage Application on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
