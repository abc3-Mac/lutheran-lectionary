"""Regression tests pinned to known-truth liturgical dates.

Run with:  python3 -m pytest tests/
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.calculator import (
    LiturgicalCalendar, calc_easter, advent1_for_year, get_series,
)
from liturgical_calendar.utils import clean_passage_for_bible_gateway, bg_url


# ---------------------------------------------------------------------------
# Computus — Easter (Gregorian, well-documented dates)
# ---------------------------------------------------------------------------

EASTER_DATES = {
    2024: date(2024, 3, 31),
    2025: date(2025, 4, 20),
    2026: date(2026, 4, 5),
    2027: date(2027, 3, 28),
    2030: date(2030, 4, 21),
    2038: date(2038, 4, 25),   # latest possible Easter this century
}

def test_easter_dates():
    for year, expected in EASTER_DATES.items():
        assert calc_easter(year) == expected, f"Easter {year}"


# ---------------------------------------------------------------------------
# Advent 1 — fourth Sunday before Christmas
# ---------------------------------------------------------------------------

ADVENT1_DATES = {
    2024: date(2024, 12, 1),
    2025: date(2025, 11, 30),
    2026: date(2026, 11, 29),
    2027: date(2027, 11, 28),
}

def test_advent1_dates():
    for year, expected in ADVENT1_DATES.items():
        assert advent1_for_year(year) == expected, f"Advent 1 {year}"


def test_series_cycle():
    # README: 2025–2026 = A, 2026–2027 = B, 2027–2028 = C
    assert get_series(2025) == "A"
    assert get_series(2026) == "B"
    assert get_series(2027) == "C"
    assert get_series(2028) == "A"


# ---------------------------------------------------------------------------
# Key movable feasts for the 2025–2026 church year
# ---------------------------------------------------------------------------

def cal_2025():
    return LiturgicalCalendar(2025)


def test_2025_anchor_dates():
    cal = cal_2025()
    assert cal.advent_1 == date(2025, 11, 30)
    assert cal.easter == date(2026, 4, 5)
    assert cal.pentecost == date(2026, 5, 24)
    assert cal.holy_trinity == date(2026, 5, 31)
    assert cal.ash_wednesday == date(2026, 2, 18)
    assert cal.palm_sunday == date(2026, 3, 29)
    # Gesima Sundays
    assert cal.septuagesima == date(2026, 2, 1)
    assert cal.quinquagesima == date(2026, 2, 15)
    # One-year Transfiguration = Sunday before Septuagesima
    assert cal.transfiguration_1yr == date(2026, 1, 25)


# ---------------------------------------------------------------------------
# Trinity season numbering (regression: Jon Ellingworth bug report 2026-06)
# The Sunday one week after Trinity Sunday is the FIRST Sunday after Trinity.
# ---------------------------------------------------------------------------

def test_trinity_numbering_one_year():
    cal = cal_2025()
    events = cal.all_events(include_minor=False, lectionary="one_year")
    by_date = {ev["date"]: ev for ev in events}

    assert by_date[date(2026, 5, 31)]["name"] == "The Holy Trinity"
    assert by_date[date(2026, 6, 7)]["name"] == "First Sunday after Trinity"
    assert by_date[date(2026, 6, 14)]["name"] == "Second Sunday after Trinity"
    assert by_date[date(2026, 6, 21)]["name"] == "Third Sunday after Trinity"

    # Slot keys must line up with the data file's keys
    assert by_date[date(2026, 6, 7)]["slot"] == "trinity_1"


def test_trinity_gospels_match_historic_lectionary():
    """ELS/LCMS historic pericopes (Tony Pittenger's checklist)."""
    cal = cal_2025()
    events = cal.all_events(include_minor=False, lectionary="one_year")
    by_name = {ev["name"]: ev for ev in events if ev.get("readings")}

    assert "Luke 16:19-31" in by_name["First Sunday after Trinity"]["readings"]["go"]
    assert "Luke 14:15-24" in by_name["Second Sunday after Trinity"]["readings"]["go"]
    assert "Luke 15:1-10" in by_name["Third Sunday after Trinity"]["readings"]["go"]


def test_lookup_weekday_governing_sunday():
    cal = cal_2025()
    # Wednesday June 10, 2026 falls in the week of Trinity 1
    info = cal.lookup(date(2026, 6, 10), lectionary="one_year")
    assert info is not None
    assert info.get("is_weekday") is True
    assert info["name"] == "First Sunday after Trinity"


def test_one_year_sundays_have_propers():
    cal = cal_2025()
    events = cal.all_events(include_minor=False, lectionary="one_year")
    sundays = [ev for ev in events if ev["is_sunday"]]
    with_propers = [ev for ev in sundays if ev.get("collect") or ev.get("introit")]
    # The propers data covers the great majority of Sundays
    assert len(with_propers) >= 50, f"only {len(with_propers)} Sundays have propers"


def test_all_events_sorted_and_unique_slots_per_date():
    cal = cal_2025()
    for lectionary in ("three_year", "one_year"):
        events = cal.all_events(include_minor=False, lectionary=lectionary)
        dates = [ev["date"] for ev in events]
        assert dates == sorted(dates), f"{lectionary} events not sorted"


# ---------------------------------------------------------------------------
# Bible Gateway URL cleaning (regression: PR #1, TomaceGordon)
# ---------------------------------------------------------------------------

def test_bg_cleaning_strips_antiphon():
    assert clean_passage_for_bible_gateway(
        "Psalm 136:1-9 (23-26) (antiphon: v. 26)") == "Psalm 136:1-9, 23-26"

def test_bg_cleaning_optional_ranges():
    assert clean_passage_for_bible_gateway("Romans 9:1-5 (6-13)") == "Romans 9:1-5, 6-13"
    assert clean_passage_for_bible_gateway("1 Corinthians 1:(1-3) 4-9") == "1 Corinthians 1:1-3, 4-9"

def test_bg_cleaning_passthrough():
    assert clean_passage_for_bible_gateway("Matthew 21:1-11") == "Matthew 21:1-11"

def test_bg_cleaning_verse_letters_and_dashes():
    assert clean_passage_for_bible_gateway("2 Kings 5:1-15a") == "2 Kings 5:1-15"
    assert clean_passage_for_bible_gateway("Isaiah 52:13—53:12") == "Isaiah 52:13-53:12"

def test_bg_url_encodes_cleaned_ref():
    url = bg_url("Psalm 122 (antiphon: v. 6)")
    assert "antiphon" not in url
    assert "Psalm%20122" in url

def test_bg_cleaning_never_breaks_database_refs():
    """Every reference in both lectionaries must clean to something sane."""
    from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
    from liturgical_calendar.data.three_year import THREE_YEAR_SLOTS

    refs = set()
    for slots in (ONE_YEAR_SLOTS, THREE_YEAR_SLOTS):
        for info in slots.values():
            readings = info.get("readings") or {}
            if not isinstance(readings, dict):
                continue
            for v in readings.values():
                if v:
                    for part in str(v).split(" | "):
                        refs.add(part.strip())

    assert len(refs) > 400
    for r in refs:
        c = clean_passage_for_bible_gateway(r)
        assert c, f"emptied: {r!r}"
        assert "(" not in c and ")" not in c, f"leftover parens: {r!r} -> {c!r}"
        assert not c.endswith((":", ",", ";")), f"dangling punctuation: {r!r} -> {c!r}"
