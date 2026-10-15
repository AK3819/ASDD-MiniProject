from datetime import date, timedelta
from app import create_app, db
from app.models import Admin, Customer, Motorcycle, ServiceBooking, SparePart, Invoice, InvoiceItem

app = create_app("development")


def seed_database():
    with app.app_context():
        # Clear existing tables
        db.drop_all()
        db.create_all()
        print("[*] Recreated database tables.")

        # 1. Create Default Admin
        admin = Admin(
            username="admin",
            email="admin@regarage.com",
        )
        admin.set_password("admin123")
        db.session.add(admin)
        print("[*] Created default admin (admin / admin123).")

        # 2. Create Customers
        customers_data = [
            Customer(name="Vikram Malhotra", mobile="9823011223", email="vikram.malhotra@gmail.com", address="Bavdhan, Pune, Maharashtra 411021"),
            Customer(name="Rajesh Sharma", mobile="9876543210", email="rajesh.sharma@yahoo.com", address="Bandra West, Mumbai, Maharashtra 400050"),
            Customer(name="Anita Desai", mobile="9123456789", email="anita.desai@outlook.com", address="Indiranagar, Bangalore, Karnataka 560038"),
            Customer(name="Rohan Kulkarni", mobile="9422019988", email="rohan.kulkarni@gmail.com", address="College Road, Nashik, Maharashtra 422005"),
            Customer(name="Sameer Khan", mobile="9911223344", email="sameer.khan@hotmail.com", address="Connaught Place, New Delhi, Delhi 110001"),
        ]
        db.session.add_all(customers_data)
        db.session.flush()

        # 3. Create Motorcycles
        motorcycles_data = [
            Motorcycle(customer_id=customers_data[0].id, registration_number="MH-12-RE-1901", model="Classic 350", manufacturing_year=2022, odometer_reading=14500),
            Motorcycle(customer_id=customers_data[0].id, registration_number="MH-12-HM-4111", model="Himalayan", manufacturing_year=2021, odometer_reading=22300),
            Motorcycle(customer_id=customers_data[1].id, registration_number="MH-02-HN-7821", model="Hunter 350", manufacturing_year=2023, odometer_reading=8200),
            Motorcycle(customer_id=customers_data[2].id, registration_number="KA-01-MT-4490", model="Meteor 350", manufacturing_year=2022, odometer_reading=12100),
            Motorcycle(customer_id=customers_data[3].id, registration_number="MH-15-BL-3500", model="Bullet 350", manufacturing_year=2019, odometer_reading=34000),
            Motorcycle(customer_id=customers_data[4].id, registration_number="DL-03-IN-6500", model="Interceptor 650", manufacturing_year=2023, odometer_reading=6800),
        ]
        db.session.add_all(motorcycles_data)
        db.session.flush()

        # 4. Create Spare Parts Inventory
        parts_data = [
            SparePart(name="RE Genuine Engine Oil 15W-50 Semi-Synth (2.5L)", category="Lubricants & Fluids", quantity=25, unit_price=650.0, minimum_stock=8),
            SparePart(name="Oil Filter Element (RE Classic/Meteor)", category="Filters", quantity=18, unit_price=180.0, minimum_stock=6),
            SparePart(name="Front Disc Brake Pads (ByBre)", category="Brakes", quantity=12, unit_price=850.0, minimum_stock=4),
            SparePart(name="Rear Brake Shoes / Pads Kit", category="Brakes", quantity=3, unit_price=620.0, minimum_stock=5),  # Low stock
            SparePart(name="Drive Chain & Sprocket Kit (Brass Plated)", category="Transmission", quantity=2, unit_price=2950.0, minimum_stock=4),  # Low stock
            SparePart(name="Spark Plug Bosch Twin Electrode", category="Electrical", quantity=22, unit_price=220.0, minimum_stock=6),
            SparePart(name="High Flow Air Filter Element", category="Filters", quantity=14, unit_price=340.0, minimum_stock=5),
            SparePart(name="Heavy-Duty Clutch Cable Assembly", category="Transmission", quantity=8, unit_price=280.0, minimum_stock=3),
            SparePart(name="Throttle Accelerator Cable", category="Engine", quantity=2, unit_price=240.0, minimum_stock=4),  # Low stock
            SparePart(name="Headlamp Bulb H4 60/55W Halogen", category="Electrical", quantity=11, unit_price=310.0, minimum_stock=4),
            SparePart(name="Front Fork Oil Seal & Dust Cap Pair", category="Body & Frame", quantity=7, unit_price=450.0, minimum_stock=3),
            SparePart(name="Motul C1 & C2 Chain Care Combo Spray", category="Lubricants & Fluids", quantity=16, unit_price=580.0, minimum_stock=5),
        ]
        db.session.add_all(parts_data)
        db.session.flush()

        today = date.today()

        # 5. Create Service Bookings
        b1 = ServiceBooking(
            customer_id=customers_data[0].id,
            motorcycle_id=motorcycles_data[0].id,
            service_type="General Service",
            booking_date=today - timedelta(days=12),
            problem_description="Periodic 15,000km service. Engine oil change, tappet inspection, brake overhaul.",
            estimated_cost=2500.0,
            status="Completed",
        )
        b2 = ServiceBooking(
            customer_id=customers_data[1].id,
            motorcycle_id=motorcycles_data[2].id,
            service_type="Oil Change",
            booking_date=today - timedelta(days=7),
            problem_description="Rough gear shifts, clutch feels stiff. Needs engine oil replacement and filter change.",
            estimated_cost=1200.0,
            status="Completed",
        )
        b3 = ServiceBooking(
            customer_id=customers_data[2].id,
            motorcycle_id=motorcycles_data[3].id,
            service_type="Brake Service",
            booking_date=today - timedelta(days=3),
            problem_description="Front brake screeching on deceleration. Inspect brake pads and fluid level.",
            estimated_cost=1800.0,
            status="Completed",
        )
        b4 = ServiceBooking(
            customer_id=customers_data[3].id,
            motorcycle_id=motorcycles_data[4].id,
            service_type="Engine Repair",
            booking_date=today - timedelta(days=1),
            problem_description="Engine misfire under acceleration. Carburetor tuning and spark plug replacement required.",
            estimated_cost=3200.0,
            status="In Progress",
        )
        b5 = ServiceBooking(
            customer_id=customers_data[4].id,
            motorcycle_id=motorcycles_data[5].id,
            service_type="Chain Maintenance",
            booking_date=today,
            problem_description="Chain slack high, noisy rattling sound from secondary drive.",
            estimated_cost=1000.0,
            status="Pending",
        )
        b6 = ServiceBooking(
            customer_id=customers_data[0].id,
            motorcycle_id=motorcycles_data[1].id,
            service_type="Electrical Repair",
            booking_date=today - timedelta(days=15),
            problem_description="Customer cancelled due to out-of-station tour.",
            estimated_cost=800.0,
            status="Cancelled",
        )
        db.session.add_all([b1, b2, b3, b4, b5, b6])
        db.session.flush()

        # 6. Create Invoices for Completed Services
        # Invoice 1 (Paid)
        inv1 = Invoice(
            invoice_number="RE-2026-0001",
            booking_id=b1.id,
            customer_id=b1.customer_id,
            motorcycle_id=b1.motorcycle_id,
            invoice_date=today - timedelta(days=11),
            labour_charge=950.0,
            parts_total=1170.0,
            grand_total=2120.0,
            status="Paid",
            payment_method="UPI",
            notes="Periodic 15,000 km general service completed. Customer satisfied with test ride.",
        )
        db.session.add(inv1)
        db.session.flush()

        item1_1 = InvoiceItem(
            invoice_id=inv1.id,
            spare_part_id=parts_data[0].id,
            part_name=parts_data[0].name,
            quantity=1,
            unit_price=650.0,
            total_price=650.0,
        )
        item1_2 = InvoiceItem(
            invoice_id=inv1.id,
            spare_part_id=parts_data[1].id,
            part_name=parts_data[1].name,
            quantity=1,
            unit_price=180.0,
            total_price=180.0,
        )
        item1_3 = InvoiceItem(
            invoice_id=inv1.id,
            spare_part_id=parts_data[6].id,
            part_name=parts_data[6].name,
            quantity=1,
            unit_price=340.0,
            total_price=340.0,
        )
        db.session.add_all([item1_1, item1_2, item1_3])

        # Invoice 2 (Paid)
        inv2 = Invoice(
            invoice_number="RE-2026-0002",
            booking_id=b2.id,
            customer_id=b2.customer_id,
            motorcycle_id=b2.motorcycle_id,
            invoice_date=today - timedelta(days=6),
            labour_charge=450.0,
            parts_total=830.0,
            grand_total=1280.0,
            status="Paid",
            payment_method="Cash",
            notes="Engine oil flushed and replaced. Clutch free play adjusted.",
        )
        db.session.add(inv2)
        db.session.flush()

        item2_1 = InvoiceItem(
            invoice_id=inv2.id,
            spare_part_id=parts_data[0].id,
            part_name=parts_data[0].name,
            quantity=1,
            unit_price=650.0,
            total_price=650.0,
        )
        item2_2 = InvoiceItem(
            invoice_id=inv2.id,
            spare_part_id=parts_data[1].id,
            part_name=parts_data[1].name,
            quantity=1,
            unit_price=180.0,
            total_price=180.0,
        )
        db.session.add_all([item2_1, item2_2])

        # Invoice 3 (Unpaid)
        inv3 = Invoice(
            invoice_number="RE-2026-0003",
            booking_id=b3.id,
            customer_id=b3.customer_id,
            motorcycle_id=b3.motorcycle_id,
            invoice_date=today - timedelta(days=2),
            labour_charge=600.0,
            parts_total=850.0,
            grand_total=1450.0,
            status="Unpaid",
            payment_method="Card",
            notes="Front disc pads replaced. Caliper pins greased.",
        )
        db.session.add(inv3)
        db.session.flush()

        item3_1 = InvoiceItem(
            invoice_id=inv3.id,
            spare_part_id=parts_data[2].id,
            part_name=parts_data[2].name,
            quantity=1,
            unit_price=850.0,
            total_price=850.0,
        )
        db.session.add(item3_1)

        db.session.commit()
        print("[*] Sample database seeded successfully with customers, motorcycles, parts, bookings, and invoices!")


if __name__ == "__main__":
    seed_database()
