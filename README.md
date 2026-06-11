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
- **One-Year propers** — every Sunday in the One-Year series displays its introit (Latin name + Psalm reference) and Collect of the Day (TLH 1941, public domain) inline in the calendar via click-to-expand, and on a dedicated printable `/propers` page
- **iCal export** — download a `.ics` file for any church year, or subscribe via `webcal://` for a live feed that auto-updates in Apple Calendar, Google Calendar, or Outlook
- **PDF export** — landscape calendar matching LCMS Church Year Calendar format
- **Scripture popups** — click any reading to see ESV text via the ESV API
- **Minor feasts toggle** — show principal feasts only, or include sanctoral calendar
- **Daily lectionary** — the LSB Daily Lectionary's two readings per day (Old + New Testament) appear on the home page Today card, in every date lookup, and in the JSON API; fixed civil dates for the Christmas/Church cycles, movable Ash Wednesday→Trinity readings for the Easter cycle, exactly as appointed. A full-year chart at `/daily` can be browsed, printed, or downloaded as PDF
- **Settings page** — one place (⚙ in the nav) for all preferences: lectionary series, Advent color (contemporary blue vs. historic violet for the One-Year series), light/dark/system theme, minor feasts default, and scripture translation (ESV or KJV) for popups and links. Everything is stored in the browser — no account, no server state
- **Search** — find Sundays and feasts by name, Latin introit title, or Scripture reference ("Cantate", "Trinity", "Luke 15")
- **Permalinks** — every date has a shareable URL (`/day/2026-06-07`) with Open Graph tags for clean unfurls on social media; a "Copy permalink" button appears on lookup results
- **Dark mode** — 🌙 toggle in the header, remembered across visits
- **JSON API** — `/api/calendar/<year>` and `/api/day/<date>` for parish websites and bulletin tools (see below)
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
# Open http://localhost:5765
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

## JSON API

Two read-only endpoints for integrating the calendar into parish websites, bulletin generators, or other tools:

```
GET /api/calendar/<year>?lectionary=three_year|one_year&minor=0|1
GET /api/day/<YYYY-MM-DD>?lectionary=three_year|one_year
```

Examples:

```bash
# Full 2025–2026 church year, one-year series
curl https://lectionary.collver.biz/api/calendar/2025?lectionary=one_year

# A single date
curl https://lectionary.collver.biz/api/day/2026-06-07?lectionary=one_year
```

`<year>` is the church year's starting (Advent) year. Responses include the day's name, season, liturgical color, readings, and — for the One-Year series — introit and collect.

## Development

```bash
pip install -r requirements.txt pytest
python -m pytest tests/    # regression suite: computus, Advent, Trinity numbering, link cleaning, routes
python app.py              # serves on http://127.0.0.1:5765 via waitress
```

Tests run automatically in CI on every push; the Docker image is only built and published if they pass.

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
- **Lutheran One-Year expanded** ✅ — collects (TLH 1941) and introits for all 76 One-Year Sundays, inline in calendar and on a printable `/propers` page
- **iCal / webcal export** ✅ — live subscription feed for Apple Calendar, Google Calendar, Outlook
- **Trinity Sunday ordinal fix** ✅ — corrected off-by-one in Trinity season numbering; "First Sunday after Trinity" now correctly assigned to the Sunday immediately following Trinity Sunday
- **Mobile-responsive calendar** ✅ — portrait view shows Date + Festival/Sunday only (no truncation); rotate to landscape to see all readings (First Reading, Psalm, Epistle, Gospel); works on Safari, Chrome, and Brave on iOS
- **Bible Gateway link sanitization** ✅ — scripture links now strip liturgical annotations (antiphons, procession notes) and convert optional parenthesized verse ranges to comma-separated ranges so every reading loads correctly on Bible Gateway (~30% of links were previously broken) — thanks to [@TomaceGordon](https://github.com/TomaceGordon) for the contribution!

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
