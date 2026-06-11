"""Tests for the LSB Daily Lectionary data and resolution logic."""

import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.calculator import daily_readings, calc_easter
from liturgical_calendar.data.daily_lectionary import DAILY_FIXED, DAILY_MOVABLE


def test_table_sizes():
    # Ash Wednesday through Holy Trinity inclusive = 103 days
    assert len(DAILY_MOVABLE) == 103
    # Nov 27-Mar 9 (104 incl. Feb 29) + May 18-Nov 26 (193) = 297
    assert len(DAILY_FIXED) == 297


def test_movable_milestones():
    assert DAILY_MOVABLE[0]["day"] == "Ash Wednesday"
    assert DAILY_MOVABLE[4]["day"].startswith("Lent 1")
    assert DAILY_MOVABLE[46]["day"].startswith("Easter")
    assert DAILY_MOVABLE[95]["day"].startswith("Pentecost")
    assert DAILY_MOVABLE[102]["day"].startswith("Holy Trinity")


def test_known_entries():
    # Verified against Wartburg Project (same lectionary as LSB/TDP)
    assert daily_readings(date(2026, 6, 11)) == {"ot": "Proverbs 9:1-18", "nt": "John 13:21-38"}
    assert daily_readings(date(2026, 2, 20)) == {
        "day": "Friday", "ot": "Genesis 2:4-25", "nt": "Mark 1:29-45"}
    # First day of the cycle
    assert daily_readings(date(2026, 11, 27)) == {"ot": "Isaiah 1:1-28", "nt": "1 Peter 1:1-12"}


def test_ash_wednesday_any_year():
    for year in (2024, 2026, 2030, 2038):
        ash_wed = calc_easter(year) - timedelta(46)
        entry = daily_readings(ash_wed)
        assert entry["day"] == "Ash Wednesday"
        assert entry["ot"] == "Genesis 1:1-19"
        assert entry["nt"] == "Mark 1:1-13"


def test_every_day_resolves():
    """No gaps for any date across two decades (incl. earliest/latest Easters)."""
    d = date(2020, 1, 1)
    while d < date(2041, 1, 1):
        assert daily_readings(d) is not None, f"no daily readings for {d}"
        d += timedelta(1)


def test_movable_overrides_fixed():
    # 2026: Ash Wednesday = Feb 18. Feb 20 falls in both tables; movable wins.
    assert "day" in daily_readings(date(2026, 2, 20))
    # Feb 17 2026 (day before Ash Wednesday) uses the fixed table.
    assert "day" not in daily_readings(date(2026, 2, 17))
