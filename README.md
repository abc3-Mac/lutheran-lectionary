# Lutheran Lectionary — LCMS Liturgical Calendar

A Flask web app providing a complete liturgical calendar for **LCMS Lutherans** following the **Lutheran Service Book (LSB)**.

## Features

- **Timezone-aware**: "Today" is determined from the user's browser, so the correct date is shown regardless of where the server is hosted. Falls back to server UTC if JavaScript is unavailable.
- **Two lectionary series**: Three-Year (A/B/C) and One-Year Historic — with full One-Year support: Gesima Sundays (Septuagesima, Sexagesima, Quinquagesima), correct Transfiguration placement (Sunday before Septuagesima), and "N Sunday after Trinity" naming throughout the season after Pentecost
- **Remembered preference** — lectionary choice is saved in `localStorage` so every page (including the Today card) reflects your last selection; no server session or login required
- **Full-year calendar view** with liturgical color coding
- **Date lookup** — find the liturgical day for any date (1583–2299); weekdays show their governing Sunday's name ("Week of Second Sunday after Trinity") with the appointed readings
- **Minor feast detection** — weekday lookups also surface any sanctoral observance for that date (e.g. "Also today: St. Barnabas, Apostle")
- **File naming utility** — generates `yyyy-mm-dd Sunday Name` labels for sermon/recording files
- **PDF export** — landscape calendar matching LCMS Church Year Calendar format
- **Scripture popups** — click any reading to see ESV text via the ESV API
- **Minor feasts toggle** — show principal feasts only, or include sanctoral calendar
- Readings sourced from the official **LSB Propers of the Day** (CPH, 2007)

## Live Demo

You can see it running at **[lectionary.collver.biz](https://lectionary.collver.biz)**

## Screenshots

![Live site](screenshots/live-site.png)

## Quick Start (Mac/Linux)

```bash
git clone https://github.com/abc3-Mac/lutheran-lectionary
cd lutheran-lectionary
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## Docker / Home Server

### Quick start

```bash
docker run -d --restart unless-stopped -p 5765:5765 \
  ghcr.io/abc3-mac/lutheran-lectionary:latest
```

Then open `http://localhost:5765` (or replace `localhost` with your server's IP).

### Portainer stack

In Portainer go to **Stacks → Add stack**, paste the contents of
[`docker-compose.yml`](docker-compose.yml), and click **Deploy the stack**.

The included `docker-compose.yml` exposes port `5765` and is ready to use as-is.

### Putting it behind Nginx (with HTTPS)

The container serves plain HTTP on port 5765. Nginx handles TLS termination.

**1. Get a certificate with Certbot:**

```bash
certbot certonly --nginx -d lectionary.example.com
```

**2. Nginx site config** (`/etc/nginx/sites-available/lutheran-lectionary`):

```nginx
server {
    listen 80;
    server_name lectionary.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name lectionary.example.com;

    ssl_certificate     /etc/letsencrypt/live/lectionary.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lectionary.example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass         http://127.0.0.1:5765;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

**3. Enable and reload:**

```bash
ln -s /etc/nginx/sites-available/lutheran-lectionary /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### Putting it behind Nginx Proxy Manager or Traefik

The container serves plain HTTP on port 5765 — point your proxy at
`http://<host-ip>:5765` or, if on a shared Docker network, at the container name.
Enable SSL/TLS termination at the proxy layer.

### Build from source

```bash
git clone https://github.com/abc3-Mac/lutheran-lectionary
cd lutheran-lectionary
docker build -t lutheran-lectionary .
docker run -d --restart unless-stopped -p 5765:5765 lutheran-lectionary
```

## Lectionary Data

All readings are extracted from the **LSB Propers of the Day** (Concordia Publishing House, 2007):

- **Three-Year Series**: 77 Sunday/feast slots × 3 series (A/B/C) = 231 reading sets
- **One-Year Series**: 119 slots including Sundays after Trinity, pre-Lent Sundays, and the full sanctoral calendar

Psalm references include antiphon notations. "Or" alternatives are preserved exactly as printed in the LSB.

## Series Cycle

| Church Year | Series |
|-------------|--------|
| 2025–2026   | A      |
| 2026–2027   | B      |
| 2027–2028   | C      |

## Roadmap

- **Docker container** — home server deployment with a single `docker run` command
- **Roman Catholic** — Roman Rite lectionary (Ordinary Form, 3-year cycle)
- **Anglican / Episcopal** — Revised Common Lectionary as used in the Episcopal Church and Anglican Communion
- **Eastern Orthodox** — Byzantine lectionary (Epistle and Gospel pericopes)
- **Lutheran One-Year expanded** — full sanctoral calendar with collect and introit text

## Analytics (Umami)

The app has a built-in hook for [Umami](https://umami.is) analytics. No tracking code is stored in the repository — you supply it via environment variables at deploy time.

Add these to your Portainer stack or `docker-compose.yml`:

```yaml
environment:
  FLASK_ENV: production
  UMAMI_SCRIPT_URL: https://analytics.example.com/script.js
  UMAMI_WEBSITE_ID: your-website-id-here
```

If either variable is absent the script tag is simply not rendered, so the app works fine without it.

## License

MIT — free for personal, parish, and educational use.

---

Albert Bernard Collver III, Ph.D.
