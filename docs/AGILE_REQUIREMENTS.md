# RE Garage — Agile Requirements

## 1. Product Backlog

| Backlog ID | Feature / Epic | User Story Summary | Business Value | Story Points | Priority |
|------------|----------------|-------------------|----------------|--------------|----------|
| **PB-01** | Authentication | Admin authentication, secure login/logout, session management, safe first-time setup | Critical | 5 | Must Have (Sprint 1) |
| **PB-02** | Dashboard | Real database analytics (customers, motorcycles, bookings, revenue, low stock) | High | 5 | Must Have (Sprint 1) |
| **PB-03** | Customer Mgmt | Full CRUD for customers with search and active-booking safe deletion validation | High | 5 | Must Have (Sprint 1) |
| **PB-04** | Motorcycle Mgmt | Motorcycle registration linked to customers, unique number plate validation, model catalog | High | 5 | Must Have (Sprint 1) |
| **PB-05** | Service Bookings | Job card booking system with status workflow (Pending -> In Progress -> Completed), AJAX bike selector | Critical | 8 | Must Have (Sprint 2) |
| **PB-06** | Inventory Mgmt | Spare parts catalog, unit pricing, real-time quantity tracking, minimum stock warnings | High | 5 | Must Have (Sprint 2) |
| **PB-07** | Billing & Invoicing | Automated invoice generator with labour charges, parts line items, stock deduction, print view | Critical | 8 | Must Have (Sprint 2) |
| **PB-08** | Service History | Past service logs, search by motorcycle registration or customer name, invoice links | Medium | 3 | Should Have (Sprint 2) |
| **PB-09** | Quality & Testing | Comprehensive Pytest suite testing auth, CRUD, status updates, invoice math, stock deduction | Critical | 5 | Must Have (Sprint 3) |
| **PB-10** | Containerization | Dockerfile and Docker Compose with persistent SQLite volume and Gunicorn WSGI | Critical | 5 | Must Have (Sprint 3) |
| **PB-11** | DevOps CI | GitHub Actions automated test execution and Docker image build pipeline on push/PR | High | 3 | Must Have (Sprint 3) |
| **PB-12** | Documentation | Complete project report, sprint plans, viva guide, and architectural diagrams | High | 3 | Must Have (Sprint 3) |

---

## 2. User Stories & Acceptance Criteria

### User Story 1 (US-01): Admin Login & Authentication
- **As a** workshop supervisor or garage administrator,
- **I want to** log in securely using my credentials,
- **So that** customer motorcycle records, billing details, and inventory data are protected from unauthorized access.

**Acceptance Criteria:**
1. Passwords must be hashed using a cryptographic hash (PBKDF2/SHA256).
2. Unauthenticated requests to protected endpoints redirect to `/login`.
3. An active session persists across pages; logout terminates the session immediately.
4. If the database has no admin account, a setup interface `/init-admin` allows safe creation.

---

### User Story 2 (US-02): Live Analytics Dashboard
- **As a** garage manager,
- **I want to** view operational statistics directly from the database upon logging in,
- **So that** I have immediate visibility over active service workloads, revenue, and inventory alerts.

**Acceptance Criteria:**
1. Cards display live counts for Total Customers, Total Motorcycles, and Total Bookings.
2. Service status breakdown reflects accurate counts for Pending, In Progress, and Completed.
3. Total Revenue calculates dynamically from the sum of grand totals for Paid invoices.
4. Low stock inventory warnings highlight any part where `quantity <= minimum_stock`.

---

### User Story 3 (US-03): Customer Management
- **As a** service receptionist,
- **I want to** add, search, view, and edit customer contact profiles,
- **So that** the workshop has accurate contact details for motorcycle owners.

**Acceptance Criteria:**
1. Customer name and mobile number (minimum 10 digits) are mandatory.
2. Search input filters customers in real-time across name, mobile number, and email.
3. Deleting a customer with active (Pending/In Progress) bookings is blocked to prevent orphaned jobs.

---

### User Story 4 (US-04): Motorcycle Registration
- **As a** service advisor,
- **I want to** register Royal Enfield motorcycles linked to their respective owners,
- **So that** the garage tracks the service lifecycle, odometer readings, and model history of each bike.

**Acceptance Criteria:**
1. Registration numbers are automatically capitalized and enforced to be unique.
2. Model options include Royal Enfield catalog choices: Bullet 350, Classic 350, Hunter 350, Meteor 350, Himalayan, Interceptor 650, Continental GT 650, or Other.
3. Manufacturing year and odometer reading must be non-negative.

---

### User Story 5 (US-05): Service Booking Workflow
- **As a** workshop foreman,
- **I want to** create service job bookings with problem descriptions and advance their status,
- **So that** the mechanics know what maintenance is needed and customers can track job progress.

**Acceptance Criteria:**
1. The motorcycle selector dynamically updates via AJAX when a customer is chosen.
2. Service status transitions through: `Pending` → `In Progress` → `Completed` (or `Cancelled`).
3. Quick status change buttons allow fast updates directly from the bookings table.

---

### User Story 6 (US-06): Spare Parts Inventory Management
- **As a** parts store manager,
- **I want to** manage our stock of genuine spare parts and receive low-stock alerts,
- **So that** mechanics never run out of critical maintenance parts during a service.

**Acceptance Criteria:**
1. Parts are categorized into Engine, Brakes, Transmission, Electrical, Body & Frame, Lubricants & Fluids, Filters, and Other.
2. Parts with quantity less than or equal to minimum stock are flagged with red low-stock badges.
3. Spare parts referenced in prior invoices cannot be deleted, preserving historical accounting records.

---

### User Story 7 (US-07): Billing, Invoicing & Stock Deduction
- **As an** accounts manager,
- **I want to** generate detailed invoices with labour charges and consumed spare parts,
- **So that** customers receive transparent bills and stock quantities are automatically updated.

**Acceptance Criteria:**
1. Invoices can only be created once per service booking (duplicate invoice creation is blocked).
2. Line totals (`quantity * unit_price`), parts total, and grand total (`labour + parts`) calculate automatically.
3. Spare parts quantities are deducted from inventory upon invoice creation.
4. Billing verifies stock availability before finalizing; if stock is insufficient, an error is raised.
5. Invoices feature printable styling with payment status toggling (`Paid` / `Unpaid`).

---

### User Story 8 (US-08): Service History & Record Lookup
- **As a** mechanic or garage manager,
- **I want to** look up past service records by motorcycle registration number or customer name,
- **So that** I can review previous maintenance dates, complaints, and parts replaced.

**Acceptance Criteria:**
1. Lists all completed service bookings sorted chronologically (newest first).
2. Search query filters across registration number, customer name, mobile, and bike model.
3. Direct link to the generated invoice for each completed service order.
