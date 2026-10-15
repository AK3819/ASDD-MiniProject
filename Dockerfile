# Use official lightweight Python 3.13 image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency requirements file
COPY requirements.txt .

# Install dependencies and gunicorn WSGI server
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all application source code
COPY . .

# Ensure instance directory exists for SQLite database storage
RUN mkdir -p instance

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set environment variables for production execution
ENV FLASK_ENV=production
ENV SECRET_KEY=re-garage-docker-secret-key-2026

# Start production server with 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "run:app"]
