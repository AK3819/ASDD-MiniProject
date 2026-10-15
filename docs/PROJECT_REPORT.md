# RE Garage — Project Report

## 1. Introduction

RE Garage is a web-based Motorcycle Service Management System designed to streamline the operations of a Royal Enfield specialist workshop. The application provides a centralized digital platform for managing customers, motorcycles, service bookings, spare parts inventory, billing, and service history.

This project is developed as an Agile Software Development and DevOps (ASDD) Mini Project, demonstrating the practical application of Agile methodologies, modern web development, containerization, and CI/CD practices.

---

## 2. Problem Statement

Traditional motorcycle service garages often rely on manual record-keeping using paper registers and spreadsheets. This leads to:

- **Data Loss Risk:** Physical records can be damaged or lost.
- **Inefficient Searches:** Finding a customer's past service history is time-consuming.
- **Inventory Mismanagement:** Spare parts stock levels are not tracked in real-time, causing delays.
- **Billing Errors:** Manual invoice calculations are prone to mistakes.
- **No Centralized System:** Information is scattered across multiple registers.

RE Garage addresses these problems by providing a single, integrated digital solution.

---

## 3. Objectives

1. Develop a fully functional web application for motorcycle service workshop management.
2. Implement complete CRUD operations for customers, motorcycles, bookings, and spare parts.
3. Build an automated billing and invoicing system with inventory deduction.
4. Create a professional, responsive user interface with a dark theme.
5. Apply Agile Software Development methodology with sprint-based planning.
6. Demonstrate DevOps practices using Docker containerization and CI/CD pipelines.
7. Write automated tests using Pytest for quality assurance.

---

## 4. Scope

### In Scope
- Admin authentication and authorization
- Customer and motorcycle registration management
- Service booking creation and status tracking
- Spare parts inventory management with low-stock alerts
- Invoice generation with automatic total calculation
- Service history lookup by registration number
- Docker deployment and GitHub Actions CI pipeline
- Responsive dark-themed UI for desktop and mobile

### Out of Scope
- Multi-user role management (only admin role implemented)
- Email/SMS notification system
- Online payment gateway integration
- Mobile native application
- Cloud deployment (designed for local/Docker deployment)

---

## 5. Technologies Used

| Category | Technology | Purpose |
|----------|-----------|---------|
| Frontend | HTML5, CSS3, JavaScript | Structure, styling, interactivity |
| CSS Framework | Bootstrap 5 | Responsive layout and components |
| Icons | Bootstrap Icons | UI iconography |
| Backend | Python 3.13 | Server-side programming |
| Web Framework | Flask 3.0 | HTTP routing and templating |
| ORM | Flask-SQLAlchemy | Database abstraction layer |
| Auth | Flask-Login | Session and authentication management |
| Database | SQLite | Lightweight relational database |
| Testing | Pytest | Automated unit and integration testing |
| Containerization | Docker, Docker Compose | Application packaging and deployment |
| CI/CD | GitHub Actions | Automated testing and build pipeline |
| Version Control | Git, GitHub | Source code management |

---

## 6. System Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                   CLIENT BROWSER                 │
│         (HTML5 / CSS3 / JS / Bootstrap 5)        │
└──────────────────────┬──────────────────────────┘
                       │ HTTP Requests
                       ▼
┌─────────────────────────────────────────────────┐
│              FLASK WEB SERVER                    │
│  ┌─────────────┐  ┌──────────────────────────┐  │
│  │  Flask-Login │  │     Route Blueprints     │  │
│  │  (Auth)      │  │  auth | dashboard | ...  │  │
│  └─────────────┘  └──────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐│
│  │          Flask-SQLAlchemy ORM               ││
│  │   Admin | Customer | Motorcycle | Booking   ││
│  │   SparePart | Invoice | InvoiceItem         ││
│  └─────────────────────────────────────────────┘│
└──────────────────────┬──────────────────────────┘
                       │ SQL Queries
                       ▼
┌─────────────────────────────────────────────────┐
│              SQLite DATABASE                     │
│           (instance/re_garage.db)                │
└─────────────────────────────────────────────────┘
```

### Docker Architecture

```
┌─────────────────────────────────────────────────┐
│               DOCKER HOST                        │
│  ┌───────────────────────────────────────────┐   │
│  │         Docker Container                  │   │
│  │   ┌──────────────────────────────────┐    │   │
│  │   │  Python 3.13-slim + Gunicorn     │    │   │
│  │   │  Flask Application (Port 5000)   │    │   │
│  │   └──────────────────────────────────┘    │   │
│  │              │                            │   │
│  │              ▼                            │   │
│  │   ┌──────────────────────────────────┐    │   │
│  │   │ /app/instance/re_garage.db       │    │   │
│  │   │ (Mounted Docker Volume)          │    │   │
│  │   └──────────────────────────────────┘    │   │
│  └───────────────────────────────────────────┘   │
│                                                   │
│  Volume: re_garage_data → /app/instance           │
│  Port:   localhost:5000 → container:5000          │
└─────────────────────────────────────────────────┘
```

---

## 7. Modules

### Module 1: Admin Authentication
- Secure login with password hashing (Werkzeug)
- Session-based authentication (Flask-Login)
- Protected routes requiring login
- Safe initial admin setup page (/init-admin)
- Logout functionality

### Module 2: Dashboard
- Displays real-time statistics from the database
- Total customers, motorcycles, bookings counts
- Service status breakdown (Pending, In Progress, Completed)
- Total revenue from paid invoices
- Recent bookings table
- Low stock alerts
- Quick action buttons

### Module 3: Customer Management
- Add, view, edit, and delete customers
- Fields: Name, Mobile, Email, Address
- Search by name, mobile, or email
- Safe deletion (prevents deleting customers with active bookings)
- Customer detail page showing linked motorcycles and bookings

### Module 4: Motorcycle Management
- Register motorcycles linked to existing customers
- Unique registration number enforcement
- Model selection from Royal Enfield catalog
- Search by registration number or customer name
- Cascading customer-motorcycle dropdown via AJAX

### Module 5: Service Booking
- Create service bookings with type, date, cost estimate, and description
- Status workflow: Pending → In Progress → Completed / Cancelled
- Quick status update from the bookings list
- Filter bookings by status
- Link to invoice generation for completed bookings

### Module 6: Spare Parts Inventory
- Add, edit, and delete spare parts
- Categories: Engine, Brakes, Transmission, Electrical, etc.
- Quantity tracking with low-stock threshold alerts
- Search and filter by category
- Safe deletion (prevents deleting parts used in past invoices)
- JSON API endpoint for dynamic billing form

### Module 7: Billing & Invoicing
- Generate invoices for service bookings
- Add labour charges and spare parts with quantities
- Automatic line total and grand total calculation
- Inventory deduction on invoice creation
- Duplicate invoice prevention per booking
- Print-friendly invoice view
- Mark invoices as Paid or Unpaid

### Module 8: Service History
- View all completed services
- Search by registration number, customer name, or model
- Links to associated invoices

---

## 8. Conclusion

RE Garage successfully demonstrates the development of a full-stack web application using modern technologies and Agile/DevOps practices. The project covers:

- **Agile Development:** Sprint-based planning with user stories and acceptance criteria
- **Full-Stack Development:** Flask backend with Bootstrap 5 frontend and SQLite database
- **DevOps Practices:** Docker containerization, GitHub version control, and CI/CD pipeline
- **Testing:** Automated tests using Pytest covering authentication, CRUD operations, and business logic

The application is ready for demonstration, can be deployed via Docker, and provides a practical example of how Agile and DevOps methodologies are applied in software development.
