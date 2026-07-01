"""Tests for the Historic Lent section: ferial lectionary & Passion History."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.calculator import LiturgicalCalendar
from liturgical_calendar.data import lenten_ferial as LF
from liturgical_calendar.data import passion_history as PH


# --- Lenten ferial lectionary ---------------------------------------------

def test_ferial_counts():
    days = list(LF.iter_days())
    assert len(days) == 45                      # 39 weekday ferias + 6 Sundays
    weekdays = list(LF.iter_days(include_sundays=False))
    assert len(weekdays) == 39
    assert len(LF.all_slots()) == 45            # every slot unique


def test_ferial_weekdays_resolve_correctly():
    """Every ferial day must land on the weekday its name implies."""
    cal = LiturgicalCalendar(2025)              # Lent 2026
    wd = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday",
          "thu": "Thursday", "fri": "Friday", "sat": "Saturday"}
    for _, day in LF.iter_days():
        d = LF.resolve_date(day, cal)
        if day["is_sunday"]:
            assert d.strftime("%A") == "Sunday", day["slot"]
        suffix = day["slot"].rsplit("_", 1)[-1]
        if suffix in wd:
            assert d.strftime("%A") == wd[suffix], (day["slot"], d.strftime("%A"))


def test_ferial_provenance_marks_match_source():
    """The * / ** tallies must match The Lutheran Missal's legend exactly."""
    from collections import Counter
    c = Counter()
    for _, day in LF.iter_days():
        for r in day["readings"]:
            c[r["origin"]] += 1
    assert c["lsb"] == 8      # ** LSB-not-historic
    assert c["hist"] == 8     # *  historic-not-LSB
    assert c["core"] == 92    # unmarked historic-and-LSB


def test_ferial_key_readings():
    by_slot = {day["slot"]: day for _, day in LF.iter_days()}
    # Ash Wednesday: historic Joel + Gospel, plus the ** LSB Epistle
    refs = [r["ref"] for r in by_slot["fer_ash_wed"]["readings"]]
    assert "Joel 2:12-19" in refs and "Matthew 6:16-21" in refs
    # Ember Wednesday keeps the * second lesson dropped by LSB
    ember = {r["ref"]: r["mark"] for r in by_slot["fer_ember_wed"]["readings"]}
    assert ember["1 Kings 19:3b-8"] == "*"
    # Good Friday: both OT lessons are the historic (pre-LSB) ones
    gf = {r["ref"]: r["mark"] for r in by_slot["good_friday_fer"]["readings"]}
    assert gf["Hosea 5:15b-6:6"] == "*" and gf["Exodus 12:1-11"] == "*"


# --- Passion History -------------------------------------------------------

def test_passion_seven_parts():
    assert len(PH.PARTS) == 7
    assert [p["n"] for p in PH.PARTS] == [1, 2, 3, 4, 5, 6, 7]


def test_passion_wednesdays_are_all_wednesdays():
    cal = LiturgicalCalendar(2025)
    rows = PH.resolve_schedule("wednesdays", cal)
    assert len(rows) == 7
    assert all(d.strftime("%A") == "Wednesday" for _, _, d in rows)
    assert rows[0][2] == cal.ash_wednesday


def test_passion_holy_week_span():
    from datetime import timedelta
    cal = LiturgicalCalendar(2025)
    rows = PH.resolve_schedule("holy_week", cal)
    assert rows[0][2] == cal.palm_sunday
    assert rows[5][2] == cal.good_friday
    assert rows[6][2] == cal.good_friday + timedelta(1) and rows[6][1] == "Holy Saturday"


# --- routes ----------------------------------------------------------------

def test_routes_ok():
    import app as A
    c = A.app.test_client()
    for url in ["/lent", "/lent/ferial", "/lent/ferial?year=2026",
                "/lent/passion", "/lent/passion?schedule=holy_week&year=2027",
                "/lent/sources"]:
        assert c.get(url).status_code == 200, url


def test_ferial_day_card_and_pdf():
    import app as A
    c = A.app.test_client()
    # 2026-02-18 = Ash Wednesday (a ferial day); 2026-07-01 is not in Lent
    card = c.get("/lent/ferial/2026-02-18")
    assert card.status_code == 200
    assert b"Ash Wednesday" in card.data
    pdf = c.get("/lent/ferial/2026-02-18/pdf")
    assert pdf.status_code == 200
    assert pdf.headers["Content-Type"] == "application/pdf"
    assert c.get("/lent/ferial/2026-07-01").status_code == 404
    assert c.get("/lent/ferial/not-a-date").status_code == 404


# --- Calendar Explorer tools ----------------------------------------------

def test_weekday_finder():
    import app as A
    c = A.app.test_client()
    r = c.get("/almanac/weekday?date=1990-05-24&weekday=6")
    assert r.status_code == 200
    assert b"Thursday" in r.data              # 1990-05-24 was a Thursday
    assert b"Sunday, May 24, 1992" in r.data  # next May 24 on a Sunday


def test_date_calculator():
    import app as A
    c = A.app.test_client()
    # Ash Wednesday to Easter 2026 is exactly 46 days
    r = c.get("/almanac/datecalc?mode=between&d1=2026-02-18&d2=2026-04-05")
    assert r.status_code == 200 and b"46" in r.data
    r2 = c.get("/almanac/datecalc?mode=offset&d1=2026-01-01&n=100&direction=after")
    assert r2.status_code == 200 and b"April 11, 2026" in r2.data


def test_font_pref_present():
    import app as A
    c = A.app.test_client()
    s = c.get("/settings").get_data(as_text=True)
    assert "set-font" in s and "lcms_font" in s
