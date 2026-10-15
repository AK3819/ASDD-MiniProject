"""Comprehensive pytest test suite for RE Garage application.

Tests cover:
- Authentication (login, invalid credentials, logout, route protection)
- Dashboard metrics and summary statistics
- Customer management (add, edit, search)
- Motorcycle fleet registration and uniqueness constraints
- Service booking lifecycle (creation, status updates)
- Inventory management (catalog addition, low-stock threshold detection)
- Billing and invoices (calculation, inventory deduction, duplicate prevention)
"""

from datetime import date
import pytest
from app import db
from app.models import Admin, Customer, Motorcycle, ServiceBooking, SparePart, Invoice, InvoiceItem

try:
    from tests.conftest import login
except ImportError:
    from conftest import login


def test_login_page_loads(client):
    """Verify that the login page loads with HTTP 200 and required form elements."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"RE GARAGE" in response.data
    assert b"Sign In" in response.data
    assert b"username" in response.data
    assert b"password" in response.data


def test_login_valid_credentials(client, init_db):
    """Verify successful login redirects to dashboard and flashes welcome message."""
    # 1. Check HTTP 302 redirect
    response = client.post(
        "/login",
        data={"username": "testadmin", "password": "password123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith(("/dashboard", "/"))

    # 2. Check redirected dashboard view with flash message
    followed = client.post(
        "/login",
        data={"username": "testadmin", "password": "password123"},
        follow_redirects=True,
    )
    assert followed.status_code == 200
    assert b"Welcome back, testadmin!" in followed.data


def test_login_invalid_credentials(client, init_db):
    """Verify login failure with incorrect password and non-existent username."""
    # Incorrect password
    response = client.post(
        "/login",
        data={"username": "testadmin", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data

    # Non-existent username
    resp_unknown = client.post(
        "/login",
        data={"username": "nonexistent_user", "password": "password123"},
        follow_redirects=True,
    )
    assert resp_unknown.status_code == 200
    assert b"Invalid username or password. Please try again." in resp_unknown.data


def test_dashboard_requires_login(client):
    """Verify unauthenticated access to /dashboard is redirected to login."""
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    followed = client.get("/dashboard", follow_redirects=True)
    assert followed.status_code == 200
    assert b"Please sign in to access RE Garage portal." in followed.data


def test_dashboard_loads_with_stats(client, init_db):
    """Verify dashboard renders correct statistics from the seeded database."""
    login(client, "testadmin", "password123")
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Workshop Dashboard" in response.data
    assert b"Total Customers" in response.data
    assert b"Total Motorcycles" in response.data
    assert b"Total Bookings" in response.data
    assert b"Pending Services" in response.data

    # Verify actual database state
    assert Customer.query.count() == 1
    assert Motorcycle.query.count() == 1
    assert ServiceBooking.query.count() == 1
    assert SparePart.query.count() == 1
    assert ServiceBooking.query.filter_by(status="Pending").count() == 1


def test_add_customer(client, init_db):
    """Verify adding a new customer via POST creates a database record and redirects."""
    login(client, "testadmin", "password123")

    customer_payload = {
        "name": "Karan Mehra",
        "mobile": "9823456789",
        "email": "karan.mehra@example.com",
        "address": "45 MG Road, Camp, Pune",
    }

    response = client.post("/customers/add", data=customer_payload, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith(("/customers", "/customers/"))

    # Verify database persistence
    saved_customer = Customer.query.filter_by(mobile="9823456789").first()
    assert saved_customer is not None
    assert saved_customer.name == "Karan Mehra"
    assert saved_customer.email == "karan.mehra@example.com"
    assert saved_customer.address == "45 MG Road, Camp, Pune"


def test_edit_customer(client, init_db):
    """Verify updating existing customer details modifies the database record."""
    login(client, "testadmin", "password123")
    customer = init_db["customer"]

    update_payload = {
        "name": "John Doe Updated",
        "mobile": "9876500000",
        "email": "john.updated@example.com",
        "address": "999 Marine Drive, Mumbai",
    }

    response = client.post(
        f"/customers/{customer.id}/edit",
        data=update_payload,
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/customers/{customer.id}")

    # Verify updated values in database
    db.session.refresh(customer)
    assert customer.name == "John Doe Updated"
    assert customer.mobile == "9876500000"
    assert customer.email == "john.updated@example.com"
    assert customer.address == "999 Marine Drive, Mumbai"


def test_search_customers(client, init_db):
    """Verify customer search query filter by name and mobile number."""
    login(client, "testadmin", "password123")

    # Add a second customer
    second_customer = Customer(
        name="Aman Verma",
        mobile="9811122233",
        email="aman.verma@example.com",
        address="Connaught Place, New Delhi",
    )
    db.session.add(second_customer)
    db.session.commit()

    # Search by name "Aman"
    resp_name = client.get("/customers/?q=Aman")
    assert resp_name.status_code == 200
    assert b"Aman Verma" in resp_name.data
    assert b"John Doe" not in resp_name.data

    # Search by mobile number "9876543210"
    resp_mobile = client.get("/customers/?q=9876543210")
    assert resp_mobile.status_code == 200
    assert b"John Doe" in resp_mobile.data
    assert b"Aman Verma" not in resp_mobile.data


def test_add_motorcycle(client, init_db):
    """Verify registering a new motorcycle linked to an existing customer."""
    login(client, "testadmin", "password123")
    customer_id = init_db["customer"].id

    bike_payload = {
        "customer_id": customer_id,
        "registration_number": "KA05CD5678",
        "model": "Meteor 350",
        "manufacturing_year": 2022,
        "odometer_reading": 8500,
    }

    response = client.post("/motorcycles/add", data=bike_payload, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith(("/motorcycles", "/motorcycles/"))

    # Verify motorcycle in database
    bike = Motorcycle.query.filter_by(registration_number="KA05CD5678").first()
    assert bike is not None
    assert bike.customer_id == customer_id
    assert bike.model == "Meteor 350"
    assert bike.manufacturing_year == 2022
    assert bike.odometer_reading == 8500


def test_unique_registration_number(client, init_db):
    """Verify attempting to add duplicate motorcycle registration number is rejected."""
    login(client, "testadmin", "password123")
    customer_id = init_db["customer"].id
    existing_reg = init_db["motorcycle"].registration_number

    duplicate_payload = {
        "customer_id": customer_id,
        "registration_number": existing_reg,
        "model": "Bullet 350",
        "manufacturing_year": 2020,
        "odometer_reading": 3000,
    }

    response = client.post("/motorcycles/add", data=duplicate_payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"already exists" in response.data

    # Database still contains exactly 1 motorcycle with this registration number
    assert Motorcycle.query.filter_by(registration_number=existing_reg).count() == 1


def test_create_booking(client, init_db):
    """Verify service booking creation persists to database and links to customer & motorcycle."""
    login(client, "testadmin", "password123")
    customer_id = init_db["customer"].id
    motorcycle_id = init_db["motorcycle"].id

    booking_payload = {
        "customer_id": customer_id,
        "motorcycle_id": motorcycle_id,
        "service_type": "Brake Service",
        "booking_date": "2026-11-01",
        "problem_description": "Rear drum brake needs adjustment and pad replacement",
        "estimated_cost": 850.0,
        "status": "Pending",
    }

    response = client.post("/bookings/create", data=booking_payload, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith(("/bookings", "/bookings/"))

    # Verify booking in database
    booking = ServiceBooking.query.filter_by(
        service_type="Brake Service",
        customer_id=customer_id,
    ).first()
    assert booking is not None
    assert booking.motorcycle_id == motorcycle_id
    assert booking.problem_description == "Rear drum brake needs adjustment and pad replacement"
    assert booking.estimated_cost == 850.0
    assert booking.status == "Pending"


def test_update_booking_status(client, init_db):
    """Verify changing service booking status via POST update-status route."""
    login(client, "testadmin", "password123")
    booking = init_db["booking"]
    assert booking.status == "Pending"

    # Transition to 'In Progress'
    response = client.post(
        f"/bookings/{booking.id}/update-status",
        data={"status": "In Progress"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    db.session.refresh(booking)
    assert booking.status == "In Progress"

    # Transition to 'Completed'
    client.post(
        f"/bookings/{booking.id}/update-status",
        data={"status": "Completed"},
        follow_redirects=True,
    )
    db.session.refresh(booking)
    assert booking.status == "Completed"


def test_add_spare_part(client, init_db):
    """Verify adding an inventory spare part persists to database with correct pricing."""
    login(client, "testadmin", "password123")

    part_payload = {
        "name": "Brake Pad Set Front",
        "category": "Brakes",
        "quantity": 12,
        "unit_price": 650.0,
        "minimum_stock": 4,
    }

    response = client.post("/inventory/add", data=part_payload, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith(("/inventory", "/inventory/"))

    # Verify in database
    part = SparePart.query.filter_by(name="Brake Pad Set Front").first()
    assert part is not None
    assert part.category == "Brakes"
    assert part.quantity == 12
    assert part.unit_price == 650.0
    assert part.minimum_stock == 4


def test_spare_part_low_stock(client, init_db):
    """Verify SparePart.is_low_stock property logic and inventory low-stock filter."""
    # 1. Critical low stock (quantity < minimum_stock)
    low_part = SparePart(
        name="Spark Plug WSR",
        category="Electrical",
        quantity=2,
        unit_price=180.0,
        minimum_stock=5,
    )
    db.session.add(low_part)

    # 2. Adequate stock (quantity > minimum_stock)
    adequate_part = SparePart(
        name="Air Filter Foam",
        category="Filters",
        quantity=15,
        unit_price=250.0,
        minimum_stock=5,
    )
    db.session.add(adequate_part)

    # 3. Boundary equality (quantity == minimum_stock)
    boundary_part = SparePart(
        name="Chain Lube Spray",
        category="Lubricants & Fluids",
        quantity=5,
        unit_price=320.0,
        minimum_stock=5,
    )
    db.session.add(boundary_part)
    db.session.commit()

    # Verify model property directly
    assert low_part.is_low_stock is True
    assert adequate_part.is_low_stock is False
    assert boundary_part.is_low_stock is True

    # Test inventory view with low_stock filter
    login(client, "testadmin", "password123")
    resp = client.get("/inventory/?low_stock=1")
    assert resp.status_code == 200
    assert b"Spark Plug WSR" in resp.data
    assert b"Chain Lube Spray" in resp.data
    assert b"Air Filter Foam" not in resp.data


def test_create_invoice(client, init_db):
    """Verify invoice creation computes grand totals, line items, and marks booking completed."""
    login(client, "testadmin", "password123")
    booking = init_db["booking"]
    part = init_db["spare_part"]  # Unit price: 450.0, quantity: 20

    invoice_payload = {
        "booking_id": booking.id,
        "labour_charge": 500.0,
        "payment_method": "UPI",
        "status": "Paid",
        "notes": "General service completed and engine oil replaced",
        "part_id[]": [str(part.id)],
        "quantity[]": ["2"],
    }

    response = client.post("/billing/create", data=invoice_payload, follow_redirects=False)
    assert response.status_code == 302

    # Verify invoice in database
    invoice = Invoice.query.filter_by(booking_id=booking.id).first()
    assert invoice is not None
    assert invoice.customer_id == booking.customer_id
    assert invoice.motorcycle_id == booking.motorcycle_id
    assert invoice.labour_charge == 500.0
    assert invoice.parts_total == 900.0  # 2 x 450.0
    assert invoice.grand_total == 1400.0  # 500.0 labour + 900.0 parts
    assert invoice.status == "Paid"
    assert invoice.payment_method == "UPI"

    # Verify invoice line items
    assert len(invoice.items) == 1
    item = invoice.items[0]
    assert item.spare_part_id == part.id
    assert item.part_name == part.name
    assert item.quantity == 2
    assert item.unit_price == 450.0
    assert item.total_price == 900.0

    # Verify booking status auto-transition to 'Completed'
    db.session.refresh(booking)
    assert booking.status == "Completed"


def test_duplicate_invoice_prevention(client, init_db):
    """Verify system prevents creating a second invoice for the same service booking."""
    login(client, "testadmin", "password123")
    booking = init_db["booking"]

    # Create the first invoice
    inv1 = Invoice(
        invoice_number="RE-2026-9001",
        booking_id=booking.id,
        customer_id=booking.customer_id,
        motorcycle_id=booking.motorcycle_id,
        invoice_date=date.today(),
        labour_charge=300.0,
        parts_total=0.0,
        grand_total=300.0,
        status="Paid",
        payment_method="Cash",
    )
    db.session.add(inv1)
    db.session.commit()

    # Attempt second invoice creation for the same booking
    duplicate_payload = {
        "booking_id": booking.id,
        "labour_charge": 400.0,
        "payment_method": "Cash",
        "status": "Unpaid",
    }
    response = client.post("/billing/create", data=duplicate_payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invoice already exists for Booking #" in response.data

    # Ensure only 1 invoice exists for this booking in the database
    assert Invoice.query.filter_by(booking_id=booking.id).count() == 1


def test_inventory_deduction(client, init_db):
    """Verify that creating an invoice properly deducts consumed spare parts quantity."""
    login(client, "testadmin", "password123")
    booking = init_db["booking"]
    part = init_db["spare_part"]

    initial_qty = part.quantity
    used_qty = 3

    invoice_payload = {
        "booking_id": booking.id,
        "labour_charge": 350.0,
        "payment_method": "Cash",
        "status": "Paid",
        "part_id[]": [str(part.id)],
        "quantity[]": [str(used_qty)],
    }

    response = client.post("/billing/create", data=invoice_payload, follow_redirects=False)
    assert response.status_code == 302

    # Verify spare part quantity was reduced in database
    db.session.refresh(part)
    assert part.quantity == initial_qty - used_qty


def test_logout(client, init_db):
    """Verify logout terminates session and redirects user back to login page."""
    login(client, "testadmin", "password123")

    # Confirm authenticated state
    dash_check = client.get("/dashboard")
    assert dash_check.status_code == 200

    # Perform logout
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    followed = client.get("/logout", follow_redirects=True)
    assert followed.status_code == 200
    assert b"You have been logged out safely." in followed.data

    # Confirm subsequent protected access is redirected to login
    re_check = client.get("/dashboard", follow_redirects=False)
    assert re_check.status_code == 302
    assert "/login" in re_check.headers["Location"]


def test_admin_password_hashing(app):
    """Verify Admin model password hashing and verification logic."""
    admin = Admin(username="securityadmin", email="security@regarage.com")
    admin.set_password("SecurePassword2026!")

    assert admin.password_hash != "SecurePassword2026!"
    assert admin.check_password("SecurePassword2026!") is True
    assert admin.check_password("WrongPassword") is False


def test_insufficient_stock_prevents_invoice(client, init_db):
    """Verify billing validation rejects invoice creation when requested quantity exceeds stock."""
    login(client, "testadmin", "password123")
    booking = init_db["booking"]
    part = init_db["spare_part"]  # Available quantity: 20

    invoice_payload = {
        "booking_id": booking.id,
        "labour_charge": 500.0,
        "payment_method": "Cash",
        "status": "Paid",
        "part_id[]": [str(part.id)],
        "quantity[]": ["999"],  # Far exceeds available stock
    }

    response = client.post("/billing/create", data=invoice_payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Insufficient stock for" in response.data

    # Ensure inventory was not altered and invoice was not created
    db.session.refresh(part)
    assert part.quantity == 20
    assert Invoice.query.filter_by(booking_id=booking.id).first() is None


def test_motorcycle_by_customer_api(client, init_db):
    """Verify API endpoint returning motorcycles by customer ID for cascading UI dropdowns."""
    login(client, "testadmin", "password123")
    customer_id = init_db["customer"].id

    response = client.get(f"/motorcycles/by-customer/{customer_id}")
    assert response.status_code == 200

    bikes = response.get_json()
    assert isinstance(bikes, list)
    assert len(bikes) == 1
    assert bikes[0]["registration_number"] == "MH02AB1234"
    assert bikes[0]["model"] == "Classic 350"
    assert bikes[0]["odometer"] == 12500
