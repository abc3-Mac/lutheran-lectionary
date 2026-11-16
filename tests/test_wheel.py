"""Liturgical Year Wheel: the four date styles and the /wheel routes."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app, get_calendar, _events_for_display
from liturgical_calendar.wheel import build_wheel_svg, DATE_STYLES, DEFAULT_DATE_STYLE


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _svg(dates, year=2025, lect="three_year", minor=False):
    cal = get_calendar(year)
    evs = _events_for_display(cal, lect, minor)
    return build_wheel_svg(cal, evs, lect, include_minor=minor, emblem_href="", dates=dates)


def test_default_style_is_season_ranges():
    assert DEFAULT_DATE_STYLE == "range"
    assert set(DATE_STYLES) == {"range", "rim", "all", "none"}


def test_range_style_shows_each_season_first_to_last_day():
    svg = _svg("range")
    # 2025-26: Ash Wednesday 18 Feb; Palm Sunday 29 Mar; Easter 5 Apr.
    for rng in ("30 NOV – 23 DEC", "24 DEC – 5 JAN", "6 JAN – 17 FEB",
                "18 FEB – 28 MAR", "29 MAR – 4 APR", "5 APR – 23 MAY"):
        assert rng in svg, rng
    # The last season runs to the Saturday before the next Advent (29 Nov 2026).
    assert "31 MAY – 28 NOV" in svg


def test_range_style_one_year_names_season_after_trinity():
    svg = _svg("range", lect="one_year")
    assert "SEASON AFTER TRINITY" in svg
    assert "1 FEB – 17 FEB" in svg          # Pre-Lent (the Gesimas)
    # The range follows the band as drawn.  In the one-year data Trinity Sunday
    # and the Last Sunday of the Church Year carry season "Ordinary Time", so
    # each is its own small unlabelled band either side of Trinity season.
    assert "7 JUN – 21 NOV" in svg


def test_rim_style_marks_each_season_start_outside_the_wheel():
    svg = _svg("rim")
    for d in ("Nov 30", "Dec 24", "Jan 6", "Feb 18", "Mar 29", "Apr 5", "May 24", "May 31"):
        assert f">{d}</text>" in svg, d
    assert 'viewBox="0 0 1100 1150"' in svg   # room for the dates
    assert "18 FEB" not in svg                 # no band ranges in this style


def test_all_style_puts_the_date_on_every_day():
    svg = _svg("all")
    assert ">Feb 18</tspan>" in svg and "Ash Wednesday" in svg
    assert ">Nov 30</tspan>" in svg
    assert svg.count('font-weight="bold" opacity="0.85"') == len(
        _events_for_display(get_calendar(2025), "three_year", False))


def test_none_style_has_no_dates():
    svg = _svg("none")
    assert "18 FEB" not in svg and "Feb 18" not in svg
    assert 'viewBox="0 0 1000 1090"' in svg


def test_unknown_style_falls_back_to_default():
    assert _svg("bogus") == _svg(DEFAULT_DATE_STYLE)


@pytest.mark.parametrize("year", [1583, 1700, 1999, 2025, 2299])
@pytest.mark.parametrize("lect", ["three_year", "one_year"])
@pytest.mark.parametrize("dates", ["range", "rim", "all", "none"])
def test_every_style_builds_across_the_range(year, lect, dates):
    for minor in (False, True):
        assert _svg(dates, year=year, lect=lect, minor=minor).startswith("<svg")


def test_wheel_page_defaults_to_ranges_and_offers_all_styles(client):
    r = client.get("/wheel?year=2025&lectionary=three_year")
    assert r.status_code == 200
    assert b"18 FEB \xe2\x80\x93 28 MAR" in r.data
    for val in DATE_STYLES:
        assert f'value="{val}"'.encode() in r.data
    # The downloads carry the chosen style.
    assert b"/wheel.png?year=2025&lectionary=three_year&minor=0&dates=range" in r.data
    assert b"lcms_wheel_dates" in r.data


def test_wheel_routes_honor_dates_param(client):
    r = client.get("/wheel.svg?year=2025&lectionary=three_year&dates=rim")
    assert r.status_code == 200 and b">Feb 18</text>" in r.data
    r = client.get("/wheel.svg?year=2025&lectionary=three_year&dates=none")
    assert b"18 FEB" not in r.data
    r = client.get("/wheel?year=2025&dates=nonsense")
    assert r.status_code == 200 and b"18 FEB \xe2\x80\x93 28 MAR" in r.data


def test_settings_page_has_wheel_dates_choice(client):
    r = client.get("/settings")
    assert b'name="set-wheeldates"' in r.data
    assert b"lcms_wheel_dates" in r.data
