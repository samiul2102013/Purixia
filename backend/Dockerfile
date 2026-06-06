# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Create directory for logs and static files
RUN mkdir -p /app/logs /app/staticfiles /app/media

# Collect static files
# Note: We run this during build to ensure static files are ready
# but usually it's better to run it at startup or via a separate command
# if the settings depend on environment variables.
# For now, we'll assume production settings are available.
# ENV DJANGO_SETTINGS_MODULE=core.settings.prod
# RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]
