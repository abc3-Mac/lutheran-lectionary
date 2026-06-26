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
from liturgical_calendar.data.hymn_of_the_day import hymn_of_the_day
from liturgical_calendar.data.civil_holidays import civil_holidays_for
from liturgical_calendar.utils import parse_readings, file_label, season_color_class, bg_url

app = Flask(__name__, template_folder=os.path.join(_HERE, "templates"),
            static_folder=os.path.join(_HERE, "static"))
app.jinja_env.globals.update(enumerate=enumerate, bg_url=bg_url)


def _read_version() -> str:
    """Running version string for the update banner / footer.

    Resolution order:
      1. APP_VERSION env var (set at Docker build time from the git tag).
      2. A VERSION file next to app.py (build-time fallback).
      3. "dev" when running from a source checkout with neither set.
    """
    env = os.environ.get("APP_VERSION", "").strip()
    if env:
        return env
    try:
        with open(os.path.join(_HERE, "VERSION"), "r", encoding="utf-8") as fh:
            v = fh.read().strip()
            if v:
                return v
    except OSError:
        pass
    return "dev"


APP_VERSION = _read_version()


@app.context_processor
def inject_version():
    return {"app_version": APP_VERSION}

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
        ev["hymn"] = hymn_of_the_day(ev["slot"], lectionary, ev.get("series"))
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
            "collect":       mf.get("collect"),
            "introit_text":  mf.get("introit_text"),
            "gradual":       mf.get("gradual"),
            "source":        mf.get("source"),
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
        "civil_holidays":  civil_holidays_for(d),
        "collect":         info.get("collect"),
        "introit":         info.get("introit"),
        "gradual":         info.get("gradual"),
        "source":          info.get("source"),
        "daily":           _daily_for_display(d),
        "hymn_of_the_day": hymn_of_the_day(slot, lectionary, info.get("series")),
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


@app.route("/day/<date_str>/pdf")
def day_pdf(date_str):
    """One-page printable propers sheet for a single date."""
    lectionary = request.args.get("lectionary", "three_year")
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(404)
    result, error = _lookup_result(d, lectionary)
    if result is None:
        abort(404)
    violet = request.args.get("historic", "1") != "0"   # one-year Advent color pref
    if request.args.get("style") == "document":
        from pdf_gen import build_day_pdf
        buf = build_day_pdf(result, lectionary, violet_advent=violet)
        style_tag = "_print"
    else:
        from pdf_gen import build_day_card_pdf   # card is the default style
        buf = build_day_card_pdf(result, lectionary, violet_advent=violet)
        style_tag = ""
    lect_tag = "1yr" if lectionary == "one_year" else "3yr"
    filename = f"Propers_{date_str}_{lect_tag}{style_tag}.pdf"
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


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


@app.route("/api/version")
def api_version():
    """Running version, used by the client to check for newer releases."""
    return jsonify({"version": APP_VERSION})


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
        "civil_holidays": civil_holidays_for(today),
        "daily":        _daily_for_display(today),
        "hymn_of_the_day": hymn_of_the_day(info["slot"], lectionary, info.get("series")),
    })


def _propers_sections(advent_year: int):
    """One-year Sundays and feast days with propers, grouped by season."""
    from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
    cal    = get_calendar(advent_year)
    events = cal.all_events(include_minor=False, lectionary='one_year')
    entries = [
        ev for ev in events
        if (ev.get("is_sunday") or ev.get("is_feast"))
        and (ev.get("collect") or ev.get("introit"))
    ]
    for ev in entries:
        ev["color_class"] = season_color_class(ev.get("color", "Green"))
        ev["date_str"]    = ev["date"].strftime("%A, %B %-d, %Y")
        # all_events()/slot_info() return THREE-year readings for slots shared by
        # both series; use the One-Year pericopes here (as the calendar/lookup do).
        slot_data = ONE_YEAR_SLOTS.get(ev["slot"])
        readings_raw = slot_data.get("readings") if slot_data else ev.get("readings")
        ev["readings_parsed"] = parse_readings(readings_raw)
    sections = _group_by_season(entries)

    # Principal fixed-date festivals carry their own One-Year propers but aren't
    # emitted as standalone events by all_events() — append them as a Festivals
    # section rather than fragmenting the Trinity sequence.
    from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS
    festival_dates = [
        ("st_michael",   date(cal.civil_year, 9, 29)),
        ("reformation",  cal.reformation_day),
        ("all_saints",   cal.all_saints_day),
        ("thanksgiving", cal.thanksgiving),
    ]
    festivals = []
    for slot, d in festival_dates:
        sd = ONE_YEAR_SLOTS.get(slot)
        p  = ONE_YEAR_PROPERS.get(slot, {})
        if not sd or not (p.get("collect") or p.get("introit")):
            continue
        festivals.append({
            "date":            d,
            "slot":            slot,
            "name":            sd["name"],
            "color_class":     season_color_class(sd.get("color", "White")),
            "date_str":        d.strftime("%B %-d"),
            "collect":         p.get("collect"),
            "introit":         p.get("introit"),
            "gradual":         p.get("gradual"),
            "source":          p.get("source"),
            "readings_parsed": parse_readings(sd.get("readings")),
        })
    if festivals:
        festivals.sort(key=lambda e: (e["date"].month, e["date"].day))
        sections.append({"season": "Festivals", "events": festivals})
    return sections


@app.route("/propers")
def propers():
    """One-year propers reference page — all Sundays with introit + collect."""
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))
    sections = _propers_sections(advent_year)

    return render_template(
        "propers.html",
        advent_year=advent_year,
        sections=sections,
        min_year=MIN_YEAR,
        max_year=MAX_YEAR,
        series_choices=SERIES_CHOICES,
        lectionary="one_year",
    )


@app.route("/propers/pdf")
def propers_pdf():
    """Printable PDF of the one-year propers (introit + collect per Sunday)."""
    try:
        advent_year = int(request.args.get("year", date.today().year))
    except ValueError:
        advent_year = date.today().year
    advent_year = max(MIN_YEAR, min(MAX_YEAR, advent_year))
    sections = _propers_sections(advent_year)

    from pdf_gen import build_propers_pdf
    violet = request.args.get("historic", "1") != "0"   # Advent color pref
    buf = build_propers_pdf(advent_year, sections, violet_advent=violet)
    filename = f"One_Year_Propers_{advent_year}-{advent_year+1}.pdf"
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name=filename)


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


@app.route("/about")
def about():
    """History, sources, and copyright/permissions statement."""
    return render_template("about.html")


@app.route("/settings")
def settings():
    """Browser-stored preferences page (no server state)."""
    return render_template("settings.html",
                           min_year=MIN_YEAR, max_year=MAX_YEAR,
                           series_choices=SERIES_CHOICES)


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
    lectionary    = request.args.get("lectionary", "three_year")
    include_daily = request.args.get("daily", "0") == "1"
    include_civil = request.args.get("civil", "0") == "1"

    ics_bytes = build_ical_year(advent_year, lectionary,
                                include_daily=include_daily,
                                include_civil=include_civil)
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
    lectionary    = request.args.get("lectionary", "three_year")
    include_daily = request.args.get("daily", "0") == "1"
    include_civil = request.args.get("civil", "0") == "1"
    ics_bytes  = build_ical_subscription(lectionary, include_daily=include_daily,
                                         include_civil=include_civil)
    response   = app.response_class(
        ics_bytes,
        mimetype="text/calendar; charset=utf-8",
    )
    # Tell calendar clients to refresh daily
    response.headers["Content-Disposition"] = "inline"
    response.headers["Cache-Control"] = "no-cache, max-age=86400"
    return response


# ---------------------------------------------------------------------------
# Almanac — calendar and lunar utilities
# ---------------------------------------------------------------------------

ALMANAC_MIN_YEAR = 30      # back to apostolic times (Julian calendar)
ALMANAC_MAX_YEAR = 2200

_MONTHS = ["", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]


def _fmt_date(d, julian: bool, with_year: bool = False, with_weekday: bool = True):
    """Format a (proleptic-Gregorian) date in the era-appropriate calendar."""
    from liturgical_calendar.almanac.convert import gregorian_to_julian
    if julian:
        y, m, day = gregorian_to_julian(d)
    else:
        y, m, day = d.year, d.month, d.day
    wd = d.strftime("%a") + ", " if with_weekday else ""
    yr = f", {y}" if with_year else ""
    return f"{wd}{_MONTHS[m]} {day}{yr}"


@app.route("/almanac")
def almanac():
    """Hub page linking the calendar/lunar tools."""
    return render_template("almanac.html", year=date.today().year)


@app.route("/almanac/moon")
def almanac_moon():
    """Moon phases for a year: full/new lists, blue moons, and the
    ecclesiastical-vs-astronomical comparison behind the date of Easter.

    Works back to apostolic times: before the 1582 reform, dates are shown on
    the Julian calendar and the astronomical positions are approximate (the
    lunar series drifts ~a day across two millennia)."""
    from liturgical_calendar.almanac import moon, computus
    from liturgical_calendar.almanac.icons import phase_icon, moon_svg
    from markupsafe import Markup

    try:
        year = int(request.args.get("year", date.today().year))
    except ValueError:
        year = date.today().year
    year = max(ALMANAC_MIN_YEAR, min(ALMANAC_MAX_YEAR, year))
    julian = year < computus.GREGORIAN_START_YEAR

    events = []
    for p in moon.phases_in_range(date(year, 1, 1), date(year, 12, 31)):
        events.append({
            "phase":   p.phase,
            "icon":    Markup(phase_icon(p.phase, size=30)),
            "date":    _fmt_date(p.dt.date(), julian),
            "time":    p.dt.strftime("%H:%M") + " UT",
        })

    blue = []
    for b in moon.blue_moons(year):
        blue.append({
            "kind": b["kind"],
            "date": _fmt_date(b["date"], julian, with_weekday=False),
            "season": b.get("season", ""),
        })

    cmp = computus.easter_moon_comparison(year)
    comparison = {
        "golden_number":   cmp["golden_number"],
        "eccl_equinox":    _fmt_date(cmp["ecclesiastical_equinox"], julian, with_weekday=False),
        "eccl_full_moon":  _fmt_date(cmp["ecclesiastical_full_moon"], julian, with_weekday=False),
        "astro_full_moon": _fmt_date(cmp["astronomical_full_moon"], julian, with_weekday=False),
        "astro_time":      cmp["astronomical_full_moon_ut"].strftime("%H:%M UT"),
        "delta_days":      cmp["delta_days"],
        "easter":          _fmt_date(cmp["easter"], julian, with_year=True, with_weekday=False),
        "full_icon":       Markup(moon_svg(1.0, True, size=30, label="Full moon")),
    }

    return render_template(
        "almanac_moon.html",
        year=year,
        julian=julian,
        before_nicaea=cmp["before_nicaea"],
        events=events,
        full_count=sum(1 for e in events if e["phase"] == moon.FULL_MOON),
        new_count=sum(1 for e in events if e["phase"] == moon.NEW_MOON),
        blue_moons=blue,
        comparison=comparison,
        min_year=ALMANAC_MIN_YEAR,
        max_year=ALMANAC_MAX_YEAR,
        prev_year=max(ALMANAC_MIN_YEAR, year - 1),
        next_year=min(ALMANAC_MAX_YEAR, year + 1),
    )


@app.route("/almanac/easter")
def almanac_easter():
    """Date of Easter and the movable feasts over a year range.

    Three modes: 'compare' (Western vs Eastern, with the gap in days),
    'western', and 'eastern' (a full movable-feast table for one tradition).
    Pre-1583 rows are shown on the Julian calendar."""
    from datetime import timedelta
    from liturgical_calendar.almanac import computus

    mode = request.args.get("mode", "compare")
    if mode not in ("compare", "western", "eastern"):
        mode = "compare"

    def _int(name, default):
        try:
            return int(request.args.get(name, default))
        except ValueError:
            return default

    start = _int("start", date.today().year)
    end = _int("end", start + 24)
    start = max(ALMANAC_MIN_YEAR, min(ALMANAC_MAX_YEAR, start))
    end = max(ALMANAC_MIN_YEAR, min(ALMANAC_MAX_YEAR, end))
    if end < start:
        start, end = end, start
    if end - start > 199:                    # keep the table bounded
        end = start + 199

    # The movable feasts to show in single-tradition mode, in liturgical order.
    feast_cols = [
        ("Septuagesima", "septuagesima"), ("Ash Wednesday", "ash_wednesday"),
        ("Easter", "easter"), ("Ascension", "ascension"),
        ("Pentecost", "pentecost"), ("Trinity", "trinity"),
    ]

    rows = []
    coincidences = 0
    if mode == "compare":
        for y in range(start, end + 1):
            julian = y < computus.GREGORIAN_START_YEAR
            east = computus.orthodox_easter(y)
            west = east if julian else computus.gregorian_easter(y)
            gap = (east - west).days
            if gap == 0:
                coincidences += 1
            rows.append({
                "year": y,
                "western": _fmt_date(west, julian, with_weekday=False),
                "eastern": _fmt_date(east, julian, with_weekday=False),
                "gap": gap,
                "same": gap == 0,
            })
    else:
        for y in range(start, end + 1):
            julian = y < computus.GREGORIAN_START_YEAR
            if mode == "eastern" or julian:
                base = computus.orthodox_easter(y)
            else:
                base = computus.gregorian_easter(y)
            cells = [_fmt_date(base + timedelta(days=computus.MOVABLE_OFFSETS[key]),
                               julian, with_weekday=False)
                     for _, key in feast_cols]
            rows.append({"year": y, "cells": cells})

    return render_template(
        "almanac_easter.html",
        mode=mode,
        start=start,
        end=end,
        rows=rows,
        feast_headers=[label for label, _ in feast_cols],
        coincidences=coincidences,
        spans_julian=start < computus.GREGORIAN_START_YEAR,
        min_year=ALMANAC_MIN_YEAR,
        max_year=ALMANAC_MAX_YEAR,
    )


ALMANAC_PASSOVER_MIN = -1499      # 1500 BC — the calculator's floor
ALMANAC_PASSOVER_MAX = 2200


def _astro_year(num: int, era: str) -> int:
    """(number, 'BC'|'AD') -> astronomical year numbering (0 = 1 BC)."""
    return num if era == "AD" else 1 - num


def _year_label(astro: int) -> str:
    return f"AD {astro}" if astro > 0 else f"{1 - astro} BC"


@app.route("/almanac/passover")
def almanac_passover():
    """Astronomical Passover (the spring / Paschal full moon) reconstructed from
    the Exodus era to the present. The Hebrew calendar was observational, so this
    is an astronomical reconstruction, not a calendar record."""
    from liturgical_calendar.almanac import moon

    def _int(name, default):
        try:
            return int(request.args.get(name, default))
        except (ValueError, TypeError):
            return default

    s_era = request.args.get("s_era", "BC")
    e_era = request.args.get("e_era", "BC")
    s_era = s_era if s_era in ("BC", "AD") else "BC"
    e_era = e_era if e_era in ("BC", "AD") else "BC"
    s_num = _int("s_num", 1446)        # default: a classic early-Exodus date
    e_num = _int("e_num", 1400)

    start = _astro_year(s_num, s_era)
    end = _astro_year(e_num, e_era)
    start = max(ALMANAC_PASSOVER_MIN, min(ALMANAC_PASSOVER_MAX, start))
    end = max(ALMANAC_PASSOVER_MIN, min(ALMANAC_PASSOVER_MAX, end))
    if end < start:
        start, end = end, start
    if end - start > 199:
        end = start + 199

    rows = []
    for y in range(start, end + 1):
        m = moon.spring_full_moon(y)
        gy, gm, gd = m["gregorian"]
        jy, jm, jd = m["julian"]
        rows.append({
            "year": _year_label(y),
            "weekday": m["weekday"],
            "gregorian": f"{_MONTHS[gm]} {gd}",
            "julian": f"{_MONTHS[jm]} {jd}",
            "time": f"{m['hour']:02d}:{m['minute']:02d} UT",
        })

    return render_template(
        "almanac_passover.html",
        rows=rows,
        s_num=s_num, s_era=s_era, e_num=e_num, e_era=e_era,
        count=len(rows),
    )


@app.route("/almanac/easter-stats")
def almanac_easter_stats():
    """Statistics on the date of Easter over a year range: earliest, latest,
    the full distribution, and how often West and East coincide."""
    from liturgical_calendar.almanac import computus

    def _int(name, default):
        try:
            return int(request.args.get(name, default))
        except (ValueError, TypeError):
            return default

    tradition = request.args.get("tradition", "western")
    if tradition not in ("western", "eastern"):
        tradition = "western"
    # Gregorian computus only makes sense from 1583; default to a long window.
    start = max(1583, _int("start", 1583))
    end = _int("end", 2582)
    end = max(start, min(start + 1999, end))            # cap 2000 years

    fn = computus.orthodox_easter if tradition == "eastern" else computus.gregorian_easter
    counts = {}                                          # (month, day) -> count
    earliest = latest = None
    coincidences = 0
    for y in range(start, end + 1):
        e = fn(y)
        key = (e.month, e.day)
        counts[key] = counts.get(key, 0) + 1
        if earliest is None or (e.month, e.day) < earliest[0]:
            earliest = ((e.month, e.day), y)
        if latest is None or (e.month, e.day) > latest[0]:
            latest = ((e.month, e.day), y)
        if computus.gregorian_easter(y) == computus.orthodox_easter(y):
            coincidences += 1

    total = end - start + 1
    peak = max(counts.values())
    dist = []
    for key in sorted(counts):
        m, d = key
        dist.append({
            "label": f"{_MONTHS[m][:3]} {d}",
            "count": counts[key],
            "pct": round(100 * counts[key] / total, 1),
            "bar": round(100 * counts[key] / peak),       # bar width %
        })
    most_common = max(counts, key=counts.get)

    return render_template(
        "almanac_stats.html",
        tradition=tradition, start=start, end=end, total=total,
        earliest={"date": f"{_MONTHS[earliest[0][0]]} {earliest[0][1]}", "year": earliest[1]},
        latest={"date": f"{_MONTHS[latest[0][0]]} {latest[0][1]}", "year": latest[1]},
        most_common=f"{_MONTHS[most_common[0]]} {most_common[1]}",
        most_common_count=counts[most_common],
        coincidences=coincidences,
        dist=dist,
    )


@app.route("/almanac/convert")
def almanac_convert():
    """Convert a date between the Julian and Gregorian calendars, with the
    Julian Day number and weekday. Works for BC years (astronomical numbering)."""
    import math
    from liturgical_calendar.almanac import convert as cv

    result = error = None
    src = request.args.get("src", "gregorian")
    if src not in ("gregorian", "julian"):
        src = "gregorian"
    y = request.args.get("year")
    m = request.args.get("month")
    d = request.args.get("day")
    if y is not None and m is not None and d is not None:
        try:
            yi, mi, di = int(y), int(m), int(d)
            if not (1 <= mi <= 12 and 1 <= di <= 31):
                raise ValueError
            jd = (cv.julian_to_jd(yi, mi, di) if src == "julian"
                  else cv.gregorian_to_jd(yi, mi, di))
            gy, gm, gd = cv.jd_to_gregorian(jd)
            jy, jm, jd_ = cv.jd_to_julian(jd)
            wd = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday"][int(math.floor(jd + 1.5)) % 7]
            result = {
                "weekday": wd,
                "gregorian": f"{_MONTHS[gm]} {int(gd)}, {_year_label(gy)}",
                "julian": f"{_MONTHS[jm]} {int(jd_)}, {_year_label(jy)}",
                "jdn": int(jd + 0.5),
            }
        except (ValueError, TypeError):
            error = "Enter a valid date (month 1–12, day 1–31)."

    return render_template("almanac_convert.html",
                           src=src, year=y or "", month=m or "", day=d or "",
                           result=result, error=error)


@app.route("/almanac/help")
def almanac_help():
    """Help & guide: how the tools work and why Easter is hard to calculate."""
    return render_template("almanac_help.html")


@app.route("/almanac/feasts")
def almanac_feasts():
    """All movable feasts for a single year, Western and Eastern."""
    from datetime import timedelta
    from liturgical_calendar.almanac import computus

    try:
        year = int(request.args.get("year", date.today().year))
    except ValueError:
        year = date.today().year
    year = max(ALMANAC_MIN_YEAR, min(ALMANAC_MAX_YEAR, year))
    julian = year < computus.GREGORIAN_START_YEAR

    order = ["septuagesima", "sexagesima", "quinquagesima", "ash_wednesday",
             "lent_1", "palm_sunday", "maundy_thursday", "good_friday",
             "holy_saturday", "easter", "ascension", "pentecost", "trinity",
             "corpus_christi"]
    labels = {
        "septuagesima": "Septuagesima", "sexagesima": "Sexagesima",
        "quinquagesima": "Quinquagesima", "ash_wednesday": "Ash Wednesday",
        "lent_1": "First Sunday in Lent", "palm_sunday": "Palm Sunday",
        "maundy_thursday": "Maundy Thursday", "good_friday": "Good Friday",
        "holy_saturday": "Holy Saturday", "easter": "Easter Day",
        "ascension": "Ascension", "pentecost": "Pentecost",
        "trinity": "Holy Trinity", "corpus_christi": "Corpus Christi",
    }
    west_base = computus.orthodox_easter(year) if julian else computus.gregorian_easter(year)
    east_base = computus.orthodox_easter(year)
    rows = []
    for key in order:
        off = computus.MOVABLE_OFFSETS[key]
        rows.append({
            "name": labels[key],
            "western": _fmt_date(west_base + timedelta(days=off), julian, with_weekday=False),
            "eastern": _fmt_date(east_base + timedelta(days=off), julian, with_weekday=False),
        })

    return render_template("almanac_feasts.html", year=year, rows=rows,
                           julian=julian, same=(west_base == east_base),
                           prev_year=max(ALMANAC_MIN_YEAR, year - 1),
                           next_year=min(ALMANAC_MAX_YEAR, year + 1),
                           min_year=ALMANAC_MIN_YEAR, max_year=ALMANAC_MAX_YEAR)


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
