# Use official Python base image
FROM python:3.10

# Disable .pyc files and enable logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Django app port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "jobportal.wsgi:application", "--bind", "0.0.0.0:8000"]
