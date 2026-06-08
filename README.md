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

## Docker / Home Server (Portainer on Ugreen NAS)

### Option A — Portainer Stack (recommended)

1. In Portainer, go to **Stacks → Add stack**
2. Name it `lutheran-lectionary`
3. Paste this into the Web editor:

```yaml
services:
  lutheran-lectionary:
    image: ghcr.io/abc3-mac/lutheran-lectionary:latest
    container_name: lutheran-lectionary
    restart: unless-stopped
    ports:
      - "5765:5765"
    environment:
      - FLASK_ENV=production
```

4. Click **Deploy the stack**
5. Open `http://<your-nas-ip>:5765` in your browser

### Option B — Build from source

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
