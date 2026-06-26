"""Tests for the Almanac engines: computus, calendar conversion, Moon phases.

Moon-phase results are cross-validated against the U.S. Naval Observatory's
published 2026 phase table (aa.usno.navy.mil) — every computed phase must land
within two minutes of USNO. Easter dates are checked against known historical
values (earliest/latest, and the 2025 East/West coincidence).
"""

import os
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.almanac import computus, convert, moon


# --- Computus -------------------------------------------------------------

def test_western_easter_known_years():
    assert computus.gregorian_easter(2024) == date(2024, 3, 31)
    assert computus.gregorian_easter(2025) == date(2025, 4, 20)
    assert computus.gregorian_easter(2026) == date(2026, 4, 5)
    assert computus.gregorian_easter(2000) == date(2000, 4, 23)


def test_western_easter_extremes():
    # Earliest possible Western Easter is March 22 (e.g. 1818, 2285);
    # latest is April 25 (e.g. 1943, 2038).
    assert computus.gregorian_easter(1818) == date(1818, 3, 22)
    assert computus.gregorian_easter(2285) == date(2285, 3, 22)
    assert computus.gregorian_easter(1943) == date(1943, 4, 25)
    assert computus.gregorian_easter(2038) == date(2038, 4, 25)
    # No Easter ever falls outside [Mar 22, Apr 25].
    for y in range(1900, 2101):
        e = computus.gregorian_easter(y)
        assert (e.month, e.day) >= (3, 22)
        assert (e.month, e.day) <= (4, 25)


def test_orthodox_easter_known_years():
    assert computus.orthodox_easter(2024) == date(2024, 5, 5)
    assert computus.orthodox_easter(2025) == date(2025, 4, 20)   # coincides with West
    assert computus.orthodox_easter(2026) == date(2026, 4, 12)
    # East is on or after West, never before.
    for y in range(2000, 2051):
        assert computus.orthodox_easter(y) >= computus.gregorian_easter(y)


def test_movable_feasts():
    mf = computus.movable_feasts(2026, "western")
    assert mf["easter"] == date(2026, 4, 5)
    assert mf["ash_wednesday"] == date(2026, 2, 18)
    assert mf["pentecost"] == date(2026, 5, 24)
    assert mf["ascension"] == date(2026, 5, 14)


# --- Calendar conversion --------------------------------------------------

def test_julian_day_known_values():
    # Meeus, Astronomical Algorithms, worked examples.
    assert convert.gregorian_to_jd(2000, 1, 1.5) == 2451545.0
    assert abs(convert.gregorian_to_jd(1957, 10, 4.81) - 2436116.31) < 1e-6
    assert convert.julian_to_jd(333, 1, 27.5) == 1842713.0


def test_jd_roundtrip():
    for y, m, d in [(2026, 6, 21.0), (1582, 10, 15.0), (1900, 1, 1.0), (2100, 12, 31.0)]:
        jd = convert.gregorian_to_jd(y, m, d)
        ry, rm, rd = convert.jd_to_gregorian(jd)
        assert (ry, rm, round(rd, 6)) == (y, m, d)


def test_calendar_reform_alignment():
    # The day after Julian 1582-10-04 is Gregorian 1582-10-15.
    assert convert.julian_to_gregorian(1582, 10, 5) == date(1582, 10, 15)
    # In the 20th-21st c. the Julian calendar runs 13 days behind Gregorian.
    assert convert.gregorian_to_julian(date(2026, 1, 14)) == (2026, 1, 1)


def test_datetime_jd_roundtrip():
    dt = datetime(2026, 3, 3, 11, 38)
    jd = convert.datetime_to_jd(dt)
    back = convert.jd_to_datetime(jd)
    assert abs((back - dt).total_seconds()) < 1.0


# --- Moon phases vs USNO 2026 --------------------------------------------

USNO_2026 = [
    ("Full moon", "2026-01-03 10:03"), ("Last quarter", "2026-01-10 15:48"),
    ("New moon", "2026-01-18 19:52"), ("First quarter", "2026-01-26 04:47"),
    ("Full moon", "2026-02-01 22:09"), ("Last quarter", "2026-02-09 12:43"),
    ("New moon", "2026-02-17 12:01"), ("First quarter", "2026-02-24 12:27"),
    ("Full moon", "2026-03-03 11:38"), ("Last quarter", "2026-03-11 09:38"),
    ("New moon", "2026-03-19 01:23"), ("First quarter", "2026-03-25 19:18"),
    ("Full moon", "2026-04-02 02:12"), ("Last quarter", "2026-04-10 04:51"),
    ("New moon", "2026-04-17 11:52"), ("First quarter", "2026-04-24 02:32"),
    ("Full moon", "2026-05-01 17:23"), ("Last quarter", "2026-05-09 21:10"),
    ("New moon", "2026-05-16 20:01"), ("First quarter", "2026-05-23 11:11"),
    ("Full moon", "2026-05-31 08:45"), ("Last quarter", "2026-06-08 10:00"),
    ("New moon", "2026-06-15 02:54"), ("First quarter", "2026-06-21 21:55"),
    ("Full moon", "2026-06-29 23:56"), ("Last quarter", "2026-07-07 19:29"),
    ("New moon", "2026-07-14 09:43"), ("First quarter", "2026-07-21 11:05"),
    ("Full moon", "2026-07-29 14:36"), ("Last quarter", "2026-08-06 02:21"),
    ("New moon", "2026-08-12 17:37"), ("First quarter", "2026-08-20 02:46"),
    ("Full moon", "2026-08-28 04:18"), ("Last quarter", "2026-09-04 07:51"),
    ("New moon", "2026-09-11 03:27"), ("First quarter", "2026-09-18 20:44"),
    ("Full moon", "2026-09-26 16:49"), ("Last quarter", "2026-10-03 13:25"),
    ("New moon", "2026-10-10 15:50"), ("First quarter", "2026-10-18 16:12"),
    ("Full moon", "2026-10-26 04:12"), ("Last quarter", "2026-11-01 20:28"),
    ("New moon", "2026-11-09 07:02"), ("First quarter", "2026-11-17 11:48"),
    ("Full moon", "2026-11-24 14:53"), ("Last quarter", "2026-12-01 06:08"),
    ("New moon", "2026-12-09 00:52"), ("First quarter", "2026-12-17 05:42"),
    ("Full moon", "2026-12-24 01:28"), ("Last quarter", "2026-12-30 18:59"),
]


def test_moon_phases_match_usno_2026():
    computed = moon.phases_in_range(date(2026, 1, 1), date(2026, 12, 31))
    assert len(computed) == len(USNO_2026)
    for (name, ts), got in zip(USNO_2026, computed):
        ref = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        assert got.phase == name
        diff = abs((got.dt - ref).total_seconds())
        assert diff <= 120, f"{name} {ts}: off by {diff:.0f}s (got {got.dt})"


def test_full_and_new_moon_counts():
    assert len(moon.full_moons(2026)) == 13   # two in May -> a blue moon
    assert len(moon.new_moons(2026)) == 12


def test_blue_moon_2026():
    bm = moon.blue_moons(2026)
    monthly = [b for b in bm if b["kind"] == "monthly"]
    assert len(monthly) == 1
    assert monthly[0]["date"] == date(2026, 5, 31)


def test_phase_at():
    full = moon.phase_at(date(2026, 3, 3))
    assert full["illumination"] > 0.98 and full["phase"] == "Full moon"
    new = moon.phase_at(date(2026, 3, 19))
    assert new["illumination"] < 0.02 and new["phase"] == "New moon"
    q = moon.phase_at(date(2026, 6, 21))
    assert q["waxing"] is True


# --- Ecclesiastical vs astronomical (date of Easter) ----------------------

def test_paschal_full_moon_drives_easter():
    # By definition Easter is the first Sunday STRICTLY after the ecclesiastical
    # Paschal full moon — verify across centuries.
    from datetime import timedelta
    for y in range(1583, 2200):
        pfm = computus.paschal_full_moon(y)
        days = (6 - pfm.weekday()) % 7 or 7   # next Sunday strictly after
        assert pfm + timedelta(days=days) == computus.gregorian_easter(y)
        assert date(y, 3, 21) <= pfm <= date(y, 4, 18)


def test_easter_moon_comparison_2019():
    # 2019 is a textbook case: ecclesiastical full moon (Apr 18) lags the
    # astronomical one by a day.
    c = computus.easter_moon_comparison(2019)
    assert c["ecclesiastical_full_moon"] == date(2019, 4, 18)
    assert c["delta_days"] != 0
    assert c["golden_number"] == 2019 % 19 + 1


# --- Extended range: Julian era (back to AD 30) ---------------------------

def test_julian_easter_always_sunday_and_consistent():
    from datetime import timedelta
    for y in range(30, 1583):
        e = convert.julian_to_gregorian(*computus.julian_easter_old_style(y))
        assert e.weekday() == 6, f"Julian Easter {y} not a Sunday: {e}"
        pfm = convert.julian_to_gregorian(*computus.julian_paschal_full_moon_old_style(y))
        days = (6 - pfm.weekday()) % 7 or 7
        assert pfm + timedelta(days=days) == e   # first Sunday strictly after the PFM


def test_ancient_calendar_conversion_floor():
    # Regression: before ~AD 400 the Gregorian-branch alpha goes negative;
    # int() (truncate) instead of floor() shifted ancient dates by a day.
    # Round-trip ancient Julian dates through Gregorian and back.
    for os in [(33, 4, 3), (325, 4, 18), (100, 1, 1), (30, 6, 15)]:
        g = convert.julian_to_gregorian(*os)
        assert convert.gregorian_to_julian(g) == os
    # The reform boundary is still exact: Julian 1582-10-04 -> Gregorian 10-14.
    assert convert.julian_to_gregorian(1582, 10, 4) == date(1582, 10, 14)


def test_crucifixion_full_moon_ad33():
    # Humphreys & Waddington: the Passover full moon of AD 33 fell on Friday
    # 3 April (Julian). Our engine should agree to the day in antiquity.
    aprils = [p for p in moon.full_moons(33) if p.dt.month in (3, 4) and p.dt.month == 4]
    j = convert.gregorian_to_julian(aprils[0].date)
    assert j[1] == 4 and j[2] == 3        # April 3 Julian
    assert aprils[0].date.weekday() == 4  # Friday


def test_historical_easter_flags():
    h = computus.historical_easter(325)
    assert h["calendar"] == "Julian" and h["before_nicaea"] is False
    h30 = computus.historical_easter(30)
    assert h30["before_nicaea"] is True and h30["western"] is None
    h2026 = computus.historical_easter(2026)
    assert h2026["calendar"] == "Gregorian" and h2026["western"] == date(2026, 4, 5)


def test_easter_west_east_coincidence_and_gap():
    # 2025: West and East coincide (both April 20). 2026: East is 7 days later.
    assert computus.gregorian_easter(2025) == computus.orthodox_easter(2025)
    assert (computus.orthodox_easter(2026) - computus.gregorian_easter(2026)).days == 7
    # The gap is always a non-negative multiple of 7 (both are Sundays).
    for y in range(1990, 2050):
        gap = (computus.orthodox_easter(y) - computus.gregorian_easter(y)).days
        assert gap >= 0 and gap % 7 == 0


def test_easter_comparison_julian_era():
    c = computus.easter_moon_comparison(1000)
    assert c["calendar"] == "Julian"
    assert c["ecclesiastical_full_moon_os"] is not None
    assert c["easter_os"] is not None


# --- Moon-phase icons -----------------------------------------------------

def test_moon_icons():
    from liturgical_calendar.almanac.icons import moon_svg, phase_icon
    from liturgical_calendar.almanac.icons import LIT, SHADOW
    new = moon_svg(0.0, True)
    assert new.count("<circle") == 1 and "<path" not in new and SHADOW in new   # bare dark disc
    assert "<path" in moon_svg(0.25, True)                                       # crescent lit path
    full = moon_svg(1.0, True)
    assert "<path" not in full and LIT in full and SHADOW not in full            # fully lit disc
    assert "Full moon" in phase_icon("Full moon")
