# ---------------------------------------------
# Agent Dockerfile
#
# Required environment variables (must be set):
#   BACKEND_URL    – URL to backend API
#   SCAN_INTERVAL  – Scan interval in seconds
# ---------------------------------------------

FROM python:3.13-alpine

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
