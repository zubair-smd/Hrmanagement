# Use an official Python image from DockerHub
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies and system libraries (for SQLite, Python packages)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && apt-get clean

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project files into the container
COPY . /app/

# Expose the default Django port (you can customize it)
EXPOSE 8000

# Set the command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]