FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the backend code
COPY . /app/

# Start Gunicorn server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
