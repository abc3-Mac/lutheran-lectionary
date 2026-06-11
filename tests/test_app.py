"""Route smoke tests using the Flask test client."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_index(client):
    assert client.get("/").status_code == 200


def test_calendar_both_lectionaries(client):
    for lect in ("three_year", "one_year"):
        r = client.get(f"/calendar?year=2025&lectionary={lect}")
        assert r.status_code == 200
        assert b"First Sunday in Advent" in r.data


def test_lookup(client):
    r = client.get("/lookup?date=2026-06-07&lectionary=one_year")
    assert r.status_code == 200
    assert b"First Sunday after Trinity" in r.data


def test_day_permalink(client):
    r = client.get("/day/2026-06-07?lectionary=one_year")
    assert r.status_code == 200
    assert b"First Sunday after Trinity" in r.data
    assert b"og:title" in r.data

    assert client.get("/day/not-a-date").status_code == 404


def test_search(client):
    r = client.get("/search?q=trinity&year=2025")
    assert r.status_code == 200
    assert b"after Trinity" in r.data

    # Latin introit search (one-year propers)
    r = client.get("/search?q=rorate&year=2025")
    assert r.status_code == 200
    assert b"Rorate" in r.data


def test_propers_page(client):
    r = client.get("/propers?year=2025")
    assert r.status_code == 200
    assert b"Introit" in r.data


def test_api_day(client):
    r = client.get("/api/day/2026-06-07?lectionary=one_year")
    assert r.status_code == 200
    data = r.get_json()
    assert data["name"] == "First Sunday after Trinity"
    assert data["date"] == "2026-06-07"

    assert client.get("/api/day/bogus").status_code == 400


def test_api_calendar(client):
    r = client.get("/api/calendar/2025?lectionary=one_year")
    assert r.status_code == 200
    data = r.get_json()
    assert data["church_year"] == "2025-2026"
    assert any(ev["name"] == "First Sunday after Trinity" for ev in data["events"])

    assert client.get("/api/calendar/1000").status_code == 400


def test_ical_export(client):
    r = client.get("/export/ical?year=2025&lectionary=one_year")
    assert r.status_code == 200
    assert b"BEGIN:VCALENDAR" in r.data
