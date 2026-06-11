"""
Liturgical Calendar Web Application — LCMS Lutheran Service Book
Flask web app with calendar view, date lookup, PDF export, and file naming.
"""

import os
import sys
from datetime import date, datetime, timedelta
from functools import lru_cache
from flask import Flask, render_template, request, send_file, jsonify, abort
import io

# When launched from inside a macOS .app bundle, __file__ is inside Resources/.
# Set the working directory to the folder containing app.py so that Flask can
# find templates/ and static/ via relative paths.
_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from liturgical_calendar.calculator import LiturgicalCalendar, advent1_for_year, daily_readings
from liturgical_calendar.utils import parse_readings, file_label, season_color_class, bg_url

app = Flask(__name__, template_folder=os.path.join(_HERE, "templates"),
            static_folder=os.path.join(_HERE, "static"))
app.jinja_env.globals.update(enumerate=enumerate, bg_url=bg_url)

# Umami analytics — injected via env vars so the tracking code never lives in the repo.
# Set UMAMI_SCRIPT_URL and UMAMI_WEBSITE_ID in your Docker/Portainer environment to enable.
_UMAMI_SCRIPT_URL = os.environ.get("UMAMI_SCRIPT_URL", "")
_UMAMI_WEBSITE_ID = os.environ.get("UMAMI_WEBSITE_ID", "")

@app.context_processor
def inject_umami():
    return {
        "umami_script_url": _UMAMI_SCRIPT_URL,
        "umami_website_id": _UMAMI_WEBSITE_ID,
    }

SERIES_CHOICES = [
    ("three_year", "Three-Year Series (A/B/C)"),
    ("one_year",   "One-Year (Historic) Series"),
]

MIN_YEAR = 1583
MAX_YEAR = 2299


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@lru_cache(maxsize=64)
def get_calendar(advent_year: int) -> LiturgicalCalendar:
    """Cached calendar factory — building a church year is pure computation,
    so instances are shared across requests. all_events() returns fresh dicts
    each call, so callers may safely mutate the events they receive."""
    return LiturgicalCalendar(advent_year)


def _build_year_choices():
    current = date.today().year
    years = []
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        label = f"{y}–{y+1}"
        years.append((y, label))
    return years


def _events_for_display(cal: LiturgicalCalendar, lectionary: str, include_minor: bool):
    """Return calendar events enriched with display data."""
    events = cal.all_events(include_minor=include_minor, lectionary=lectionary)
    for ev in events:
        ev["color_class"] = season_color_class(ev.get("color", "Green"))
        ev["date_str"]    = ev["date"].strftime("%b %-d, %Y")
        ev["day_of_week"] = ev["date"].strftime("%A")
        readings_raw = ev.get("readings")

        # One-Year series: readings come from one_year data
        if lectionary == "one_year":
            from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
            slot_data = ONE_YEAR_SLOTS.get(ev["slot"])
            if slot_data:
                readings_raw = slot_data.get("readings")

        ev["readings_parsed"] = parse_readings(readings_raw)
    return events


def _group_by_season(events):
    """Group a flat event list into season sections for display."""
    sections = []
    current_season = None
    current_group  = []
    for ev in events:
        s = ev.get("season", "")
        if s != current_season:
            if current_group:
                sections.append({"season": current_season, "events": current_group})
            current_season = s
            current_group  = [ev]
        else:
            current_group.append(ev)
    if current_group:
        sections.append({"season": current_season, "events": current_group})
    return sections


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    today = date.today()
    # Determine current church year
    current_advent_year = today.year if today >= advent1_for_year(today.year) else today.year - 1
    return render_template(
        "index.html",
        today=today,
        current_advent_year=current_advent_year,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
    )


@app.route("/calendar")
def calendar_view():
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year

    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))

    lectionary    = request.args.get("lectionary", "three_year")
    include_minor = request.args.get("minor", "1") == "1"

    cal    = get_calendar(advent_year)
    events = _events_for_display(cal, lectionary, include_minor)
    sections = _group_by_season(events)

    return render_template(
        "calendar.html",
        cal=cal,
        sections=sections,
        advent_year=advent_year,
        lectionary=lectionary,
        include_minor=include_minor,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
    )


def _lookup_result(d: date, lectionary: str):
    """Build the lookup display dict for a date. Returns (result, error)."""
    if d < date(MIN_YEAR, 11, 27) or d > date(MAX_YEAR + 1, 11, 26):
        return None, f"Date must be between {MIN_YEAR} and {MAX_YEAR + 1}."

    ay = d.year if d >= advent1_for_year(d.year) else d.year - 1
    cal = get_calendar(ay)
    info = cal.lookup(d, lectionary=lectionary)
    if info is None:
        return None, f"No liturgical data found for {d.strftime('%B %-d, %Y')}."

    slot = info["slot"]
    is_weekday = info.get("is_weekday", False)
    gov_date = info.get("governing_date")

    readings_raw = info.get("readings")
    if lectionary == "one_year":
        from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
        od = ONE_YEAR_SLOTS.get(slot)
        if od:
            readings_raw = od.get("readings")

    sun_name = info.get("name", slot)
    display_name = f"Week of {sun_name}" if is_weekday else sun_name

    mf = info.get("minor_feast")
    minor_feast = None
    if mf:
        minor_feast = {
            "name":          mf.get("name", ""),
            "color":         mf.get("color", ""),
            "color_class":   season_color_class(mf.get("color", "")),
            "readings_parsed": parse_readings(mf.get("readings")),
        }

    result = {
        "date":            d,
        "date_str":        d.strftime("%A, %B %-d, %Y"),
        "slot":            slot,
        "church_year":     info["church_year"],
        "series":          info["series"],
        "name":            display_name,
        "sun_name":        sun_name,
        "governing_date":  gov_date,
        "is_weekday":      is_weekday,
        "season":          info.get("season", ""),
        "color":           info.get("color", ""),
        "color_class":     season_color_class(info.get("color", "")),
        "readings_parsed": parse_readings(readings_raw),
        "file_label":      cal.file_label(gov_date or d, lectionary=lectionary),
        "minor_feast":     minor_feast,
        "collect":         info.get("collect"),
        "introit":         info.get("introit"),
        "daily":           _daily_for_display(d),
    }
    return result, None


def _daily_for_display(d: date):
    """LSB daily lectionary readings with BibleGateway links, or None."""
    entry = daily_readings(d)
    if not entry:
        return None
    return [
        {"label": "Old Testament", "ref": entry["ot"], "url": bg_url(entry["ot"])},
        {"label": "New Testament", "ref": entry["nt"], "url": bg_url(entry["nt"])},
    ]


@app.route("/lookup")
def lookup():
    date_str   = request.args.get("date", "")
    lectionary = request.args.get("lectionary", "three_year")
    result     = None
    error      = None

    if date_str:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            result, error = _lookup_result(d, lectionary)
        except ValueError:
            error = "Invalid date format. Please use YYYY-MM-DD."

    return render_template(
        "lookup.html",
        date_str=date_str,
        lectionary=lectionary,
        result=result,
        error=error,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
        today=date.today().strftime("%Y-%m-%d"),
    )


@app.route("/day/<date_str>")
def day_permalink(date_str):
    """Shareable permalink for a specific date, e.g. /day/2026-06-07."""
    lectionary = request.args.get("lectionary", "three_year")
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(404)
    result, error = _lookup_result(d, lectionary)
    if result is None:
        abort(404)
    return render_template(
        "lookup.html",
        date_str=date_str,
        lectionary=lectionary,
        result=result,
        error=error,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
        today=date.today().strftime("%Y-%m-%d"),
        permalink=True,
        og_title=f"{result['name']} — {result['date_str']}",
        og_description=f"Appointed readings and liturgical information for {result['date_str']} ({result['season']}).",
    )


@app.route("/search")
def search():
    """Search Sundays and feasts by name, Latin introit title, or reading reference."""
    q = request.args.get("q", "").strip()
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))

    results = []
    if len(q) >= 2:
        needle = q.lower()
        cal = get_calendar(advent_year)
        seen = set()
        for lectionary, lect_label in SERIES_CHOICES:
            for ev in cal.all_events(include_minor=True, lectionary=lectionary):
                hay = [ev.get("name", ""), ev.get("slot", ""), ev.get("alt_name") or ""]
                intro = ev.get("introit")
                if intro:
                    hay.append(intro.get("name", ""))
                    hay.append(intro.get("ref", ""))
                readings = ev.get("readings")
                if isinstance(readings, dict):
                    hay.extend(str(v) for v in readings.values() if v)
                if any(needle in h.lower() for h in hay):
                    key = (ev["date"], ev["name"], lectionary)
                    if key in seen:
                        continue
                    seen.add(key)
                    results.append({
                        "date":        ev["date"],
                        "date_str":    ev["date"].strftime("%a, %b %-d, %Y"),
                        "name":        ev["name"],
                        "season":      ev.get("season", ""),
                        "color_class": season_color_class(ev.get("color", "Green")),
                        "lectionary":  lectionary,
                        "lect_label":  lect_label,
                        "introit":     intro,
                    })
        results.sort(key=lambda r: (r["date"], r["lectionary"]))

    return render_template(
        "search.html",
        q=q,
        advent_year=advent_year,
        results=results,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
    )


@app.route("/pdf")
def generate_pdf():
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year

    lectionary    = request.args.get("lectionary", "three_year")
    include_minor = request.args.get("minor", "1") == "1"

    from pdf_gen import build_pdf
    cal    = get_calendar(advent_year)
    events = _events_for_display(cal, lectionary, include_minor)

    buf = build_pdf(cal, events, lectionary)
    filename = f"Liturgical_Calendar_{advent_year}-{advent_year+1}.pdf"
    return send_file(
        buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/api/today")
def api_today():
    """JSON endpoint: liturgical info for today.

    Accepts ?date=YYYY-MM-DD from the browser so the result reflects the
    user's local date rather than the server's timezone.
    """
    date_param = request.args.get("date", "")
    try:
        today = datetime.strptime(date_param, "%Y-%m-%d").date() if date_param else date.today()
    except ValueError:
        today = date.today()
    lectionary = request.args.get("lectionary", "three_year")
    ay = today.year if today >= advent1_for_year(today.year) else today.year - 1
    cal = get_calendar(ay)
    info = cal.lookup(today, lectionary=lectionary)
    if info is None:
        return jsonify({"error": "No liturgical data for today."})

    is_weekday = info.get("is_weekday", False)
    gov_date = info.get("governing_date")
    sun_name = info.get("name", "")
    # Use calendar's file_label for correct ordinal naming of Proper/Trinity Sundays
    lbl = cal.file_label(gov_date or today, lectionary=lectionary)

    display_name = f"Week of {sun_name}" if is_weekday else sun_name

    mf = info.get("minor_feast")
    minor_feast = None
    if mf:
        minor_feast = {"name": mf.get("name", ""), "color": mf.get("color", "")}

    return jsonify({
        "date":         today.isoformat(),
        "church_year":  info["church_year"],
        "series":       info["series"],
        "slot":         info["slot"],
        "name":         display_name,
        "sun_name":     sun_name,
        "is_weekday":   is_weekday,
        "season":       info.get("season"),
        "color":        info.get("color"),
        "file_label":   lbl,
        "minor_feast":  minor_feast,
        "daily":        _daily_for_display(today),
    })


@app.route("/propers")
def propers():
    """One-year propers reference page — all Sundays with introit + collect."""
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))

    cal    = get_calendar(advent_year)
    events = cal.all_events(include_minor=False, lectionary='one_year')
    # Keep only Sundays (and feasts with propers)
    sundays = [
        ev for ev in events
        if ev.get("is_sunday") and (ev.get("collect") or ev.get("introit"))
    ]
    for ev in sundays:
        ev["color_class"] = season_color_class(ev.get("color", "Green"))
        ev["date_str"]    = ev["date"].strftime("%A, %B %-d, %Y")

    # Group by season for display
    sections = []
    current_season = None
    current_group  = []
    for ev in sundays:
        s = ev.get("season", "")
        if s != current_season:
            if current_group:
                sections.append({"season": current_season, "events": current_group})
            current_season = s
            current_group  = [ev]
        else:
            current_group.append(ev)
    if current_group:
        sections.append({"season": current_season, "events": current_group})

    return render_template(
        "propers.html",
        advent_year=advent_year,
        sections=sections,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
        lectionary="one_year",
    )


def _daily_year_days(advent_year: int):
    """All daily-lectionary entries for one church year, grouped by month."""
    cal = get_calendar(advent_year)
    months = []
    current_label = None
    d = cal.advent_1
    while d < cal.next_advent_1:
        entry = daily_readings(d)
        if entry:
            label = d.strftime("%B %Y")
            if label != current_label:
                months.append({"month": label, "days": []})
                current_label = label
            months[-1]["days"].append({
                "date":     d,
                "date_str": d.strftime("%a, %b %-d"),
                "day":      entry.get("day", ""),
                "ot":       entry["ot"],
                "nt":       entry["nt"],
                "ot_url":   bg_url(entry["ot"]),
                "nt_url":   bg_url(entry["nt"]),
            })
        d += timedelta(1)
    return cal, months


@app.route("/daily")
def daily_page():
    """Full-year LSB Daily Lectionary chart."""
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))
    cal, months = _daily_year_days(advent_year)
    return render_template(
        "daily.html",
        advent_year=advent_year,
        cal=cal,
        months=months,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
    )


@app.route("/daily/pdf")
def daily_pdf():
    """Printable PDF of the full-year daily lectionary."""
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))
    cal, months = _daily_year_days(advent_year)

    from pdf_gen import build_daily_pdf
    buf = build_daily_pdf(advent_year, months)
    filename = f"LSB_Daily_Lectionary_{advent_year}-{advent_year+1}.pdf"
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


@app.route("/export/ical")
def export_ical():
    """Download a .ics file for one complete church year."""
    from liturgical_calendar.ical_export import build_ical_year
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    lectionary = request.args.get("lectionary", "three_year")

    ics_bytes = build_ical_year(advent_year, lectionary)
    lect_tag  = "3yr" if lectionary == "three_year" else "1yr"
    filename  = f"LCMS_Lectionary_{advent_year}-{advent_year+1}_{lect_tag}.ics"
    return send_file(
        io.BytesIO(ics_bytes),
        mimetype="text/calendar; charset=utf-8",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/export/ical/subscribe")
def export_ical_subscribe():
    """
    Live webcal:// subscription endpoint.
    Always returns the current + next church year so subscribers' calendars
    auto-update without re-importing.
    """
    from liturgical_calendar.ical_export import build_ical_subscription
    lectionary = request.args.get("lectionary", "three_year")
    ics_bytes  = build_ical_subscription(lectionary)
    response   = app.response_class(
        ics_bytes,
        mimetype="text/calendar; charset=utf-8",
    )
    # Tell calendar clients to refresh daily
    response.headers["Content-Disposition"] = "inline"
    response.headers["Cache-Control"] = "no-cache, max-age=86400"
    return response


# ---------------------------------------------------------------------------
# JSON API
# ---------------------------------------------------------------------------

def _event_to_json(ev: dict) -> dict:
    """Serialize an event dict for the JSON API."""
    out = dict(ev)
    out["date"] = ev["date"].isoformat()
    return out


@app.route("/api/calendar/<int:year>")
def api_calendar(year):
    """Full church year as JSON. ?lectionary=three_year|one_year &minor=0|1"""
    if not (MIN_YEAR <= year <= MAX_YEAR):
        return jsonify({"error": f"Year must be between {MIN_YEAR} and {MAX_YEAR}."}), 400
    lectionary    = request.args.get("lectionary", "three_year")
    include_minor = request.args.get("minor", "1") == "1"
    cal = get_calendar(year)
    events = cal.all_events(include_minor=include_minor, lectionary=lectionary)
    return jsonify({
        "church_year": f"{year}-{year+1}",
        "series":      cal.series,
        "lectionary":  lectionary,
        "events":      [_event_to_json(ev) for ev in events],
    })


@app.route("/api/day/<date_str>")
def api_day(date_str):
    """Liturgical info for a single date as JSON. ?lectionary=three_year|one_year"""
    lectionary = request.args.get("lectionary", "three_year")
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    result, error = _lookup_result(d, lectionary)
    if result is None:
        return jsonify({"error": error}), 404
    out = dict(result)
    out["date"] = d.isoformat()
    if out.get("governing_date"):
        out["governing_date"] = out["governing_date"].isoformat()
    return jsonify(out)


if __name__ == "__main__":
    # Local / Mac-app launch. The Docker container uses Gunicorn (see Dockerfile);
    # locally we prefer waitress (production-grade, pure Python, launchd-friendly)
    # and fall back to the Flask dev server if it isn't installed.
    try:
        from waitress import serve
        print("Serving on http://127.0.0.1:5765 (waitress)")
        serve(app, host="127.0.0.1", port=5765, threads=8)
    except ImportError:
        app.run(debug=False, port=5765)
