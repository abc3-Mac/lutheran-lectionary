"""Tests for civil / secular holiday awareness (Roadmap E).

Dates cross-verified against an independent calendar for 2026 (and a few other
years) — moveable holidays must be derived correctly, not hand-typed.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.data.civil_holidays import (
    civil_holidays_for,
    _nth_weekday,
    _last_weekday,
)


def _names(d: date) -> list[str]:
    return [h["name"] for h in civil_holidays_for(d)]


def test_fixed_date_holidays():
    assert "New Year's Day" in _names(date(2026, 1, 1))
    assert "Valentine's Day" in _names(date(2026, 2, 14))
    assert "St. Patrick's Day" in _names(date(2026, 3, 17))
    assert "Juneteenth" in _names(date(2026, 6, 19))
    assert "Independence Day" in _names(date(2026, 7, 4))
    assert "Veterans Day" in _names(date(2026, 11, 11))
    assert "Halloween" in _names(date(2026, 10, 31))
    assert "Christmas Day" in _names(date(2026, 12, 25))


def test_moveable_holidays_2026():
    # The motivating example: 2026-06-21 is Father's Day (and Pentecost 4).
    assert "Father's Day" in _names(date(2026, 6, 21))
    assert "Mother's Day" in _names(date(2026, 5, 10))      # 2nd Sun of May
    assert "Memorial Day" in _names(date(2026, 5, 25))      # last Mon of May
    assert "Labor Day" in _names(date(2026, 9, 7))          # 1st Mon of Sep
    assert "Thanksgiving Day" in _names(date(2026, 11, 26)) # 4th Thu of Nov
    assert "Martin Luther King Jr. Day" in _names(date(2026, 1, 19))   # 3rd Mon Jan
    assert "Presidents' Day" in _names(date(2026, 2, 16))   # 3rd Mon Feb
    assert "Columbus Day / Indigenous Peoples' Day" in _names(date(2026, 10, 12))  # 2nd Mon Oct


def test_moveable_holidays_other_years():
    # Independent cross-check across years guards the nth-weekday math.
    assert "Thanksgiving Day" in _names(date(2025, 11, 27))
    assert "Thanksgiving Day" in _names(date(2024, 11, 28))
    assert "Mother's Day" in _names(date(2025, 5, 11))
    assert "Father's Day" in _names(date(2025, 6, 15))
    assert "Memorial Day" in _names(date(2024, 5, 27))


def test_no_holiday_on_ordinary_day():
    assert civil_holidays_for(date(2026, 6, 28)) == []
    assert civil_holidays_for(date(2026, 3, 4)) == []


def test_shape_and_kind():
    h = civil_holidays_for(date(2026, 7, 4))[0]
    assert h == {"name": "Independence Day", "kind": "federal", "country": "USA"}
    h = civil_holidays_for(date(2026, 6, 21))[0]
    assert h["kind"] == "observance"   # Father's Day is not a federal holiday


def test_unknown_country_is_empty():
    assert civil_holidays_for(date(2026, 7, 4), country="ZZ") == []


def test_weekday_helpers():
    # Mon=1 … Sun=7
    assert _nth_weekday(2026, 6, 7, 3) == date(2026, 6, 21)   # 3rd Sunday of June
    assert _nth_weekday(2026, 1, 1, 1) == date(2026, 1, 5)    # 1st Monday of Jan
    assert _last_weekday(2026, 5, 1) == date(2026, 5, 25)     # last Monday of May
    assert _last_weekday(2026, 12, 4) == date(2026, 12, 31)   # last Thursday of Dec
