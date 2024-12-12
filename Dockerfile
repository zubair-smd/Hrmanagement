# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Create a non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies as non-root user
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Change ownership of the application directory
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Any additional setup (e.g., database migrations, collecting static files)
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]