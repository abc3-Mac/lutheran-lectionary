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


def test_enrichment_coverage_high():
    """The CSB enrichment should reach almost every slot — guard against a
    regression that silently drops introit text or graduals wholesale."""
    n_text = sum(1 for s in ALL_SLOTS if (ONE_YEAR_PROPERS[s].get("introit") or {}).get("text"))
    n_grad = sum(1 for s in ALL_SLOTS if ONE_YEAR_PROPERS[s].get("gradual"))
    n_src = sum(1 for s in ALL_SLOTS if ONE_YEAR_PROPERS[s].get("source"))
    assert n_text == len(ALL_SLOTS), f"only {n_text}/{len(ALL_SLOTS)} have introit text"
    assert n_grad >= 70, f"only {n_grad} graduals (expected ~75)"
    assert n_src == len(ALL_SLOTS), f"only {n_src}/{len(ALL_SLOTS)} have a source"


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
