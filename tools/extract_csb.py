"""
One-off extraction tool — NOT part of the running app.

Parses the public-domain Common Service Book of the Lutheran Church (1917)
propers text (sources/CSB-1917-propers.txt, an OCR-corrected compilation) into
structured per-day blocks: introit (antiphon + psalm verse + Gloria), collect,
and gradual.

Then joins each block to the app's existing ONE_YEAR_PROPERS slots by fuzzy-
matching the stored collect text (the stored collects are already known-good,
so they make a reliable join key). Emits:
  - sources/csb_blocks.json     all parsed CSB blocks
  - sources/csb_audit.json      per-slot: stored vs CSB collect + match score

Run:  python tools/extract_csb.py
"""

import json
import os
import re
import sys
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources", "CSB-1917-propers.txt")

sys.path.insert(0, ROOT)
from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS

MARKERS = ("INTROIT", "COLLECT", "GRADUAL", "TRACT", "EPISTLE", "GOSPEL")


def norm(s: str) -> str:
    """Normalize for fuzzy text comparison: lowercase, collapse whitespace,
    strip punctuation/OCR specks so spacing and stray dots don't mask matches."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_marker(line: str) -> str | None:
    """Return the marker keyword if this line opens a propers section.
    Tolerant of OCR punctuation variants, e.g. 'EPISTLE,' / 'EPISTLE.' / 'GOSPEL '."""
    for m in MARKERS:
        if line == m or re.match(rf"^{m}[\s.,:;]", line):
            return m
    return None


def looks_like_title(line: str) -> bool:
    """A day title: short, not a marker, not body text (no terminal Amen/colon)."""
    if not line or is_marker(line):
        return False
    if line.rstrip().endswith(("Amen.", "Hallelujah.", ":", ";")):
        return False
    if line.lstrip().startswith(("V.", "Verse", "Psalm.", "Glory be", "Or:", "For ")):
        return False
    return len(line) <= 60


def is_subtitle(line: str) -> bool:
    """A sub-heading under a title, e.g. 'For an early service', 'Whitsunday'."""
    return bool(line) and line.startswith(("For ", "Whitsunday")) and len(line) <= 40


def is_submass(line: str) -> bool:
    """A roman-numeral marker introducing a second mass under the same day."""
    return line in ("II", "III")


def parse_blocks(lines: list[str]) -> list[dict]:
    """Split the text into day-blocks. A block begins at a title line that is
    immediately (within 1 blank line) followed by a section marker or a
    'the same as' cross-reference."""
    # Find block-start indices. A block begins at either:
    #   (a) a title line whose next marker is reached past 0+ subtitle lines, or
    #   (b) a roman-numeral sub-mass line ('II') — a second mass under the day.
    starts = []           # list of (index, title_override_or_None)
    last_title = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if is_submass(s):
            starts.append((i, f"{last_title} — later service" if last_title else s))
            continue
        if not looks_like_title(s):
            continue
        # peek forward past blanks and subtitle lines for a section marker
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or is_subtitle(lines[j].strip())):
            j += 1
        if j >= len(lines):
            continue
        nxt = lines[j].strip()
        # A new day-block only ever OPENS with the Introit or Collect (or a
        # 'same as' cross-ref). Lines followed by GRADUAL/EPISTLE/GOSPEL/TRACT
        # are mid-section content tails (e.g. '...lusts thereof.'), not titles.
        if is_marker(nxt) in ("INTROIT", "COLLECT") or \
                nxt.startswith(("The INTROIT", "INTROIT", "The COLLECT")):
            starts.append((i, None))
            last_title = s
    starts.append((len(lines), None))

    blocks = []
    for k in range(len(starts) - 1):
        i0 = starts[k][0]
        i1 = starts[k + 1][0]
        title = starts[k][1] or lines[i0].strip()
        body = lines[i0 + 1:i1]
        blocks.append({"title": title, "raw": body,
                       **extract_sections(body)})
    return blocks


def extract_sections(body: list[str]) -> dict:
    """Pull INTROIT / COLLECT / GRADUAL text out of a block body."""
    sections = {"introit": None, "collect": None, "gradual": None,
                "same_as": None}
    cur = None
    buckets = {"INTROIT": [], "COLLECT": [], "GRADUAL": [], "_DROP": []}
    for ln in body:
        s = ln.strip()
        # cross-reference, e.g. "INTROIT and COLLECT the same as for Christmas Day."
        if "same as" in s.lower():
            sections["same_as"] = s
            cur = "_DROP"
            continue
        m = is_marker(s)
        if m:
            if m in ("EPISTLE", "GOSPEL", "TRACT"):
                cur = "_DROP"          # readings handled elsewhere; ignore text
            else:
                cur = m
            continue
        if cur and cur != "_DROP":
            buckets[cur].append(s)
    if buckets["INTROIT"]:
        sections["introit"] = "\n".join(x for x in buckets["INTROIT"] if x).strip()
    if buckets["COLLECT"]:
        sections["collect"] = " ".join(x for x in buckets["COLLECT"] if x).strip()
    if buckets["GRADUAL"]:
        sections["gradual"] = "\n".join(x for x in buckets["GRADUAL"] if x).strip()
    return sections


def best_match(stored_collect: str, blocks: list[dict]) -> tuple[dict | None, float]:
    """Find the CSB block whose collect best matches the stored collect."""
    target = norm(stored_collect)
    best, score = None, 0.0
    for b in blocks:
        if not b.get("collect"):
            continue
        r = SequenceMatcher(None, target, norm(b["collect"])).ratio()
        if r > score:
            best, score = b, r
    return best, score


def clean_introit(text: str) -> str | None:
    """Antiphon + psalm verse only — drop the invariant Gloria Patri and any
    'Or,' alternate. Collapse OCR line-wraps into flowing text."""
    if not text:
        return None
    kept = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("Glory be to the Father") or s == "Or," or s == "Or":
            break
        if s:
            kept.append(s)
    out = re.sub(r"\s+", " ", " ".join(kept)).strip()
    return out or None


def clean_gradual(text: str) -> str | None:
    if not text:
        return None
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip() or None


def psalm_numbers(ref: str) -> set:
    """Extract psalm chapter numbers from a stored introit ref like
    'Psalm 25:1-3, 5' or 'Isaiah 45:8; Psalm 19:1' -> {'25','19'} (psalms only
    where labelled, else any leading chapter)."""
    nums = set(re.findall(r"Psalm\s+(\d+)", ref or ""))
    return nums


# Explicit slot -> CSB block title (substring match). Irregular cases listed;
# the regular trinity_N / epiphany_N are generated below.
SLOT_TO_CSB = {
    "advent_1": "First Sunday in Advent",
    "advent_2": "Second Sunday in Advent",
    "advent_3": "Third Sunday in Advent",
    "advent_4": "Fourth Sunday in Advent",
    "christmas_eve": "Christmas Day, The Nativity of Our Lord",       # early service
    "christmas_midnight": "Christmas Day, The Nativity of Our Lord",
    "christmas_dawn": "Christmas Day, The Nativity of Our Lord",
    "christmas_day": "later service",                                  # the 'II' block
    "christmas_sunday_1": "The First Sunday after Christmas",
    "christmas_sunday_2": "The First Sunday after Christmas",   # CSB: same propers
    "new_years_eve": "The Circumcision and Name of Jesus",
    "new_years_day": "The Circumcision and Name of Jesus",
    "epiphany": "The Epiphany of our Lord",
    "baptism_of_lord": "The First Sunday after the Epiphany",
    "transfiguration": "The Transfiguration of our Lord",
    "septuagesima": "Septuagesima Sunday",
    "sexagesima": "Sexagesima Sunday",
    "quinquagesima": "Quinquagesima Sunday",
    "ash_wednesday": "Ash Wednesday",
    "lent_1": "Invocavit",
    "lent_2": "Reminiscere",
    "lent_3": "Oculi",
    "lent_4": "Laetare",
    "lent_5": "Judica",
    "palm_sunday": "Palmarum",
    "maundy_thursday": "Thursday in Holy Week",
    "good_friday": "Good Friday",
    "easter": "Easter Day",
    "easter_2": "Quasi Modo Geniti",
    "easter_3": "Misericordias Domini",
    "easter_4": "Jubilate",
    "easter_5": "Cantate",
    "easter_6": "Rogate",
    "easter_7": "Exaudi",
    "ascension": "The Ascension of our Lord",
    "pentecost": "The Festival of Pentecost",
    "holy_trinity": "The Festival of the Holy Trinity",
    "last_sunday": "The Twenty-Seventh Sunday after Trinity",
    "reformation": "The Festival of the Reformation",
    "all_saints": "All Saints",
    "st_michael": "September 29",
}
_ORD = ["", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh",
        "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth",
        "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth", "Eighteenth",
        "Nineteenth", "Twentieth", "Twenty-First", "Twenty-Second",
        "Twenty-Third", "Twenty-Fourth", "Twenty-Fifth", "Twenty-Sixth",
        "Twenty-Seventh"]
for _n in range(1, 28):
    SLOT_TO_CSB.setdefault(f"trinity_{_n}", f"The {_ORD[_n]} Sunday after Trinity")
for _n in range(2, 6):
    SLOT_TO_CSB.setdefault(f"epiphany_{_n}", f"The {_ORD[_n]} Sunday after the Epiphany")
# epiphany 6-8 are app padding beyond CSB; fall back to Epiphany 5
for _n in range(6, 9):
    SLOT_TO_CSB.setdefault(f"epiphany_{_n}", "The Fifth Sunday after the Epiphany")


def find_block(blocks, title_sub):
    for b in blocks:
        if title_sub in b["title"]:
            return b
    return None


def resolve_same_as(blocks, b, field):
    """Follow 'the same as for X' to the referenced block's introit/gradual."""
    val = b.get(field)
    if val:
        return val
    sa = b.get("same_as") or ""
    m = re.search(r"same as for (?:the )?(.+?)(?:[.\n]|$)", sa, re.I)
    if not m:
        return None
    ref = m.group(1).strip().rstrip(".")
    # normalize 'holy week' capitalization for matching
    for b2 in blocks:
        if ref.lower() in b2["title"].lower():
            return b2.get(field)
    return None


# Slots whose CSB block the auto-parser fragments on an intervening rubric
# paragraph. Slice the raw text between these exact title lines instead.
RAW_OVERRIDES = {
    "new_years_eve":  ("The Circumcision and Name of Jesus", "COLLECT FOR NEW YEAR"),
    "new_years_day":  ("The Circumcision and Name of Jesus", "COLLECT FOR NEW YEAR"),
    "reformation":    ("The Festival of the Reformation", "All Saints’ Day"),
    "all_saints":     ("All Saints’ Day", "St. Andrew"),
    "trinity_27":     ("The Twenty-Seventh Sunday after Trinity", "Apostles’ Days"),
    "last_sunday":    ("The Twenty-Seventh Sunday after Trinity", "Apostles’ Days"),
    "thanksgiving":   ("A Day of General or Special Thanksgiving", "\x00END"),
}


def raw_slice_block(lines, start_title, end_title):
    """Build a single block from the raw text between two title lines."""
    s = e = None
    for i, ln in enumerate(lines):
        t = ln.strip()
        if s is None and t == start_title:
            s = i
        elif s is not None and t == end_title:
            e = i
            break
    if s is None:
        return None
    body = lines[s + 1:e] if e else lines[s + 1:s + 60]
    return {"title": start_title, "raw": body, **extract_sections(body)}


def build_enrichment(blocks, lines):
    from liturgical_calendar.data.one_year import ONE_YEAR_SLOTS
    enrich, report = {}, []
    for slot, data in ONE_YEAR_PROPERS.items():
        title_sub = SLOT_TO_CSB.get(slot)
        if slot in RAW_OVERRIDES:
            b = raw_slice_block(lines, *RAW_OVERRIDES[slot])
        else:
            b = find_block(blocks, title_sub) if title_sub else None
        name = ONE_YEAR_SLOTS.get(slot, {}).get("name", slot)
        intro = grad = None
        collect_ok = None
        if b:
            intro = clean_introit(resolve_same_as(blocks, b, "introit"))
            grad = clean_gradual(resolve_same_as(blocks, b, "gradual"))
            stored = data.get("collect", "")
            if b.get("collect") and stored:
                # validate the mapping: stored collect should lead the CSB block collect
                collect_ok = norm(stored)[:80] in norm(b["collect"])
        enrich[slot] = {
            "introit_text": intro,
            "gradual": grad,
            "source": f"Common Service Book of the Lutheran Church (Philadelphia, 1917), "
                      f"Introits, Collects, Epistles, Graduals and Gospels — {name}",
        }
        report.append({"slot": slot, "csb": title_sub, "found": bool(b),
                       "collect_ok": collect_ok,
                       "has_introit": bool(intro), "has_gradual": bool(grad)})
    return enrich, report


def main():
    with open(SRC, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    blocks = parse_blocks(lines)
    with_collect = [b for b in blocks if b.get("collect")]
    print(f"Parsed {len(blocks)} blocks ({len(with_collect)} with a collect).")

    out_blocks = [{k: b[k] for k in ("title", "introit", "collect", "gradual", "same_as")}
                  for b in blocks]
    with open(os.path.join(ROOT, "sources", "csb_blocks.json"), "w", encoding="utf-8") as fh:
        json.dump(out_blocks, fh, indent=2, ensure_ascii=False)

    audit = []
    for slot, data in ONE_YEAR_PROPERS.items():
        stored = data.get("collect", "")
        b, score = best_match(stored, blocks)
        audit.append({
            "slot": slot,
            "score": round(score, 3),
            "csb_title": b["title"] if b else None,
            "stored_collect": stored,
            "csb_collect": b["collect"] if b else None,
            "csb_introit": b["introit"] if b else None,
            "csb_gradual": b["gradual"] if b else None,
            "identical": norm(stored) == norm(b["collect"]) if b else False,
        })
    audit.sort(key=lambda a: a["score"])
    with open(os.path.join(ROOT, "sources", "csb_audit.json"), "w", encoding="utf-8") as fh:
        json.dump(audit, fh, indent=2, ensure_ascii=False)

    print("\nLowest-confidence collect matches (review these):")
    for a in audit[:12]:
        flag = "IDENTICAL" if a["identical"] else "DIFFERS"
        print(f"  {a['score']:.3f} {flag:9} {a['slot']:20} -> {a['csb_title']}")
    n_ident = sum(1 for a in audit if a["identical"])
    print(f"\n{n_ident}/{len(audit)} stored collects already identical to CSB (normalized).")

    enrich, report = build_enrichment(blocks, lines)
    with open(os.path.join(ROOT, "sources", "csb_enrichment.json"), "w", encoding="utf-8") as fh:
        json.dump(enrich, fh, indent=2, ensure_ascii=False)
    n_intro = sum(1 for r in report if r["has_introit"])
    n_grad = sum(1 for r in report if r["has_gradual"])
    print(f"\nEnrichment: {n_intro}/{len(report)} slots got introit text, "
          f"{n_grad}/{len(report)} got a gradual.")
    print("Slots needing attention (mapping not found / collect mismatch / no introit):")
    for r in report:
        if not r["found"] or r["collect_ok"] is False or not r["has_introit"]:
            print(f"  found={r['found']!s:5} collect_ok={r['collect_ok']!s:5} "
                  f"introit={r['has_introit']!s:5} gradual={r['has_gradual']!s:5} "
                  f"{r['slot']:18} -> {r['csb']}")


if __name__ == "__main__":
    main()
