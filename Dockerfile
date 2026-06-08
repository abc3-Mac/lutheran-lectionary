FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 5765

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5765", "--workers", "2", "--timeout", "60", "app:app"]
