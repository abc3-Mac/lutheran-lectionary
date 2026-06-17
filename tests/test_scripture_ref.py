"""Regression tests for the client-side scripture-popup reference handling.

Reported 2026-06-17: clicking the Gospel for the Fourth Sunday after Pentecost
("Matthew 10:5a, 21-33") showed only verse 5 — everything after the comma was
dropped. Two distinct defects in static/main.js were responsible:

  1. The ESV API splits a discontiguous reference into one passage string per
     contiguous range; main.js rendered only passages[0], losing "21-33".
  2. The half-verse suffix ("5a") 404s on bible-api.com (KJV/ASV path) and is
     silently dropped by the ESV API.

The fix added a `normalizeRef()` helper (strips half-verse letters) and renders
ALL returned passages. These tests pin both behaviours. The JS regex is mirrored
here and asserted byte-for-byte against the source, so the two cannot drift.
"""

import os
import re

MAIN_JS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "main.js"
)

# Must stay identical to the regex literal in static/main.js's normalizeRef().
NORMALIZE_PATTERN = r"(\d)[a-z]\b"


def normalize_ref(ref):
    """Python mirror of the JS normalizeRef() — strips half-verse suffixes."""
    return re.sub(NORMALIZE_PATTERN, r"\1", ref)


def read_main_js():
    with open(MAIN_JS, encoding="utf-8") as f:
        return f.read()


# --- normalizeRef behaviour ------------------------------------------------

def test_strips_half_verse_suffix_reported_case():
    # The exact reference from the bug report.
    assert normalize_ref("Matthew 10:5a, 21-33") == "Matthew 10:5, 21-33"


def test_strips_trailing_and_internal_half_verses():
    assert normalize_ref("Psalm 16:9b-11") == "Psalm 16:9-11"
    assert normalize_ref("Matthew 16:13-19a") == "Matthew 16:13-19"


def test_preserves_book_numbers_and_chapter_refs():
    # Leading book numbers ("1 John") and cross-chapter refs must be untouched.
    assert normalize_ref("1 John 5:1-5") == "1 John 5:1-5"
    assert normalize_ref("2 Timothy 4:6-8, 16-18") == "2 Timothy 4:6-8, 16-18"
    assert normalize_ref("Genesis 1:1-2:3") == "Genesis 1:1-2:3"


def test_leaves_plain_refs_unchanged():
    for ref in ("Jeremiah 20:7-13", "Romans 6:12-23", "Psalm 91:1-10 (11-16)"):
        assert normalize_ref(ref) == ref


# --- guard the source against silent regressions ---------------------------

def test_js_regex_matches_python_mirror():
    src = read_main_js()
    # The JS literal is /(\d)[a-z]\b/g — assert the same pattern is present so
    # this test and the shipped regex cannot drift apart.
    assert "(\\d)[a-z]\\b" in src


def test_js_renders_all_passages_not_just_first():
    src = read_main_js()
    # The original bug: bodyEl.textContent = passages[0].trim();
    assert "passages[0]" not in src, "ESV path regressed to rendering only the first passage"
    assert "passages.map(" in src, "ESV path should join all returned passages"


def test_js_normalizes_before_fetching():
    src = read_main_js()
    assert "function normalizeRef" in src
    # Both fetch paths must use the normalized ref, not the raw display ref.
    assert "normalizeRef(ref)" in src
