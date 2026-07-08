FROM python:3.12-slim

WORKDIR /app

# Server-side renderer for the Liturgical Year wheel PNG export (/wheel.png):
# the prebuilt resvg binary (handles <textPath>, embedded images, textLength)
# plus fonts-liberation for a Times-compatible serif (Georgia isn't on Linux).
# Pinned to a release; linux x86_64 matches the deploy target (NAS + CI).
ARG RESVG_VERSION=0.47.0
RUN apt-get update && apt-get install -y --no-install-recommends \
        fonts-liberation ca-certificates curl \
    && curl -fsSL -o /tmp/resvg.tar.gz \
        "https://github.com/linebender/resvg/releases/download/v${RESVG_VERSION}/resvg-linux-x86_64.tar.gz" \
    && tar -xzf /tmp/resvg.tar.gz -C /tmp \
    && install -m 0755 "$(find /tmp -name resvg -type f | head -1)" /usr/local/bin/resvg \
    && rm -rf /tmp/resvg.tar.gz \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

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
