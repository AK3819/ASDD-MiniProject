from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Admin(UserMixin, db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    motorcycles = db.relationship("Motorcycle", backref="customer", cascade="all, delete-orphan", lazy=True)
    bookings = db.relationship("ServiceBooking", backref="customer", cascade="all, delete-orphan", lazy=True)
    invoices = db.relationship("Invoice", backref="customer", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Customer {self.name} - {self.mobile}>"


class Motorcycle(db.Model):
    __tablename__ = "motorcycles"

    MODELS = [
        "Bullet 350",
        "Classic 350",
        "Hunter 350",
        "Meteor 350",
        "Himalayan",
        "Interceptor 650",
        "Continental GT 650",
        "Other"
    ]

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    registration_number = db.Column(db.String(25), unique=True, nullable=False, index=True)
    model = db.Column(db.String(50), nullable=False)
    manufacturing_year = db.Column(db.Integer, nullable=False)
    odometer_reading = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("ServiceBooking", backref="motorcycle", cascade="all, delete-orphan", lazy=True)
    invoices = db.relationship("Invoice", backref="motorcycle", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Motorcycle {self.registration_number} ({self.model})>"


class ServiceBooking(db.Model):
    __tablename__ = "service_bookings"

    SERVICE_TYPES = [
        "General Service",
        "Oil Change",
        "Brake Service",
        "Chain Maintenance",
        "Clutch Repair",
        "Engine Repair",
        "Electrical Repair",
        "Other"
    ]

    STATUS_CHOICES = ["Pending", "In Progress", "Completed", "Cancelled"]

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey("motorcycles.id"), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    booking_date = db.Column(db.Date, nullable=False, default=date.today)
    problem_description = db.Column(db.Text, nullable=True)
    estimated_cost = db.Column(db.Float, default=0.0, nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    invoice = db.relationship("Invoice", backref="booking", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ServiceBooking #{self.id} - {self.service_type} - {self.status}>"


class SparePart(db.Model):
    __tablename__ = "spare_parts"

    CATEGORIES = [
        "Engine",
        "Brakes",
        "Transmission",
        "Electrical",
        "Body & Frame",
        "Lubricants & Fluids",
        "Filters",
        "Other"
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    minimum_stock = db.Column(db.Integer, default=5, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_stock

    def __repr__(self):
        return f"<SparePart {self.name} (Qty: {self.quantity})>"


class Invoice(db.Model):
    __tablename__ = "invoices"

    STATUS_CHOICES = ["Paid", "Unpaid"]
    PAYMENT_METHODS = ["Cash", "UPI", "Card", "Net Banking"]

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("service_bookings.id"), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey("motorcycles.id"), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False, default=date.today)
    labour_charge = db.Column(db.Float, default=0.0, nullable=False)
    parts_total = db.Column(db.Float, default=0.0, nullable=False)
    grand_total = db.Column(db.Float, default=0.0, nullable=False)
    status = db.Column(db.String(20), default="Unpaid", nullable=False)
    payment_method = db.Column(db.String(30), default="Cash", nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("InvoiceItem", backref="invoice", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Invoice {self.invoice_number} - Rs. {self.grand_total} - {self.status}>"


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    spare_part_id = db.Column(db.Integer, db.ForeignKey("spare_parts.id"), nullable=True)
    part_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    spare_part = db.relationship("SparePart")

    def __repr__(self):
        return f"<InvoiceItem {self.part_name} x {self.quantity} = Rs. {self.total_price}>"
