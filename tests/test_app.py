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


def test_propers_page_includes_principal_festivals(client):
    # Reformation, All Saints, St. Michael, Thanksgiving carry One-Year propers
    # but aren't standalone events — they appear in a Festivals section.
    r = client.get("/propers?year=2026")
    assert r.status_code == 200
    assert b"Festivals" in r.data
    assert b"Reformation Day" in r.data
    assert b"St. Michael" in r.data
    assert b"All Saints" in r.data
    assert b"pour out, we beseech Thee, Thy Holy Spirit" in r.data  # Reformation collect


def test_propers_page_uses_one_year_readings(client):
    # Regression: the propers page must show the One-Year historic pericope,
    # not the Three-Year reading for the same slot. Advent 1 one-year Gospel is
    # Matthew 21:1-9 (not the three-year Mark/Luke), OT Jeremiah 23 (not Isaiah).
    r = client.get("/propers?year=2026")
    assert r.status_code == 200
    assert b"Jeremiah 23:5-8" in r.data
    assert b"Matthew 21:1-9" in r.data
    assert b"Isaiah 64:1-9" not in r.data      # three-year Series B Advent 1 OT
    # CSB 1917 introit antiphon text + gradual now render inline
    assert b"introit-text-block" in r.data
    assert b"gradual-text-block" in r.data
    assert b"Common Service Book" in r.data


def test_lookup_shows_csb_introit_text(client):
    # Advent 2 (Dec 7, 2025), one-year — Populus Sion introit antiphon + gradual
    r = client.get("/lookup?date=2025-12-07&lectionary=one_year")
    assert r.status_code == 200
    assert b"introit-text" in r.data
    assert b"gradual-text" in r.data
    assert b"DAUGHTER of Zion" in r.data          # PD antiphon text from CSB 1917
    assert b"Common Service Book" in r.data
    # the invariant Gloria Patri is not reproduced in the stored antiphon
    assert b"as it was in the beginning, is now" not in r.data


def test_api_day(client):
    r = client.get("/api/day/2026-06-07?lectionary=one_year")
    assert r.status_code == 200
    data = r.get_json()
    assert data["name"] == "First Sunday after Trinity"
    assert data["date"] == "2026-06-07"

    assert client.get("/api/day/bogus").status_code == 400


def test_api_version(client):
    r = client.get("/api/version")
    assert r.status_code == 200
    data = r.get_json()
    assert "version" in data
    assert isinstance(data["version"], str) and data["version"]


def test_footer_shows_version(client):
    # The running version is rendered into the footer on every page.
    assert b'id="app-version"' in client.get("/").data


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


def test_almanac_hub(client):
    r = client.get("/almanac")
    assert r.status_code == 200
    assert b"Moon Phases" in r.data
    assert b'href="/almanac/moon"' in r.data
    # linked in the nav
    assert b'href="/almanac"' in client.get("/").data


def test_almanac_moon_page(client):
    r = client.get("/almanac/moon?year=2026")
    assert r.status_code == 200
    assert b"Moon Phases" in r.data
    assert b"Full moon" in r.data
    assert b"<svg" in r.data                       # phase icons render
    assert b"Blue moon" in r.data                  # 2026 has one (May 31)
    assert b"Paschal full moon" in r.data          # eccl-vs-astro panel
    assert b"April 5, 2026" in r.data              # Easter 2026


def test_almanac_moon_year_clamped(client):
    r = client.get("/almanac/moon?year=99999")
    assert r.status_code == 200
    r = client.get("/almanac/moon?year=notayear")
    assert r.status_code == 200


def test_almanac_easter_compare(client):
    r = client.get("/almanac/easter?start=2026&end=2026&mode=compare")
    assert r.status_code == 200
    assert b"April 5" in r.data      # Western Easter 2026
    assert b"April 12" in r.data     # Eastern Easter 2026
    assert b"+7" in r.data           # the gap


def test_almanac_easter_coincidence(client):
    # 2025 is a rare year when West and East agree (both April 20).
    r = client.get("/almanac/easter?start=2025&end=2025&mode=compare")
    assert b"coincide" in r.data
    assert b"same" in r.data


def test_almanac_easter_western_feasts(client):
    r = client.get("/almanac/easter?start=2026&end=2026&mode=western")
    assert r.status_code == 200
    assert b"Ash Wednesday" in r.data
    assert b"Pentecost" in r.data
    assert b"February 18" in r.data   # Ash Wednesday 2026


def test_almanac_easter_span_capped(client):
    r = client.get("/almanac/easter?start=2000&end=9999&mode=compare")
    assert r.status_code == 200       # span clamped, no error


def test_almanac_moon_ancient_year(client):
    # AD 33: Julian calendar, the Paschal-Controversy retrojection note, and the
    # accuracy caveat all appear.
    r = client.get("/almanac/moon?year=33")
    assert r.status_code == 200
    assert b"Julian calendar" in r.data
    assert b"approximate" in r.data
    assert b"Paschal Controversy" in r.data


def test_daily_page(client):
    r = client.get("/daily?year=2025")
    assert r.status_code == 200
    assert b"Proverbs 9:1-18" in r.data        # June 11, 2026
    assert b"Isaiah 1:1-28" in r.data          # first day of church year


def test_daily_pdf(client):
    r = client.get("/daily/pdf?year=2025")
    assert r.status_code == 200
    assert r.data[:5] == b"%PDF-"


def test_lookup_minor_feast_readings_clickable(client):
    # June 11, 2026 = St. Barnabas; banner should include scripture links
    r = client.get("/lookup?date=2026-06-11&lectionary=three_year")
    assert r.status_code == 200
    assert b"St. Barnabas" in r.data
    assert b"minor-feast-readings" in r.data


def test_calendar_has_historic_colors_toggle(client):
    checkbox = b'<input type="checkbox" id="historic-colors-toggle">'
    r = client.get("/calendar?year=2025&lectionary=one_year")
    assert checkbox in r.data
    # not offered for three-year
    r = client.get("/calendar?year=2025&lectionary=three_year")
    assert checkbox not in r.data


def test_settings_page(client):
    r = client.get("/settings")
    assert r.status_code == 200
    assert b"set-lectionary" in r.data
    assert b"set-advent" in r.data
    assert b"set-translation" in r.data


def test_settings_in_nav(client):
    r = client.get("/")
    assert b'href="/settings"' in r.data


def test_propers_pdf(client):
    r = client.get("/propers/pdf?year=2025")
    assert r.status_code == 200
    assert r.data[:5] == b"%PDF-"


def test_day_pdf(client):
    # One-year single-day propers sheet
    r = client.get("/day/2025-12-07/pdf?lectionary=one_year")
    assert r.status_code == 200
    assert r.data[:5] == b"%PDF-"
    # Three-year variant
    r = client.get("/day/2026-06-07/pdf?lectionary=three_year")
    assert r.status_code == 200
    assert r.data[:5] == b"%PDF-"
    # Bad date 404s
    assert client.get("/day/not-a-date/pdf").status_code == 404
    # The lookup card exposes both PDF buttons (default card + plain document)
    r = client.get("/lookup?date=2025-12-07&lectionary=one_year")
    assert b"/day/2025-12-07/pdf" in r.data
    assert b"style=document" in r.data


def test_day_pdf_styles(client):
    # Card is the default style; ?style=document renders the plain sheet.
    for lect in ("one_year", "three_year"):
        for suffix in ("", "&style=card", "&style=document"):
            r = client.get(f"/day/2026-06-07/pdf?lectionary={lect}{suffix}")
            assert r.status_code == 200
            assert r.data[:5] == b"%PDF-"


def test_about_page(client):
    r = client.get("/about")
    assert r.status_code == 200
    assert b"Common Service Book" in r.data
    assert b"Calendar Explorer" in r.data
    # About is linked in the nav
    assert b'href="/about"' in client.get("/").data


def test_day_pdf_citation_is_conditional():
    # The 1917 (CSB) source must only be cited where those texts actually appear —
    # i.e. the one-year series, never the three-year (which carries no introit/collect/gradual).
    from pdf_gen import _day_citation
    one_year = {"introit": {"name": "x"}, "collect": "y", "gradual": "z"}
    three_year = {"introit": None, "collect": None, "gradual": None}
    assert "Common Service Book" in _day_citation(one_year, "one_year")
    assert "Common Service Book" not in _day_citation(three_year, "three_year")
    assert "Lutheran Service Book" in _day_citation(three_year, "three_year")


def test_ical_includes_propers_and_daily(client):
    r = client.get("/export/ical?year=2025&lectionary=one_year")
    assert r.status_code == 200
    assert b"Introit:" in r.data
    assert b"Collect:" in r.data
    assert b"Daily Lectionary:" in r.data
    # daily events not present without the flag
    assert b"-daily@lectionary" not in r.data


def test_ical_daily_events_flag(client):
    r = client.get("/export/ical?year=2025&lectionary=one_year&daily=1")
    assert r.status_code == 200
    assert b"-daily@lectionary" in r.data
    assert b"TRANSP:TRANSPARENT" in r.data


def test_hymn_of_the_day_in_pages_and_api(client):
    r = client.get("/lookup?date=2026-06-07&lectionary=one_year")
    assert b"Hymn of the Day" in r.data
    assert b"LSB 768" in r.data          # Trinity 1, one-year

    r = client.get("/api/day/2026-06-07?lectionary=one_year")
    assert r.get_json()["hymn_of_the_day"][0].startswith("LSB 768")

    # calendar expand row includes the hymn (one-year)
    r = client.get("/calendar?year=2025&lectionary=one_year")
    assert b"Hymn of the Day:" in r.data
