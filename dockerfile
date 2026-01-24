FROM python:3.11-slim

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

CMD ["pip", "install", "prometheus_client"]

COPY metrics_exporter.py .


CMD ["python", "metrics_exporter.py"]
