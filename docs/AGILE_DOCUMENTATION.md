# RE Garage — Agile Documentation

## 1. Product Backlog

| ID | User Story | Priority | Story Points | Sprint |
|----|-----------|----------|-------------|--------|
| PB-01 | Project setup and configuration | High | 3 | Sprint 1 |
| PB-02 | Admin login and authentication | High | 5 | Sprint 1 |
| PB-03 | Dashboard with real statistics | High | 5 | Sprint 1 |
| PB-04 | Customer CRUD management | High | 5 | Sprint 1 |
| PB-05 | Motorcycle CRUD management | High | 5 | Sprint 1 |
| PB-06 | Service booking management | High | 8 | Sprint 2 |
| PB-07 | Spare parts inventory | Medium | 5 | Sprint 2 |
| PB-08 | Billing and invoicing | High | 8 | Sprint 2 |
| PB-09 | Service history module | Medium | 3 | Sprint 2 |
| PB-10 | Automated testing (Pytest) | High | 5 | Sprint 3 |
| PB-11 | Docker containerization | High | 5 | Sprint 3 |
| PB-12 | GitHub Actions CI pipeline | Medium | 3 | Sprint 3 |
| PB-13 | Agile and DevOps documentation | Medium | 3 | Sprint 3 |
| **Total** | | | **63** | |

---

## 2. User Stories

### Sprint 1

**US-01: Admin Login**
> As a workshop admin, I want to log in with a username and password so that only authorized users can access the system.

**Acceptance Criteria:**
- Admin can log in with valid credentials
- Invalid credentials show an error message
- All pages are protected behind authentication
- Admin can log out safely
- First-time setup allows creating initial admin account

---

**US-02: Dashboard Overview**
> As a workshop admin, I want to see a dashboard with real-time statistics so that I can get a quick overview of garage operations.

**Acceptance Criteria:**
- Dashboard displays total customers, motorcycles, bookings, and revenue
- Service status breakdown is shown (Pending, In Progress, Completed)
- Recent bookings are listed
- Low stock alerts are visible
- All numbers come from the actual database

---

**US-03: Customer Management**
> As a workshop admin, I want to add, view, edit, and delete customer records so that I can maintain an up-to-date customer database.

**Acceptance Criteria:**
- Admin can add a new customer with name, mobile, email, and address
- Admin can view all customers in a searchable table
- Admin can edit existing customer details
- Admin can delete customers only if they have no active bookings
- Admin can search customers by name, mobile, or email

---

**US-04: Motorcycle Registration**
> As a workshop admin, I want to register motorcycles linked to customers so that I can track which bikes each customer owns.

**Acceptance Criteria:**
- Admin can add a motorcycle with registration number, model, year, and odometer
- Each motorcycle must belong to a valid customer
- Registration numbers must be unique
- Admin can edit and delete motorcycles (if no active bookings)
- Admin can search motorcycles by registration number

---

### Sprint 2

**US-05: Service Booking**
> As a workshop admin, I want to create and manage service bookings so that I can track work orders for motorcycles.

**Acceptance Criteria:**
- Admin can create a booking selecting customer, motorcycle, service type, and date
- Motorcycle dropdown filters based on selected customer
- Service status can be updated (Pending → In Progress → Completed)
- Bookings can be filtered by status
- Completed bookings can trigger invoice generation

---

**US-06: Spare Parts Inventory**
> As a workshop admin, I want to manage spare parts inventory so that I can track stock levels and avoid running out of parts.

**Acceptance Criteria:**
- Admin can add, edit, and delete spare parts
- Each part has name, category, quantity, unit price, and minimum stock
- Low stock warnings are displayed when quantity ≤ minimum stock
- Parts can be searched and filtered by category
- Parts used in invoices cannot be deleted

---

**US-07: Billing and Invoicing**
> As a workshop admin, I want to generate invoices for completed services so that I can bill customers accurately.

**Acceptance Criteria:**
- Admin can create an invoice for a service booking
- Invoice includes labour charges and spare parts with quantities
- Totals are calculated automatically
- Spare parts inventory is deducted upon invoice creation
- Duplicate invoices for the same booking are prevented
- Invoices can be marked as Paid or Unpaid
- Invoices have a print-friendly view

---

**US-08: Service History**
> As a workshop admin, I want to view past completed services so that I can look up a motorcycle's service history.

**Acceptance Criteria:**
- Admin can see all completed services
- Admin can search by registration number or customer name
- Each history entry links to its invoice (if exists)

---

### Sprint 3

**US-09: Automated Testing**
> As a developer, I want automated tests covering critical functionality so that I can verify the application works correctly.

**Acceptance Criteria:**
- Tests cover login, customer CRUD, motorcycle CRUD, bookings, inventory, and billing
- Tests use an in-memory SQLite database
- All tests pass with `pytest -v`

---

**US-10: Docker Deployment**
> As a DevOps engineer, I want to containerize the application so that it can be deployed consistently on any machine.

**Acceptance Criteria:**
- Dockerfile builds a valid image using Python slim
- Docker Compose starts the application on port 5000
- SQLite database is persisted using a Docker volume
- `docker compose up --build` works successfully

---

**US-11: CI/CD Pipeline**
> As a developer, I want a CI pipeline that runs tests and builds the Docker image automatically on every push to main.

**Acceptance Criteria:**
- GitHub Actions workflow triggers on push/PR to main
- Pipeline installs dependencies and runs Pytest
- Pipeline builds Docker image after tests pass
- Pipeline reports success or failure

---

## 3. Sprint Planning

### Sprint 1 (Week 1-2)

**Sprint Goal:** Set up the project foundation, implement authentication, dashboard, and basic entity management.

| Task | Story Points | Status |
|------|-------------|--------|
| Project setup (Flask, SQLAlchemy, config) | 3 | ✅ Done |
| Database models design | 3 | ✅ Done |
| Admin login/logout system | 5 | ✅ Done |
| Dashboard with real statistics | 5 | ✅ Done |
| Customer CRUD with search | 5 | ✅ Done |
| Motorcycle CRUD with search | 5 | ✅ Done |
| **Sprint Total** | **26** | |

**Sprint Velocity: 26 points**

---

### Sprint 2 (Week 3-4)

**Sprint Goal:** Implement core business modules — service bookings, inventory, billing, and service history.

| Task | Story Points | Status |
|------|-------------|--------|
| Service booking CRUD with status workflow | 8 | ✅ Done |
| Spare parts inventory with low stock alerts | 5 | ✅ Done |
| Billing and invoice generation | 8 | ✅ Done |
| Service history module | 3 | ✅ Done |
| **Sprint Total** | **24** | |

**Sprint Velocity: 24 points**

---

### Sprint 3 (Week 5-6)

**Sprint Goal:** Add testing, DevOps infrastructure, and complete documentation.

| Task | Story Points | Status |
|------|-------------|--------|
| Write Pytest test suite | 5 | ✅ Done |
| Create Dockerfile and compose.yaml | 5 | ✅ Done |
| GitHub Actions CI pipeline | 3 | ✅ Done |
| Agile and DevOps documentation | 3 | ✅ Done |
| **Sprint Total** | **16** | |

**Sprint Velocity: 16 points**

---

## 4. Story Point Estimation

We used the **Fibonacci sequence** (1, 2, 3, 5, 8, 13) for estimating story points:

| Points | Complexity | Example |
|--------|-----------|---------|
| 1-2 | Very Simple | Fix a UI label, add a field |
| 3 | Simple | Service history page, project setup |
| 5 | Moderate | Customer CRUD, inventory management |
| 8 | Complex | Billing with inventory deduction, booking with status workflow |
| 13 | Very Complex | Not used in this project |

---

## 5. Sprint Backlog Summary

| Sprint | Planned Points | Completed Points | Velocity |
|--------|---------------|-----------------|----------|
| Sprint 1 | 26 | 26 | 26 |
| Sprint 2 | 24 | 24 | 24 |
| Sprint 3 | 16 | 16 | 16 |
| **Total** | **66** | **66** | **Avg: 22** |

---

## 6. Testing Table

| Test ID | Test Description | Module | Expected Result | Actual Result | Status |
|---------|-----------------|--------|----------------|---------------|--------|
| T-01 | Login page loads | Auth | HTTP 200, login form displayed | HTTP 200 | ✅ Pass |
| T-02 | Valid login credentials | Auth | Redirect to dashboard | Redirect 302 | ✅ Pass |
| T-03 | Invalid login credentials | Auth | Flash error message | Error shown | ✅ Pass |
| T-04 | Dashboard requires login | Dashboard | Redirect to login | Redirect 302 | ✅ Pass |
| T-05 | Dashboard shows statistics | Dashboard | Page contains stat values | Stats displayed | ✅ Pass |
| T-06 | Add new customer | Customer | Customer saved to database | Customer created | ✅ Pass |
| T-07 | Edit customer | Customer | Customer details updated | Details updated | ✅ Pass |
| T-08 | Search customers | Customer | Matching results displayed | Results found | ✅ Pass |
| T-09 | Add motorcycle | Motorcycle | Motorcycle saved with customer link | Motorcycle created | ✅ Pass |
| T-10 | Unique registration number | Motorcycle | Duplicate rejected | Flash error | ✅ Pass |
| T-11 | Create service booking | Booking | Booking created with Pending status | Booking saved | ✅ Pass |
| T-12 | Update booking status | Booking | Status changed successfully | Status updated | ✅ Pass |
| T-13 | Add spare part | Inventory | Part added to inventory | Part saved | ✅ Pass |
| T-14 | Low stock detection | Inventory | is_low_stock returns True | True returned | ✅ Pass |
| T-15 | Create invoice | Billing | Invoice created, totals calculated | Invoice saved | ✅ Pass |
| T-16 | Duplicate invoice prevention | Billing | Second invoice rejected | Redirect to existing | ✅ Pass |
| T-17 | Inventory deduction on invoice | Billing | Part quantity decreased | Quantity decreased | ✅ Pass |
| T-18 | Logout | Auth | Redirect to login page | Redirect 302 | ✅ Pass |

---

## 7. Git Workflow

We followed a simple **Git Feature Branch Workflow**:

```
main (production-ready)
  ├── feature/auth        → Login and authentication
  ├── feature/dashboard   → Dashboard module
  ├── feature/customers   → Customer management
  ├── feature/motorcycles → Motorcycle management
  ├── feature/bookings    → Service booking system
  ├── feature/inventory   → Spare parts inventory
  ├── feature/billing     → Invoicing system
  ├── feature/docker      → Docker configuration
  └── feature/testing     → Automated tests
```

**Workflow Steps:**
1. Create a feature branch from `main`
2. Develop and test the feature locally
3. Commit changes with meaningful messages
4. Push branch and create Pull Request
5. CI pipeline runs automated tests
6. Merge into `main` after review

---

## 8. Docker Architecture

```
┌──────────────────────────────────────────┐
│            Docker Compose                │
│                                          │
│  Service: re-garage                      │
│  ┌────────────────────────────────────┐  │
│  │  Image: python:3.13-slim          │  │
│  │  Server: Gunicorn (2 workers)     │  │
│  │  App: Flask (run:app)             │  │
│  │  Port: 5000                       │  │
│  └──────────────┬─────────────────────┘  │
│                 │                        │
│  Volume: re_garage_data                  │
│  ┌──────────────▼─────────────────────┐  │
│  │  /app/instance/re_garage.db       │  │
│  │  (Persistent SQLite Database)     │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

**Key Commands:**
- `docker compose up --build` — Build and start
- `docker compose down` — Stop containers
- `docker compose logs` — View logs
- `docker compose ps` — Check running status

---

## 9. CI/CD Pipeline Explanation

```
┌─────────┐     ┌──────────┐     ┌──────────────┐
│  Push /  │────▶│  GitHub  │────▶│   GitHub     │
│   PR     │     │  Repo    │     │   Actions    │
└─────────┘     └──────────┘     └──────┬───────┘
                                        │
                              ┌─────────▼─────────┐
                              │   Job 1: Test      │
                              │  - Checkout code   │
                              │  - Setup Python    │
                              │  - Install deps    │
                              │  - Run pytest -v   │
                              └─────────┬─────────┘
                                        │ (if pass)
                              ┌─────────▼─────────┐
                              │ Job 2: Docker Build│
                              │  - Checkout code   │
                              │  - docker build    │
                              │  - Verify image    │
                              └───────────────────┘
```

The pipeline ensures that:
1. Every code change is automatically tested
2. Docker image is only built if all tests pass
3. Broken code cannot be merged into the main branch
