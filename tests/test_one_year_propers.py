"""Coverage tests for the One-Year propers (CSB 1917): every slot must keep a
collect + introit name/ref, and the public-domain introit antiphon text, gradual,
and source citation must be well-formed where present."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS

ALL_SLOTS = sorted(ONE_YEAR_PROPERS)


@pytest.mark.parametrize("slot", ALL_SLOTS)
def test_every_slot_has_core_propers(slot):
    """collect + introit name/ref are mandatory for every slot."""
    entry = ONE_YEAR_PROPERS[slot]
    assert entry.get("collect"), f"{slot} missing collect"
    intro = entry.get("introit") or {}
    assert intro.get("name"), f"{slot} missing introit name"
    assert intro.get("ref"), f"{slot} missing introit ref"


@pytest.mark.parametrize("slot", ALL_SLOTS)
def test_optional_fields_well_formed(slot):
    """Where introit text / gradual / source are present they are non-empty
    strings (the merge + templates render them as guarded optionals)."""
    entry = ONE_YEAR_PROPERS[slot]
    text = (entry.get("introit") or {}).get("text")
    if text is not None:
        assert isinstance(text, str) and text.strip(), f"{slot} empty introit text"
    grad = entry.get("gradual")
    if grad is not None:
        assert isinstance(grad, str) and grad.strip(), f"{slot} empty gradual"
    src = entry.get("source")
    if src is not None:
        assert "Common Service Book" in src, f"{slot} source not CSB-cited"


# CSB 1917 (this compilation) prints only two Christmas formularies (early /
# later), so the Vigil and Dawn slots have no antiphon text from it.
NO_CSB_INTROIT = {"christmas_eve", "christmas_dawn"}


def test_enrichment_coverage_high():
    """The CSB enrichment should reach every slot except the two Christmas
    formularies CSB lacks — guard against a regression that silently drops
    introit text or graduals wholesale."""
    n_text = sum(1 for s in ALL_SLOTS if (ONE_YEAR_PROPERS[s].get("introit") or {}).get("text"))
    n_grad = sum(1 for s in ALL_SLOTS if ONE_YEAR_PROPERS[s].get("gradual"))
    n_src = sum(1 for s in ALL_SLOTS if ONE_YEAR_PROPERS[s].get("source"))
    assert n_text == len(ALL_SLOTS) - len(NO_CSB_INTROIT), \
        f"expected {len(ALL_SLOTS) - len(NO_CSB_INTROIT)} introit texts, got {n_text}"
    assert n_grad >= 70, f"only {n_grad} graduals (expected ~73)"
    assert n_src == len(ALL_SLOTS), f"only {n_src}/{len(ALL_SLOTS)} have a source"


def test_christmas_vigil_dawn_have_no_mismatched_antiphon():
    """Regression guard for the Eve/Dawn bug: these keep name+ref but must NOT
    carry the midnight (Dominus Dixit) antiphon text."""
    for slot in NO_CSB_INTROIT:
        intro = ONE_YEAR_PROPERS[slot]["introit"]
        assert intro.get("name") and intro.get("ref")
        assert not intro.get("text"), f"{slot} should have no CSB antiphon text"


def test_no_unexpected_shared_antiphons():
    """Identical introit text across slots is allowed only where the propers are
    genuinely shared; catches a mis-mapping that copies one antiphon to many."""
    from collections import defaultdict
    by_text = defaultdict(list)
    for s in ALL_SLOTS:
        t = (ONE_YEAR_PROPERS[s].get("introit") or {}).get("text")
        if t:
            by_text[t].append(s)
    shared = {frozenset(v) for v in by_text.values() if len(v) > 1}
    allowed = {
        frozenset({"christmas_sunday_1", "christmas_sunday_2"}),
        frozenset({"new_years_eve", "new_years_day"}),
        frozenset({"trinity_27", "last_sunday"}),
        frozenset({"epiphany_3", "epiphany_4", "epiphany_5",
                   "epiphany_6", "epiphany_7", "epiphany_8"}),
    }
    assert shared <= allowed, f"unexpected shared antiphons: {shared - allowed}"


def test_introit_text_drops_gloria():
    """Per the chosen format: antiphon + psalm verse, no invariant Gloria Patri."""
    for s in ALL_SLOTS:
        text = (ONE_YEAR_PROPERS[s].get("introit") or {}).get("text") or ""
        assert "Glory be to the Father" not in text, f"{s} introit still has Gloria"


def test_no_legacy_tlh_only_citation_in_data():
    """Sources cite the 1917 CSB (pre-1928), not TLH 1941 as the authority."""
    for s in ALL_SLOTS:
        src = ONE_YEAR_PROPERS[s].get("source")
        if src:
            assert "1917" in src
