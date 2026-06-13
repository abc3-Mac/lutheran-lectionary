"""
One-off generator — NOT part of the running app.

Rewrites liturgical_calendar/data/sanctoral.py, adding the public-domain collect,
introit antiphon text, gradual, and source citation from the Common Service Book
of the Lutheran Church (1917) — see sources/csb_sanctoral.json (from
tools/extract_csb.py). Saints not in CSB 1917 (Holy Innocents, Confession of
St. Peter, St. Barnabas, St. Mary Magdalene) keep readings only.

Invariants after generation: name / date_str / season / color / feast / minor /
readings are unchanged for every slot; no slot added or dropped.

Run:  python tools/extract_csb.py && python tools/gen_sanctoral.py
"""

import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from liturgical_calendar.data.sanctoral import SANCTORAL_SLOTS as OLD

OUT = os.path.join(ROOT, "liturgical_calendar", "data", "sanctoral.py")
ENRICH = os.path.join(ROOT, "sources", "csb_sanctoral.json")

HEADER = '''"""
LCMS Sanctoral Calendar — Principal and Minor Feasts.

Fixed-date observances that may coincide with or displace Sundays.
Readings are per the Lutheran Service Book (LSB).

Collects, introit antiphons (antiphon + psalm verse; Gloria Patri omitted), and
graduals are from the *Common Service Book of the Lutheran Church* (Philadelphia,
1917), public domain. Apostles and Evangelists without a proper collect use the
respective CSB "common" (Apostles' Days / Evangelists' Days). Feasts not present
in CSB 1917 (Holy Innocents, Confession of St. Peter, St. Barnabas, St. Mary
Magdalene) carry readings only.
"""


def _r(ot=None, ps=None, ep=None, go=None):
    return {"ot": ot, "ps": ps, "ep": ep, "go": go}


# Key: slot name used in calculator.py / date_to_slot()
SANCTORAL_SLOTS = {
'''

ORDER = ["name", "date_str", "season", "color", "feast", "minor"]


def pystr(s, indent):
    if s is None:
        return "None"
    if len(s) <= 88 and "\n" not in s:
        return repr(s)
    pad = " " * indent
    wrapped = textwrap.wrap(s, width=84, break_long_words=False, break_on_hyphens=False)
    lines = [pad + repr(w + (" " if i < len(wrapped) - 1 else ""))
             for i, w in enumerate(wrapped)]
    return "(\n" + "\n".join(lines) + "\n" + " " * (indent - 4) + ")"


def emit_readings(r):
    parts = ", ".join(f"{k}={r.get(k)!r}" for k in ("ot", "ps", "ep", "go"))
    return f"_r({parts})"


def main():
    enrich = json.load(open(ENRICH, encoding="utf-8"))
    out = [HEADER]
    for slot, old in OLD.items():
        en = enrich.get(slot, {})
        out.append(f'    "{slot}": {{\n')
        for k in ORDER:
            if k in old:
                out.append(f'        "{k}": {old[k]!r},\n')
        out.append(f'        "readings": {emit_readings(old["readings"])},\n')
        if en.get("collect"):
            out.append(f'        "collect": {pystr(en["collect"], 12)},\n')
        if en.get("introit_text"):
            out.append(f'        "introit_text": {pystr(en["introit_text"], 12)},\n')
        if en.get("gradual"):
            out.append(f'        "gradual": {pystr(en["gradual"], 12)},\n')
        if en.get("source"):
            out.append(f'        "source": {pystr(en["source"], 12)},\n')
        out.append("    },\n")
    out.append("}\n")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("".join(out))

    import importlib
    import liturgical_calendar.data.sanctoral as m
    importlib.reload(m)
    NEW = m.SANCTORAL_SLOTS
    assert set(NEW) == set(OLD), "slot set changed!"
    for slot in OLD:
        for k in ORDER + ["readings"]:
            if k in OLD[slot]:
                assert NEW[slot].get(k) == OLD[slot][k], f"{k} changed for {slot}"
    n_col = sum(1 for s in NEW if NEW[s].get("collect"))
    print(f"Wrote {OUT}")
    print(f"  slots={len(NEW)}  collect={n_col}  "
          f"introit={sum(1 for s in NEW if NEW[s].get('introit_text'))}  "
          f"gradual={sum(1 for s in NEW if NEW[s].get('gradual'))}")
    print("  invariants OK: name/date_str/season/color/feast/minor/readings unchanged.")


if __name__ == "__main__":
    main()
