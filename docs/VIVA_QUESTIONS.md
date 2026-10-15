# RE Garage — Viva Questions & Answers

## ASDD Mini Project Viva Preparation Guide

---

### Q1. What is the purpose of your project?

**Answer:** RE Garage is a web-based Motorcycle Service Management System designed for a Royal Enfield specialist workshop. It manages customers, motorcycles, service bookings, spare parts inventory, billing, and service history through a single integrated web application. It demonstrates Agile Software Development and DevOps practices.

---

### Q2. What technologies did you use and why?

**Answer:** 
- **Flask (Python)** — Lightweight web framework, easy to learn and suitable for moderate-level projects
- **SQLAlchemy** — ORM for database operations, eliminates raw SQL writing
- **SQLite** — File-based database, no separate server installation needed
- **Bootstrap 5** — Responsive UI framework for professional-looking frontend
- **Docker** — Containerization for consistent deployment across environments
- **GitHub Actions** — Free CI/CD pipeline for automated testing
- **Pytest** — Python testing framework for automated test cases

---

### Q3. What is Flask and why did you choose it over Django?

**Answer:** Flask is a micro web framework for Python. I chose Flask because:
- It's lightweight and simple to understand
- It doesn't enforce a specific project structure (flexibility)
- It's suitable for moderate-level projects without unnecessary overhead
- Django would have been over-engineering for this project's scope

---

### Q4. What is SQLAlchemy? What is an ORM?

**Answer:** SQLAlchemy is a Python SQL toolkit and Object-Relational Mapper (ORM). An ORM allows us to interact with the database using Python objects instead of writing raw SQL queries. For example, `Customer.query.all()` translates to `SELECT * FROM customers`. This makes code more readable, maintainable, and secure against SQL injection.

---

### Q5. Explain the MVC architecture of your project.

**Answer:** While Flask doesn't strictly follow MVC, my project implements a similar pattern:
- **Model:** `app/models.py` — SQLAlchemy database models (Admin, Customer, Motorcycle, etc.)
- **View:** `app/templates/` — Jinja2 HTML templates that render the UI
- **Controller:** `app/routes/` — Blueprint route handlers that process requests and connect models to views

---

### Q6. What is a Flask Blueprint? Why did you use them?

**Answer:** A Blueprint is a way to organize a Flask application into modular components. Each module (auth, customers, motorcycles, etc.) is a separate Blueprint with its own routes. Benefits:
- Code is organized by feature, not by file type
- Each blueprint can have its own URL prefix (e.g., `/customers`, `/bookings`)
- Makes the project easier to maintain and understand

---

### Q7. How did you implement authentication?

**Answer:** I used Flask-Login for session-based authentication:
- Passwords are hashed using Werkzeug's `generate_password_hash()` (never stored in plain text)
- `Flask-Login` manages user sessions with `login_user()` and `logout_user()`
- The `@login_required` decorator protects routes from unauthorized access
- A safe `/init-admin` page allows creating the first admin account

---

### Q8. What is password hashing? Why not store plain text passwords?

**Answer:** Password hashing converts a password into a fixed-length string using a one-way mathematical function. Even if the database is compromised, attackers cannot reverse the hash to get the original password. I used Werkzeug's PBKDF2 hashing with SHA-256. Storing plain text passwords is a critical security vulnerability.

---

### Q9. How does the billing system work?

**Answer:** 
1. Admin selects a service booking (that doesn't already have an invoice)
2. Adds labour charges and selects spare parts with quantities
3. The system calculates line totals and grand total automatically
4. On submission, spare parts inventory is deducted atomically
5. If stock is insufficient, the transaction is rejected
6. Only one invoice per booking is allowed (duplicate prevention)
7. The invoice can be marked as Paid or Unpaid

---

### Q10. What is Docker and why did you use it?

**Answer:** Docker is a containerization platform that packages an application with all its dependencies into a standardized unit called a container. I used Docker because:
- It ensures the application runs the same way on any machine
- No need to install Python or dependencies manually on the host
- The SQLite database is persisted using Docker volumes
- It demonstrates DevOps practices required for the ASDD submission

---

### Q11. Explain your Dockerfile.

**Answer:** My Dockerfile:
1. `FROM python:3.13-slim` — Uses a lightweight Python base image
2. `WORKDIR /app` — Sets the working directory inside the container
3. `COPY requirements.txt .` and `RUN pip install` — Installs dependencies (cached layer)
4. `COPY . .` — Copies application source code
5. `EXPOSE 5000` — Documents the port the app listens on
6. `CMD ["gunicorn", ...]` — Runs the production server (Gunicorn)

---

### Q12. What is Docker Compose? How does it differ from Docker?

**Answer:** Docker builds and runs individual containers. Docker Compose is a tool for defining and running multi-container applications using a YAML file (`compose.yaml`). Even for single-container applications like mine, Compose simplifies management by defining volumes, ports, environment variables, and restart policies in one file. Starting the app is just `docker compose up --build`.

---

### Q13. What is a Docker Volume and why is it important?

**Answer:** A Docker Volume is a persistent storage mechanism that exists outside the container's filesystem. Without a volume, all data (including our SQLite database) would be lost when the container stops or is rebuilt. My `compose.yaml` maps a named volume `re_garage_data` to `/app/instance/` inside the container, ensuring the database persists.

---

### Q14. What is CI/CD? Explain your GitHub Actions pipeline.

**Answer:** CI/CD stands for Continuous Integration / Continuous Deployment.
- **CI:** Automatically running tests whenever code is pushed to catch bugs early
- **CD:** Automatically deploying tested code (not implemented in this project)

My GitHub Actions pipeline:
1. Triggers on push/PR to the `main` branch
2. **Job 1 (Test):** Sets up Python, installs dependencies, runs `pytest -v`
3. **Job 2 (Docker Build):** Runs only if tests pass, builds the Docker image to verify it works

---

### Q15. What Agile methodology did you follow?

**Answer:** I followed **Scrum-based Agile methodology** with:
- **Product Backlog:** Prioritized list of all features
- **User Stories:** Requirements written from the user's perspective ("As a... I want... so that...")
- **Sprint Planning:** 3 sprints of 2 weeks each
- **Story Point Estimation:** Using Fibonacci sequence (1, 2, 3, 5, 8)
- **Sprint Backlog:** Tasks assigned to each sprint
- **Sprint Velocity:** Tracking completed points per sprint

---

### Q16. What are User Stories? Give an example from your project.

**Answer:** A User Story describes a feature from the end-user's perspective. Format: "As a [role], I want [feature], so that [benefit]."

Example: "As a workshop admin, I want to generate invoices for completed services so that I can bill customers accurately."

Each user story has **Acceptance Criteria** — specific conditions that must be met for the story to be considered complete.

---

### Q17. What is Pytest? How did you write tests?

**Answer:** Pytest is a Python testing framework. I wrote tests that:
- Create a test Flask app with an in-memory SQLite database (no file I/O)
- Use fixtures to set up test data (admin user, customers, motorcycles, etc.)
- Make actual HTTP requests using Flask's test client
- Verify both HTTP responses AND database state changes
- Cover authentication, CRUD operations, billing calculations, and inventory deduction

Run tests with: `pytest -v`

---

### Q18. How do you handle safe deletion in your application?

**Answer:** I prevent cascading data loss by checking for dependencies before deletion:
- **Customer deletion:** Blocked if customer has active (Pending/In Progress) service bookings
- **Motorcycle deletion:** Blocked if motorcycle has active service bookings
- **Spare Part deletion:** Blocked if part has been used in past invoice items
- **Booking deletion:** Blocked if an invoice has already been generated

This ensures referential integrity and prevents accidental data loss.

---

### Q19. What is the difference between Gunicorn and Flask's built-in server?

**Answer:** Flask's built-in development server (`flask run`) is single-threaded and not suitable for production. **Gunicorn** (Green Unicorn) is a production-grade WSGI HTTP server that:
- Handles multiple concurrent requests using worker processes
- Is more stable and performant under load
- Is the industry standard for deploying Flask applications
- My Dockerfile uses Gunicorn with 2 worker processes

---

### Q20. Explain the database schema of your project.

**Answer:** My database has 7 tables:
1. **admins** — Admin users with hashed passwords
2. **customers** — Customer records (name, mobile, email, address)
3. **motorcycles** — Bikes linked to customers via `customer_id` foreign key
4. **service_bookings** — Service orders linking customers and motorcycles
5. **spare_parts** — Inventory items with quantities and prices
6. **invoices** — Bills linked to bookings with one-to-one relationship (unique booking_id)
7. **invoice_items** — Line items on invoices linking to spare parts

Foreign key relationships ensure data integrity.

---

### Q21. What is the .gitignore file and why is it important?

**Answer:** `.gitignore` specifies files and directories that Git should ignore and not track. In my project, it excludes:
- `venv/` — Virtual environment (large, machine-specific)
- `instance/*.db` — Database files (contain data, not code)
- `.env` — Environment variables with secrets
- `__pycache__/` — Python bytecode cache
- `.pytest_cache/` — Test cache

This keeps the repository clean and prevents sensitive data from being pushed to GitHub.

---

### Q22. How does the cascading motorcycle dropdown work in the booking form?

**Answer:** When the admin selects a customer in the booking form:
1. JavaScript listens for the `change` event on the customer dropdown
2. It sends a `fetch()` AJAX request to `/motorcycles/by-customer/<customer_id>`
3. The Flask route returns a JSON list of motorcycles belonging to that customer
4. JavaScript dynamically populates the motorcycle dropdown with the results

This provides a smooth user experience without page reloads.

---

### Q23. What is Flask-Login's `@login_required` decorator?

**Answer:** `@login_required` is a decorator that protects a route. When an unauthenticated user tries to access a protected page:
1. Flask-Login intercepts the request
2. Redirects the user to the login page
3. Stores the original URL in a `next` parameter
4. After successful login, redirects back to the originally requested page

---

### Q24. How would you scale this application for production use?

**Answer:** For production scaling, I would:
- Replace SQLite with PostgreSQL or MySQL (multi-user concurrent access)
- Add user role management (admin, technician, receptionist)
- Implement email/SMS notifications for service updates
- Add a proper payment gateway for online payments
- Deploy on a cloud platform (AWS, Azure, or GCP)
- Add Redis for session caching
- Implement backup and disaster recovery for the database

---

### Q25. What challenges did you face during development?

**Answer:** Key challenges:
1. **Cascading dropdowns:** Required AJAX calls to dynamically load motorcycles based on selected customer
2. **Billing with inventory deduction:** Needed atomic transactions to prevent stock inconsistencies
3. **Safe deletion logic:** Had to check multiple foreign key dependencies before allowing deletion
4. **Docker volume persistence:** Ensuring SQLite data survives container restarts required proper volume mapping
5. **Dark theme UI:** Customizing Bootstrap 5 for a consistent dark garage aesthetic required extensive CSS overrides
