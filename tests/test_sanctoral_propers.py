"""Coverage tests for the sanctoral propers (CSB 1917 collects/introits/graduals).
Saints present in CSB 1917 get a collect; modern feasts absent from it keep
readings only (honest scripture-ref fallback)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from liturgical_calendar.data.sanctoral import SANCTORAL_SLOTS
from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS

# In CSB 1917; must carry a PD collect.
CSB_COVERED = [
    "st_andrew", "st_thomas", "conversion_of_st_paul", "presentation_of_lord",
    "st_matthias", "annunciation", "st_mark", "philip_and_james",
    "nativity_of_john_baptist", "st_peter_st_paul", "st_james", "st_bartholomew",
    "st_matthew", "st_michael", "st_luke", "simon_and_jude", "all_saints",
]
# Not in CSB 1917 -> readings only.
NOT_IN_CSB = ["holy_innocents", "confession_of_st_peter", "st_barnabas",
              "st_mary_magdalene"]


@pytest.mark.parametrize("slot", CSB_COVERED)
def test_covered_saints_have_pd_propers(slot):
    e = SANCTORAL_SLOTS[slot]
    assert e.get("collect"), f"{slot} missing collect"
    assert e.get("introit_text"), f"{slot} missing introit text"
    assert "1917" in (e.get("source") or ""), f"{slot} missing CSB source"
    assert "Glory be to the Father" not in e["introit_text"]


@pytest.mark.parametrize("slot", NOT_IN_CSB)
def test_uncovered_saints_have_no_fabricated_collect(slot):
    # honest fallback: no collect invented for feasts absent from CSB 1917
    assert not SANCTORAL_SLOTS[slot].get("collect"), f"{slot} should have no collect"


def test_michael_and_all_saints_match_temporal_collect():
    import re
    norm = lambda s: " ".join(re.sub(r"[^a-z ]", " ", (s or "").lower()).split())
    for slot in ("st_michael", "all_saints"):
        assert norm(SANCTORAL_SLOTS[slot]["collect"]) == norm(ONE_YEAR_PROPERS[slot]["collect"])


def test_apostles_use_common_collect():
    # apostles without a proper collect share the Apostles' Days common
    common = SANCTORAL_SLOTS["st_andrew"]["collect"]
    assert "Whom to know is everlasting life" in common
    assert SANCTORAL_SLOTS["st_thomas"]["collect"] == common
    assert SANCTORAL_SLOTS["st_james"]["collect"] == common
