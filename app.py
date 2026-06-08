"""
Liturgical Calendar Web Application — LCMS Lutheran Service Book
Flask web app with calendar view, date lookup, PDF export, and file naming.
"""

import os
import sys
from datetime import date, datetime
from flask import Flask, render_template, request, send_file, jsonify, abort
import io

# When launched from inside a macOS .app bundle, __file__ is inside Resources/.
# Set the working directory to the folder containing app.py so that Flask can
# find templates/ and static/ via relative paths.
_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from liturgical_calendar.calculator import LiturgicalCalendar, advent1_for_year
from liturgical_calendar.utils import parse_readings, file_label, season_color_class, bg_url

app = Flask(__name__, template_folder=os.path.join(_HERE, "templates"),
            static_folder=os.path.join(_HERE, "static"))
app.jinja_env.globals.update(enumerate=enumerate)

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

    cal    = LiturgicalCalendar(advent_year)
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


@app.route("/lookup")
def lookup():
    date_str   = request.args.get("date", "")
    lectionary = request.args.get("lectionary", "three_year")
    result     = None
    error      = None

    if date_str:
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            if d < date(MIN_YEAR, 11, 27) or d > date(MAX_YEAR + 1, 11, 26):
                error = f"Date must be between {MIN_YEAR} and {MAX_YEAR + 1}."
            else:
                ay = d.year if d >= advent1_for_year(d.year) else d.year - 1
                cal = LiturgicalCalendar(ay)
                info = cal.lookup(d, lectionary=lectionary)
                if info is None:
                    error = f"No liturgical data found for {d.strftime('%B %-d, %Y')}."
                else:
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
                        "file_label":      file_label(gov_date or d, sun_name),
                        "minor_feast":     minor_feast,
                    }
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


@app.route("/pdf")
def generate_pdf():
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year

    lectionary    = request.args.get("lectionary", "three_year")
    include_minor = request.args.get("minor", "1") == "1"

    from pdf_gen import build_pdf
    cal    = LiturgicalCalendar(advent_year)
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
    cal = LiturgicalCalendar(ay)
    info = cal.lookup(today, lectionary=lectionary)
    if info is None:
        return jsonify({"error": "No liturgical data for today."})

    is_weekday = info.get("is_weekday", False)
    gov_date = info.get("governing_date")
    sun_name = info.get("name", "")
    # Use calendar's file_label for correct ordinal naming of Proper Sundays
    lbl = cal.file_label(gov_date or today)

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
    })


if __name__ == "__main__":
    app.run(debug=False, port=5765)
