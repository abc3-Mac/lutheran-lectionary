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
    assert h == {
        "name": "Independence Day", "kind": "federal", "country": "USA",
        "relationship": "on", "date": "2026-07-04", "when": "Saturday, July 4",
    }
    h = civil_holidays_for(date(2026, 6, 21))[0]
    assert h["kind"] == "observance"   # Father's Day is not a federal holiday
    assert h["relationship"] == "on"


def test_nearest_sunday_surfaces_holiday():
    # July 4, 2026 is a Saturday; the nearest Sunday is July 5. The Sunday
    # should surface Independence Day as a "nearby" observance with its real date.
    sun = civil_holidays_for(date(2026, 7, 5))
    indep = [h for h in sun if h["name"] == "Independence Day"]
    assert indep, "Independence Day should surface on the nearest Sunday"
    assert indep[0]["relationship"] == "nearby"
    assert indep[0]["date"] == "2026-07-04"
    assert indep[0]["when"] == "Saturday, July 4"


def test_nearest_sunday_is_the_only_one():
    # The Sunday *before* July 4 (June 28) is farther away, so it must NOT
    # surface Independence Day — only the genuinely nearest Sunday does.
    assert "Independence Day" not in _names(date(2026, 6, 28))


def test_monday_holiday_surfaces_on_prior_sunday():
    # Memorial Day 2026 is Mon May 25; the nearest Sunday is the day before.
    h = [x for x in civil_holidays_for(date(2026, 5, 24)) if x["name"] == "Memorial Day"]
    assert h and h[0]["relationship"] == "nearby"
    assert h[0]["date"] == "2026-05-25"


def test_holiday_on_sunday_is_on_not_nearby():
    # Father's Day already falls on a Sunday — it must be "on", never duplicated.
    fathers = [h for h in civil_holidays_for(date(2026, 6, 21)) if h["name"] == "Father's Day"]
    assert len(fathers) == 1 and fathers[0]["relationship"] == "on"


def test_include_nearby_can_be_disabled():
    # iCal feeds want only holidays that land squarely on the day.
    assert civil_holidays_for(date(2026, 7, 5), include_nearby=False) == []


def test_unknown_country_is_empty():
    assert civil_holidays_for(date(2026, 7, 4), country="ZZ") == []


def test_weekday_helpers():
    # Mon=1 … Sun=7
    assert _nth_weekday(2026, 6, 7, 3) == date(2026, 6, 21)   # 3rd Sunday of June
    assert _nth_weekday(2026, 1, 1, 1) == date(2026, 1, 5)    # 1st Monday of Jan
    assert _last_weekday(2026, 5, 1) == date(2026, 5, 25)     # last Monday of May
    assert _last_weekday(2026, 12, 4) == date(2026, 12, 31)   # last Thursday of Dec
