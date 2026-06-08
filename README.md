# Lutheran Lectionary — LCMS Liturgical Calendar

A Flask web app providing a complete liturgical calendar for **LCMS Lutherans** following the **Lutheran Service Book (LSB)**.

## Features

- **Two lectionary series**: Three-Year (A/B/C) and One-Year Historic
- **Full-year calendar view** with liturgical color coding
- **Date lookup** — find the liturgical day for any date (1583–2299)
- **File naming utility** — generates `yyyy-mm-dd Sunday Name` labels for sermon/recording files
- **PDF export** — landscape calendar matching LCMS Church Year Calendar format
- **Scripture popups** — click any reading to see ESV text via the ESV API
- **Minor feasts toggle** — show principal feasts only, or include sanctoral calendar
- Readings sourced from the official **LSB Propers of the Day** (CPH, 2007)

## Screenshots

_Coming soon_

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

### Putting it behind a reverse proxy (Nginx Proxy Manager, Caddy, Traefik, etc.)

The container serves plain HTTP on port 5765. Your reverse proxy handles TLS termination.

**Nginx Proxy Manager example:**

| Field | Value |
|-------|-------|
| Scheme | `http` |
| Forward Hostname / IP | your server IP, or the container name if on a shared Docker network |
| Forward Port | `5765` |
| SSL | Request a Let's Encrypt certificate, Force SSL, HTTP/2 on |
| Block Common Exploits | On |

**Shared Docker network (optional):** If NPM runs in Docker on the same host, you can
put both containers on a shared network so NPM can reach the app by container name
instead of IP:

```yaml
services:
  lutheran-lectionary:
    image: ghcr.io/abc3-mac/lutheran-lectionary:latest
    container_name: lutheran-lectionary
    restart: unless-stopped
    ports:
      - "5765:5765"
    environment:
      FLASK_ENV: production
    networks:
      - proxy_network   # replace with your NPM network name

networks:
  proxy_network:
    external: true
```

Then set the Forward Hostname in NPM to `lutheran-lectionary` (the container name).

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

## License

MIT — free for personal, parish, and educational use.

---

Albert Bernard Collver III, Ph.D.
