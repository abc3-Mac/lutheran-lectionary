"""Tests for the LSB Hymn of the Day data and accessor."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from liturgical_calendar.data.hymn_of_the_day import (
    HOTD_ONE_YEAR, HOTD_THREE_YEAR, hymn_of_the_day)
from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
from liturgical_calendar.data.three_year import THREE_YEAR_SLOTS


def test_known_assignments():
    # Advent 1 is LSB 332 in both series (the classic chief hymn)
    assert hymn_of_the_day("advent_1", "one_year")[0].startswith("LSB 332")
    for yr in "ABC":
        assert hymn_of_the_day("advent_1", "three_year", yr)[0].startswith("LSB 332")
    # One-year frequently differs from three-year
    assert hymn_of_the_day("trinity_1", "one_year")[0].startswith("LSB 768")


def test_three_year_varies_by_series_year():
    # Proper 29 (Christ the King) has a different hymn each year
    a = hymn_of_the_day("proper_29", "three_year", "A")[0]
    b = hymn_of_the_day("proper_29", "three_year", "B")[0]
    c = hymn_of_the_day("proper_29", "three_year", "C")[0]
    assert len({a, b, c}) == 3
    # Epiphany 5: A differs from B/C
    assert hymn_of_the_day("epiphany_5", "three_year", "A")[0].startswith("LSB 578")
    assert hymn_of_the_day("epiphany_5", "three_year", "B")[0].startswith("LSB 398")


def test_last_sunday_three_year_aliases_proper_29():
    for yr in "ABC":
        assert (hymn_of_the_day("last_sunday", "three_year", yr)
                == hymn_of_the_day("proper_29", "three_year", yr))


def test_full_coverage():
    # Every one-year slot has at least one hymn
    missing1 = [s for s in ONE_YEAR_SLOTS if s not in HOTD_ONE_YEAR]
    assert not missing1, missing1
    # Every three-year slot has hymns for all of A, B, C
    for s in THREE_YEAR_SLOTS:
        entry = HOTD_THREE_YEAR.get(s)
        assert entry, f"no hymns for {s}"
        for yr in "ABC":
            assert entry[yr], f"no year-{yr} hymn for {s}"


def test_unknown_slot_returns_none():
    assert hymn_of_the_day("not_a_slot", "one_year") is None
    assert hymn_of_the_day("not_a_slot", "three_year", "A") is None
