# Use slim Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python exporter script
COPY process_logs.py .

# Expose Prometheus metrics port
EXPOSE 8000

# Run exporter with unbuffered output
CMD ["python", "-u", "process_logs.py"]

