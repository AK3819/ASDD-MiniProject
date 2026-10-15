# RE Garage — Royal Enfield Motorcycle Service Management System

<p align="center">
  <strong>🏍️ RE GARAGE PRO</strong><br/>
  <em>Specialist Royal Enfield Service Workshop Management</em><br/><br/>
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-green?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap" alt="Bootstrap">
  <img src="https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Docker-Ready-blue?logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-yellow?logo=github-actions" alt="CI">
</p>

---

## 📋 About

**RE Garage** is a full-stack web application built to manage a motorcycle service workshop. It handles customer records, motorcycle registration, service bookings, spare parts inventory, billing/invoicing, and service history — all through a premium dark-themed dashboard.

> **Note:** This is an academic demonstration project developed as an ASDD (Agile Software Development and DevOps) Mini Project. It is not an official Royal Enfield product.

---

## ✨ Features

| Module | Description |
|--------|-------------|
| **Admin Login** | Secure authentication with password hashing, session management, protected routes |
| **Dashboard** | Real-time statistics from the database — customers, motorcycles, bookings, revenue |
| **Customer Management** | Full CRUD with search. Safe deletion checks for active bookings |
| **Motorcycle Management** | Register bikes linked to customers. Unique registration numbers. Model catalog |
| **Service Bookings** | Create/edit bookings with status workflow (Pending → In Progress → Completed) |
| **Spare Parts Inventory** | Track parts with categories, stock levels, low-stock warnings |
| **Billing & Invoicing** | Generate invoices, add labour + parts, auto-calculate totals, print invoices |
| **Service History** | View completed services, search by registration number, past invoices |

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons |
| **Backend** | Python 3.13, Flask, Flask-SQLAlchemy, Flask-Login |
| **Database** | SQLite |
| **DevOps** | Git, GitHub, Docker, Docker Compose, GitHub Actions |
| **Testing** | Pytest |

---

## 📁 Project Structure

```
RE-Garage-ASDD/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # SQLAlchemy database models
│   ├── routes/
│   │   ├── auth.py              # Login/Logout/Init-Admin
│   │   ├── dashboard.py         # Dashboard statistics
│   │   ├── customers.py         # Customer CRUD
│   │   ├── motorcycles.py       # Motorcycle CRUD
│   │   ├── bookings.py          # Service booking management
│   │   ├── inventory.py         # Spare parts inventory
│   │   ├── billing.py           # Invoice generation
│   │   └── history.py           # Service history
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── customers/
│   │   ├── motorcycles/
│   │   ├── bookings/
│   │   ├── inventory/
│   │   ├── billing/
│   │   ├── history/
│   │   └── errors/
│   └── static/
│       ├── css/custom.css
│       └── js/main.js
├── tests/
│   ├── conftest.py
│   └── test_app.py
├── docs/
│   ├── PROJECT_REPORT.md
│   ├── AGILE_DOCUMENTATION.md
│   └── VIVA_QUESTIONS.md
├── instance/                    # SQLite database (auto-created)
├── config.py                    # App configuration
├── run.py                       # Application entry point
├── seed.py                      # Sample data seeder
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── .env.example
├── .github/workflows/ci.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ installed
- Git installed
- (Optional) Docker Desktop for containerized deployment

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RE-Garage-ASDD.git
cd RE-Garage-ASDD
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed Sample Data (Optional)

```bash
python seed.py
```

This creates a default admin account:
- **Username:** `admin`
- **Password:** `admin123`

### 5. Run the Application

```bash
python run.py
```

Open your browser at: **http://localhost:5000**

### 6. First-Time Setup (Without Seed Data)

If you skip the seed step, visit **http://localhost:5000/init-admin** to create the first admin account through a safe setup form.

---

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
docker compose up --build
```

The application will be available at: **http://localhost:5000**

### Other Docker Commands

```bash
# Build the image manually
docker build -t re-garage .

# Run in detached mode
docker compose up -d

# Check running containers
docker compose ps

# View application logs
docker compose logs -f

# Stop the application
docker compose down

# Stop and remove volumes (resets database)
docker compose down -v
```

The SQLite database is persisted using a Docker volume (`re_garage_data`), so data survives container restarts.

---

## 🧪 Running Tests

```bash
# Run all tests
pytest -v

# Run with output
pytest -v -s

# Run a specific test
pytest tests/test_app.py::test_login_valid_credentials -v
```

---

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

1. **Triggers** on push/PR to `main` branch
2. **Runs tests** using Pytest on Ubuntu with Python 3.13
3. **Builds Docker image** to verify container health

The pipeline runs automatically when code is pushed to GitHub.

---

## 📊 Database Models

| Model | Description |
|-------|-------------|
| `Admin` | Workshop admin users with hashed passwords |
| `Customer` | Customer records (name, mobile, email, address) |
| `Motorcycle` | Bikes linked to customers (registration, model, year, odometer) |
| `ServiceBooking` | Service requests with type, status workflow, and cost estimates |
| `SparePart` | Inventory items with stock levels and low-stock alerts |
| `Invoice` | Generated invoices with labour charges and parts totals |
| `InvoiceItem` | Individual spare parts line items on an invoice |

---

## 🏍️ Supported Motorcycle Models

- Bullet 350
- Classic 350
- Hunter 350
- Meteor 350
- Himalayan
- Interceptor 650
- Continental GT 650
- Other

---

## 📝 Agile Documentation

Detailed Agile and DevOps documentation is available in the `docs/` folder:

- **[Project Report](docs/PROJECT_REPORT.md)** — Introduction, architecture, modules, technologies
- **[Agile Documentation](docs/AGILE_DOCUMENTATION.md)** — User stories, sprint planning, backlog
- **[Viva Questions](docs/VIVA_QUESTIONS.md)** — 20+ Q&A for college viva preparation

---

## 🔒 Default Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ Change these credentials in production. The seed script is for demonstration only.

---

## 📜 License

This project is developed for academic purposes as part of an ASDD Mini Project submission.

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) — Python web framework
- [Bootstrap 5](https://getbootstrap.com/) — Frontend CSS framework
- [Bootstrap Icons](https://icons.getbootstrap.com/) — Icon library
- [SQLAlchemy](https://www.sqlalchemy.org/) — Python ORM
- [Docker](https://www.docker.com/) — Containerization platform
- [GitHub Actions](https://github.com/features/actions) — CI/CD platform
