# ---------------------------------------------
# Agent Dockerfile
#
# Environment variables:
#   BACKEND_URL    – URL to backend API (default: http://localhost:8080)
#   SCAN_INTERVAL  – Scan interval in seconds (default: 60)
# ---------------------------------------------


FROM python:3.13-alpine

WORKDIR /app
COPY . .

# Install tools 
RUN apk add --no-cache wireless-tools iproute2 net-tools bash

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
