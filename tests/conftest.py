"""Pytest configuration and fixtures for RE Garage application test suite.

This module sets up:
- 'app' fixture: in-memory SQLite Flask application configured with 'testing' config
- 'client' fixture: Flask test client
- 'init_db' fixture: database seeded with baseline admin, customer, motorcycle, spare part, and booking
- 'login' helper function: programmatic staff authentication helper
"""

from datetime import date
import pytest
from app import create_app, db
from app.models import Admin, Customer, Motorcycle, ServiceBooking, SparePart, Invoice, InvoiceItem


def login(client, username="testadmin", password="password123", follow_redirects=True):
    """Helper function to log in an admin user via POST to /login.

    Args:
        client: Flask test client instance
        username (str): Username or email of the admin account
        password (str): Plain-text password
        follow_redirects (bool): Whether test client should follow 302 redirect

    Returns:
        TestResponse: Response from the POST request
    """
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=follow_redirects,
    )


@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for each test.

    Uses the 'testing' configuration which configures an in-memory SQLite database
    and disables CSRF token enforcement for predictable testing.
    """
    app_instance = create_app("testing")
    ctx = app_instance.app_context()
    ctx.push()
    db.create_all()

    yield app_instance

    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app):
    """Provide a test client for simulating HTTP requests against the app."""
    return app.test_client()


@pytest.fixture
def init_db(app):
    """Seed test database with essential initial data.

    Returns a dictionary containing references to all seeded model instances:
    - admin: 'testadmin' / 'password123'
    - customer: 'John Doe'
    - motorcycle: 'MH02AB1234' (Classic 350)
    - spare_part: 'Engine Oil 15W50 (1L)' (Qty: 20, Min: 5)
    - booking: General Service (Pending)
    """
    # 1. Admin user
    admin = Admin(username="testadmin", email="admin@regarage.com")
    admin.set_password("password123")
    db.session.add(admin)

    # 2. Customer
    customer = Customer(
        name="John Doe",
        mobile="9876543210",
        email="john@example.com",
        address="123 Royal Enfield Lane, Mumbai",
    )
    db.session.add(customer)
    db.session.flush()

    # 3. Motorcycle linked to Customer
    motorcycle = Motorcycle(
        customer_id=customer.id,
        registration_number="MH02AB1234",
        model="Classic 350",
        manufacturing_year=2021,
        odometer_reading=12500,
    )
    db.session.add(motorcycle)
    db.session.flush()

    # 4. Spare Part
    spare_part = SparePart(
        name="Engine Oil 15W50 (1L)",
        category="Lubricants & Fluids",
        quantity=20,
        unit_price=450.0,
        minimum_stock=5,
    )
    db.session.add(spare_part)
    db.session.flush()

    # 5. Service Booking
    booking = ServiceBooking(
        customer_id=customer.id,
        motorcycle_id=motorcycle.id,
        service_type="General Service",
        booking_date=date.today(),
        problem_description="Periodic general servicing and oil change",
        estimated_cost=1500.0,
        status="Pending",
    )
    db.session.add(booking)
    db.session.commit()

    return {
        "admin": admin,
        "customer": customer,
        "motorcycle": motorcycle,
        "spare_part": spare_part,
        "booking": booking,
    }
