"""
iCalendar (.ics) export for the LCMS Liturgical Calendar.

Produces RFC 5545-compliant VCALENDAR output.  Each liturgical Sunday and
principal feast becomes an all-day VEVENT with:
  - SUMMARY  = liturgical name
  - DESCRIPTION = appointed readings (comma-separated)
  - CATEGORIES = liturgical season
  - COLOR (RFC 7986) = liturgical color mapped to a CSS-named color
  - X-APPLE-CALENDAR-COLOR = same, as a hex color (Apple Calendar)
  - URL = link to the lookup page for that date

Two entry points:
  build_ical_year(advent_year, lectionary)  → bytes
      One complete church year — used for the download endpoint.

  build_ical_subscription(lectionary)       → bytes
      Rolling ~2-year window (current church year + next) — used for the
      webcal:// subscription endpoint so the feed stays perpetually current.
"""

from datetime import date, timedelta
from icalendar import Calendar, Event, vText, vDate

# ---------------------------------------------------------------------------
# Liturgical-color → hex  (Apple Calendar uses these for event colouring)
# ---------------------------------------------------------------------------
_COLOR_HEX = {
    "Blue":    "#1a4c8b",
    "White":   "#f5f5f0",
    "Red":     "#c0392b",
    "Scarlet": "#8b0000",
    "Purple":  "#6a0dad",
    "Black":   "#2c2c2c",
    "Green":   "#2e7d32",
}

# RFC 7986 COLOR property uses CSS-named colors — approximate mapping
_COLOR_CSS = {
    "Blue":    "blue",
    "White":   "white",
    "Red":     "red",
    "Scarlet": "darkred",
    "Purple":  "purple",
    "Black":   "black",
    "Green":   "green",
}

# Base URL for reading links — can be overridden by callers
_BASE_URL = "https://lectionary.collver.biz"


_READING_LABELS = {"ot": "First Reading", "ps": "Psalm", "ep": "Epistle", "go": "Gospel"}


def _readings_str(readings) -> str:
    """Format readings list/dict as a human-readable string."""
    if not readings:
        return ""
    if isinstance(readings, list):
        return ", ".join(str(r) for r in readings)
    if isinstance(readings, dict):
        parts = []
        for label, refs in readings.items():
            label = _READING_LABELS.get(label, label)
            if isinstance(refs, list):
                parts.append(f"{label}: {', '.join(str(r) for r in refs)}")
            else:
                parts.append(f"{label}: {refs}")
        return "\n".join(parts)
    return str(readings)


def _make_calendar(name: str, description: str, lectionary: str) -> Calendar:
    cal = Calendar()
    cal.add("PRODID", "-//Albert Collver//LCMS Lutheran Lectionary//EN")
    cal.add("VERSION", "2.0")
    cal.add("CALSCALE", "GREGORIAN")
    cal.add("METHOD", "PUBLISH")
    cal.add("X-WR-CALNAME", vText(name))
    cal.add("X-WR-CALDESC", vText(description))
    cal.add("X-WR-TIMEZONE", "UTC")
    # RFC 7986 color for the whole calendar
    series_color = "#1a4c8b" if lectionary == "three_year" else "#6a0dad"
    cal.add("COLOR", vText(series_color))
    return cal


def _add_daily_events(cal: Calendar, advent_year: int, base_url: str = _BASE_URL):
    """One transparent all-day event per day with the LSB daily readings."""
    from liturgical_calendar.calculator import LiturgicalCalendar, daily_readings

    lc = LiturgicalCalendar(advent_year)
    d = lc.advent_1
    while d < lc.next_advent_1:
        entry = daily_readings(d)
        if entry:
            vevent = Event()
            vevent.add("SUMMARY", f"📖 {entry['ot']}; {entry['nt']}")
            vevent.add("DTSTART", vDate(d))
            vevent.add("DTEND", vDate(d + timedelta(1)))
            vevent.add("UID", f"{d.isoformat()}-daily@lectionary.collver.biz")
            vevent.add("DESCRIPTION",
                       f"LSB Daily Lectionary\nOld Testament: {entry['ot']}\nNew Testament: {entry['nt']}")
            vevent.add("CATEGORIES", vText("Daily Lectionary"))
            vevent.add("TRANSP", "TRANSPARENT")   # don't block busy/free time
            vevent.add("URL", f"{base_url}/day/{d.isoformat()}")
            cal.add_component(vevent)
        d += timedelta(1)


def _add_events(cal: Calendar, advent_year: int, lectionary: str,
                base_url: str = _BASE_URL):
    from liturgical_calendar.calculator import LiturgicalCalendar, daily_readings

    lc = LiturgicalCalendar(advent_year)
    events = lc.all_events(include_minor=True, lectionary=lectionary)

    # Track UIDs to avoid duplicates when building multi-year feeds
    for ev in events:
        d: date = ev["date"]
        name: str = ev["name"]
        slot: str = ev["slot"]
        color: str = ev.get("color", "Green")
        season: str = ev.get("season", "")
        readings = ev.get("readings")

        if ev.get("alt_name"):
            name = f"{name} / {ev['alt_name']}"

        vevent = Event()
        vevent.add("SUMMARY", name)
        vevent.add("DTSTART", vDate(d))
        vevent.add("DTEND", vDate(d + timedelta(1)))

        # UID must be globally unique and stable across refreshes
        lect_tag = "1yr" if lectionary == "one_year" else "3yr"
        vevent.add("UID", f"{d.isoformat()}-{slot}-{lect_tag}@lectionary.collver.biz")

        # Description: appointed readings, then propers (one-year), then daily lectionary
        desc_parts = []
        readings_str = _readings_str(readings)
        if readings_str:
            desc_parts.append(readings_str)
        intro = ev.get("introit")
        if intro:
            desc_parts.append(f"Introit: {intro['name']} — {intro['ref']}")
        if ev.get("collect"):
            desc_parts.append(f"Collect: {ev['collect']}")
        daily = daily_readings(d)
        if daily:
            desc_parts.append(f"Daily Lectionary: {daily['ot']}; {daily['nt']}")
        if desc_parts:
            vevent.add("DESCRIPTION", "\n\n".join(desc_parts))

        vevent.add("CATEGORIES", vText(season))
        vevent.add("COLOR", vText(_COLOR_CSS.get(color, "green")))
        vevent.add("X-APPLE-CALENDAR-COLOR", vText(_COLOR_HEX.get(color, "#2e7d32")))

        vevent.add("URL", f"{base_url}/day/{d.isoformat()}?lectionary={lectionary}")

        # Mark feasts as higher class
        if ev.get("is_feast"):
            vevent.add("CLASS", "PUBLIC")

        cal.add_component(vevent)


def build_ical_year(advent_year: int, lectionary: str = "three_year",
                    base_url: str = _BASE_URL, include_daily: bool = False) -> bytes:
    """
    Return a .ics byte string for one complete church year.
    Used for the download (/export/ical?year=2025&lectionary=three_year).
    include_daily adds one transparent event per day with the LSB daily readings.
    """
    lect_label = "Three-Year Series" if lectionary == "three_year" else "One-Year Historic Series"
    name = f"LCMS Liturgical Calendar {advent_year}–{advent_year+1} ({lect_label})"
    desc = (
        f"LSB {lect_label} — {advent_year}–{advent_year+1} church year. "
        "Generated by lectionary.collver.biz"
    )
    cal = _make_calendar(name, desc, lectionary)
    _add_events(cal, advent_year, lectionary, base_url)
    if include_daily:
        _add_daily_events(cal, advent_year, base_url)
    return cal.to_ical()


def build_ical_subscription(lectionary: str = "three_year",
                             base_url: str = _BASE_URL,
                             include_daily: bool = False) -> bytes:
    """
    Return a .ics byte string covering the current church year + the next one.
    Used for the webcal:// subscription endpoint — always returns fresh data
    so subscribers' calendars auto-update.
    """
    from liturgical_calendar.calculator import advent1_for_year

    today = date.today()
    current_ay = today.year if today >= advent1_for_year(today.year) else today.year - 1

    lect_label = "Three-Year Series" if lectionary == "three_year" else "One-Year Historic Series"
    name = f"LCMS Liturgical Calendar — {lect_label} (Live)"
    desc = (
        f"LSB {lect_label} — live subscription covering two church years. "
        "Refreshes automatically. Generated by lectionary.collver.biz"
    )
    cal = _make_calendar(name, desc, lectionary)
    _add_events(cal, current_ay,     lectionary, base_url)
    _add_events(cal, current_ay + 1, lectionary, base_url)
    if include_daily:
        _add_daily_events(cal, current_ay,     base_url)
        _add_daily_events(cal, current_ay + 1, base_url)
    return cal.to_ical()
