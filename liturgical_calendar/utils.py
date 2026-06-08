"""Utility helpers for display, BibleGateway links, and file naming."""

import re
from urllib.parse import quote


ORDINALS = [
    "", "First", "Second", "Third", "Fourth", "Fifth",
    "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
    "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth",
    "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth",
    "Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth",
    "Twenty-fifth", "Twenty-sixth", "Twenty-seventh",
]


def ordinal(n: int) -> str:
    return ORDINALS[n] if 0 < n < len(ORDINALS) else str(n)


def bg_url(reference: str, version: str = "ESV") -> str:
    """Return a BibleGateway URL for a scripture reference."""
    if not reference:
        return "#"
    ref_clean = reference.strip()
    return f"https://www.biblegateway.com/passage/?search={quote(ref_clean)}&version={version}"


def parse_readings(readings: dict | None) -> list[dict]:
    """
    Convert a readings dict {ot, ps, ep, go} into a list of
    {label, ref, url} dicts, handling '|' alternatives.
    """
    if not readings:
        return []
    label_map = {"ot": "First Reading", "ps": "Psalm", "ep": "Epistle", "go": "Gospel"}
    result = []
    for key, label in label_map.items():
        val = readings.get(key)
        if not val:
            continue
        # Handle alternative readings split by ' | '
        parts = [p.strip() for p in val.split(" | ")]
        primary = parts[0]
        alts    = parts[1:]
        result.append({
            "label":    label,
            "ref":      primary,
            "alts":     alts,
            "url":      bg_url(primary),
            "alt_urls": [bg_url(a) for a in alts],
        })
    return result


def safe_filename(text: str) -> str:
    """Make a string safe for use in a filename."""
    text = text.replace("/", "-").replace("\\", "-")
    text = re.sub(r'[<>:"|?*]', "", text)
    return text.strip()


def file_label(d, name: str) -> str:
    """
    Return a filename-safe label:
        2026-06-07 Second Sunday after Pentecost
    """
    return safe_filename(f"{d.strftime('%Y-%m-%d')} {name}")


def season_color_class(color: str) -> str:
    """Map liturgical color name to a CSS class."""
    mapping = {
        "Blue":    "season-blue",
        "White":   "season-white",
        "Red":     "season-red",
        "Green":   "season-green",
        "Purple":  "season-purple",
        "Black":   "season-black",
        "Scarlet": "season-red",
    }
    return mapping.get(color, "season-green")
