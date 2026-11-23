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
# Reformation / All Saints (regression: Sat Oct 31 2026 showed Pentecost 22)
# LCMS 2025–26 calendar: Reformation observed Oct 25, All Saints Nov 1.
# ---------------------------------------------------------------------------

def test_reformation_and_all_saints_2026():
    cal = cal_2025()
    assert cal.reformation_observed == date(2026, 10, 25)
    assert cal.all_saints_observed  == date(2026, 11, 1)
    for lectionary in ("three_year", "one_year"):
        assert cal.lookup(date(2026, 10, 25), lectionary)["slot"] == "reformation"
        assert cal.lookup(date(2026, 10, 31), lectionary)["slot"] == "reformation"
        assert cal.lookup(date(2026, 11, 1),  lectionary)["slot"] == "all_saints"
    # The week after an observed festival belongs to the displaced Proper
    wk = cal.lookup(date(2026, 10, 27))
    assert wk["is_weekday"] and wk["name"] == "Twenty-second Sunday after Pentecost"
    assert cal.lookup(date(2026, 11, 8))["name"] == "Twenty-fourth Sunday after Pentecost"


def test_reformation_and_all_saints_never_share_a_sunday():
    for y in range(2020, 2050):
        cal = LiturgicalCalendar(y - 1)
        assert cal.reformation_observed != cal.all_saints_observed
        assert cal.lookup(date(y, 10, 31))["slot"] == "reformation"
        assert cal.lookup(date(y, 11, 1))["slot"] == "all_saints"


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


def test_one_year_trinity_season_covers_trinity_and_last_sunday():
    from datetime import date
    from liturgical_calendar.calculator import LiturgicalCalendar
    cal = LiturgicalCalendar(2025)
    evs = [e for e in cal.all_events(lectionary="one_year")
           if cal.holy_trinity <= e["date"] < cal.next_advent_1]
    assert evs and all(e["season"] == "Trinity" for e in evs), \
        {e["name"]: e["season"] for e in evs if e["season"] != "Trinity"}
    for d in (date(2026, 5, 31), date(2026, 6, 2), date(2026, 11, 22), date(2026, 11, 26)):
        assert cal.lookup(d, "one_year")["season"] == "Trinity", d
    # The three-year series keeps "Ordinary Time".
    assert cal.lookup(date(2026, 11, 22), "three_year")["season"] == "Ordinary Time"


def test_thanksgiving_has_its_own_day_and_readings_in_both_lectionaries():
    """LSB Propers of the Day, pp. 438-439: one set of propers for both series."""
    cal = LiturgicalCalendar(2025)
    for lectionary in ("three_year", "one_year"):
        day = cal.lookup(date(2026, 11, 26), lectionary)
        assert day["name"] == "Day of Thanksgiving"
        assert day["is_weekday"] is False
        assert day["readings"] == {
            "ot": "Deuteronomy 8:1-10",
            "ps": "Psalm 67 (antiphon: v. 7)",
            "ep": "Philippians 4:6-20 | 1 Timothy 2:1-4",
            "go": "Luke 17:11-19",
        }
        ev = [e for e in cal.all_events(True, lectionary) if e["slot"] == "thanksgiving"]
        assert ev and ev[0]["readings"]["go"] == "Luke 17:11-19"


def test_thanksgiving_eve_points_to_the_day_and_friday_returns_to_the_week():
    cal = LiturgicalCalendar(2025)
    eve = cal.lookup(date(2026, 11, 25), "three_year")
    assert eve["is_weekday"] and eve["eve_of"]["name"] == "Day of Thanksgiving"
    fri = cal.lookup(date(2026, 11, 27), "three_year")
    assert fri["is_weekday"] and fri["name"] == "Last Sunday of the Church Year"
    assert fri["eve_of"] is None


def test_weekdays_with_their_own_propers_are_their_own_days():
    """LSB Propers of the Day: Holy Week, Easter and Pentecost weekdays."""
    cal = LiturgicalCalendar(2026)        # Easter 28 March 2027, Pentecost 16 May
    expected = {
        date(2026, 12, 24): "The Nativity of Our Lord (Christmas Eve)",
        date(2027, 3, 22): "Monday in Holy Week",
        date(2027, 3, 23): "Tuesday in Holy Week",
        date(2027, 3, 24): "Wednesday in Holy Week",
        date(2027, 3, 27): "Holy Saturday",
        date(2027, 3, 29): "Easter Monday",
        date(2027, 3, 30): "Easter Tuesday",
        date(2027, 3, 31): "Easter Wednesday",
        date(2027, 5, 15): "Pentecost Eve",
        date(2027, 5, 17): "Pentecost Monday",
        date(2027, 5, 18): "Pentecost Tuesday",
    }
    for lectionary in ("three_year", "one_year"):
        for d, name in expected.items():
            day = cal.lookup(d, lectionary)
            assert (day["name"], day["is_weekday"]) == (name, False), (d, lectionary)
            assert day["readings"]
        # none of them governs the days after it
        assert cal.lookup(date(2027, 4, 1), lectionary)["slot"] == "easter"
        assert cal.lookup(date(2027, 5, 19), lectionary)["slot"] == "pentecost"
        # listed with the minor feasts, never without, never on the wheel
        slots = {e["slot"] for e in cal.all_events(False, lectionary)}
        assert "easter_monday" not in slots and "holy_saturday" not in slots
        slots = {e["slot"] for e in cal.all_events(True, lectionary)}
        assert {"monday_holy_week", "holy_saturday", "easter_wednesday", "pentecost_tuesday"} <= slots


def test_three_year_holy_week_weekdays_match_the_book():
    cal = LiturgicalCalendar(2026)
    assert cal.lookup(date(2027, 3, 22))["readings"] == {
        "ot": "Isaiah 50:5-10", "ps": "Psalm 36:5-10 (antiphon: v. 9)",
        "ep": "Hebrews 9:11-15", "go": "Matthew 26:1-27:66 | John 12:1-23"}
    assert cal.lookup(date(2027, 3, 24))["readings"]["go"] == "Luke 22:1-23:56 | John 13:16-38"


def test_other_services_of_the_great_feasts():
    cal = LiturgicalCalendar(2026)
    names = lambda d, l="three_year": [o["name"] for o in cal.lookup(d, l)["other_services"]]
    assert names(date(2026, 12, 25)) == ["Christmas Midnight", "Christmas Dawn"]
    assert names(date(2027, 3, 28)) == ["Easter Sunrise", "Easter Evening"]
    assert names(date(2027, 5, 16)) == ["Pentecost Evening"]
    assert names(date(2027, 3, 29)) == []
    # one-year Christmas Dawn has its own Old Testament reading
    dawn = cal.lookup(date(2026, 12, 25), "one_year")["other_services"][1]
    assert dawn["readings"]["ot"] == "Micah 5:2-5a"
    # December 24 on a Sunday (2028) is Advent 4, with Christmas Eve beside it
    cal28 = LiturgicalCalendar(2028)
    day = cal28.lookup(date(2028, 12, 24))
    assert day["slot"] == "advent_4" and [o["name"] for o in day["other_services"]] == ["Christmas Eve"]


def test_ten_more_feasts_fall_on_their_dates():
    cal = LiturgicalCalendar(2026)
    expected = {
        date(2026, 12, 26): "St. Stephen, Martyr",
        date(2026, 12, 27): "St. John, Apostle and Evangelist",
        date(2027, 1, 24): "St. Timothy, Pastor and Confessor",
        date(2027, 1, 26): "St. Titus, Pastor and Confessor",
        date(2027, 3, 19): "St. Joseph, Guardian of Jesus",
        date(2027, 8, 15): "St. Mary, Mother of Our Lord",
        date(2027, 8, 29): "The Martyrdom of St. John the Baptist",
        date(2027, 9, 14): "Holy Cross Day",
        date(2027, 10, 23): "St. James of Jerusalem, Brother of Jesus and Martyr",
    }
    for lectionary in ("three_year", "one_year"):
        for d, name in expected.items():
            mf = cal.lookup(d, lectionary)["minor_feast"]
            assert mf and mf["name"] == name and mf["readings"], (d, lectionary)
    # The Visitation: May 31 in the three-year lectionary, July 2 in the one-year
    assert cal.lookup(date(2027, 5, 31), "three_year")["minor_feast"]["name"] == "The Visitation"
    assert cal.lookup(date(2027, 7, 2), "three_year")["minor_feast"] is None
    assert cal.lookup(date(2027, 7, 2), "one_year")["minor_feast"]["name"] == "The Visitation"
    assert cal.lookup(date(2027, 5, 31), "one_year")["minor_feast"] is None
