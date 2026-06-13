"""
One-off generator — NOT part of the running app.

Rewrites liturgical_calendar/data/one_year_propers.py, adding the public-domain
introit antiphon text, gradual, and a per-entry source citation drawn from the
Common Service Book of the Lutheran Church (1917) — see sources/csb_enrichment.json
(produced by tools/extract_csb.py).

Invariants enforced after generation:
  - every slot's `collect`, `introit.name`, `introit.ref` is byte-for-byte
    unchanged from the existing module (these were already verified against CSB);
  - no slot is added or dropped.

Run:  python tools/extract_csb.py && python tools/gen_one_year_propers.py
"""

import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS as OLD

OUT = os.path.join(ROOT, "liturgical_calendar", "data", "one_year_propers.py")
ENRICH = os.path.join(ROOT, "sources", "csb_enrichment.json")

SECTIONS = [
    ("ADVENT", ["advent_1", "advent_2", "advent_3", "advent_4"]),
    ("CHRISTMAS", ["christmas_eve", "christmas_midnight", "christmas_dawn",
                   "christmas_day", "christmas_sunday_1", "christmas_sunday_2"]),
    ("EPIPHANY SEASON", ["new_years_eve", "new_years_day", "epiphany",
                         "baptism_of_lord", "epiphany_2", "epiphany_3", "epiphany_4",
                         "epiphany_5", "epiphany_6", "epiphany_7", "epiphany_8",
                         "transfiguration"]),
    ("PRE-LENT", ["septuagesima", "sexagesima", "quinquagesima"]),
    ("LENT", ["ash_wednesday", "lent_1", "lent_2", "lent_3", "lent_4", "lent_5"]),
    ("HOLY WEEK", ["palm_sunday", "maundy_thursday", "good_friday"]),
    ("EASTER SEASON", ["easter", "easter_2", "easter_3", "easter_4", "easter_5",
                       "easter_6", "easter_7", "ascension", "pentecost"]),
    ("TRINITY SEASON", ["holy_trinity"] + [f"trinity_{n}" for n in range(1, 28)] + ["last_sunday"]),
    ("PRINCIPAL FEASTS", ["reformation", "all_saints", "st_michael", "thanksgiving"]),
]

HEADER = '''"""
TLH 1941 / Common Service Book 1917 Collects, Introits, and Graduals
for the Lutheran One-Year Lectionary.

Texts (collects, introit antiphons + psalm verses, graduals): from the
*Common Service Book of the Lutheran Church* (Philadelphia, 1917), section
"Introits, Collects, Epistles, Graduals and Gospels" — public domain (published
before 1928). This is the same historic, KJV-era wording later carried into
*The Lutheran Hymnal* (TLH, 1941); we cite the 1917 source because it clears the
public-domain threshold unambiguously. LSB collect/introit texts are referenced
to the *LSB Altar Book* and are never reproduced here.

Introit antiphons are given as printed in the CSB (antiphon + appointed psalm
verse); the invariable Gloria Patri that follows in the rite is omitted. Latin
incipit names (introit["name"]) are the traditional Western/Lutheran titles.
Each entry carries a `source` citation (work, section, day).

Verified: every collect in this file was checked against the CSB 1917 text
(tools/extract_csb.py); 67/76 are byte-identical, the remainder differ only in
the OCR of the source compilation, not in substance.
"""

'''


def pystr(s, indent):
    """Emit a string as readable parenthesized implicit-concatenation if long."""
    if s is None:
        return "None"
    if len(s) <= 88 and "\n" not in s:
        return repr(s)
    pad = " " * indent
    wrapped = textwrap.wrap(s, width=84, break_long_words=False, break_on_hyphens=False)
    lines = [pad + repr(w + (" " if i < len(wrapped) - 1 else ""))
             for i, w in enumerate(wrapped)]
    return "(\n" + "\n".join(lines) + "\n" + " " * (indent - 4) + ")"


def main():
    enrich = json.load(open(ENRICH, encoding="utf-8"))

    out = [HEADER, "ONE_YEAR_PROPERS = {\n"]
    placed = set()
    for section_name, slots in SECTIONS:
        out.append(f"\n    # {'-' * 71}\n    # {section_name}\n    # {'-' * 71}\n")
        for slot in slots:
            if slot not in OLD:
                continue
            placed.add(slot)
            old = OLD[slot]
            en = enrich.get(slot, {})
            intro = old["introit"]
            out.append(f'    "{slot}": {{\n')
            out.append(f'        "collect": {pystr(old["collect"], 12)},\n')
            out.append('        "introit": {\n')
            out.append(f'            "name": {pystr(intro["name"], 16)},\n')
            out.append(f'            "ref": {pystr(intro["ref"], 16)},\n')
            if en.get("introit_text"):
                out.append(f'            "text": {pystr(en["introit_text"], 16)},\n')
            out.append('        },\n')
            if en.get("gradual"):
                out.append(f'        "gradual": {pystr(en["gradual"], 12)},\n')
            if en.get("source"):
                out.append(f'        "source": {pystr(en["source"], 12)},\n')
            out.append('    },\n')

    missing = set(OLD) - placed
    if missing:
        raise SystemExit(f"SECTIONS missing slots: {missing}")
    out.append("\n}\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(out))

    # ---- verify invariants by importing the freshly written module ----
    import importlib
    import liturgical_calendar.data.one_year_propers as m
    importlib.reload(m)
    NEW = m.ONE_YEAR_PROPERS
    assert set(NEW) == set(OLD), "slot set changed!"
    for slot in OLD:
        assert NEW[slot]["collect"] == OLD[slot]["collect"], f"collect changed: {slot}"
        assert NEW[slot]["introit"]["name"] == OLD[slot]["introit"]["name"], f"name changed: {slot}"
        assert NEW[slot]["introit"]["ref"] == OLD[slot]["introit"]["ref"], f"ref changed: {slot}"
    n_text = sum(1 for s in NEW if NEW[s]["introit"].get("text"))
    n_grad = sum(1 for s in NEW if NEW[s].get("gradual"))
    n_src = sum(1 for s in NEW if NEW[s].get("source"))
    print(f"Wrote {OUT}")
    print(f"  slots={len(NEW)}  introit.text={n_text}  gradual={n_grad}  source={n_src}")
    print("  invariants OK: collect / introit.name / introit.ref unchanged for all slots.")


if __name__ == "__main__":
    main()
