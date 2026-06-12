FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Build-time version (git tag, or a date fallback) injected by CI via
# --build-arg VERSION=...  Exposed to the app as APP_VERSION so the footer
# and the update-check banner know which release is running.
ARG VERSION=dev
ENV APP_VERSION=${VERSION}

EXPOSE 5765

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5765", "--workers", "2", "--timeout", "60", "app:app"]
