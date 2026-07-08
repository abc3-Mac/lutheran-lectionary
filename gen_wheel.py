#!/usr/bin/env python3
"""
gen_wheel.py — render the Liturgical Year wheel as a poster file.

The SVG engine (``liturgical_calendar.wheel``) is the single source of truth;
this CLI writes the SVG and, when a Chrome/Chromium binary is available,
rasterises it to PNG and/or PDF via headless Chrome — the same pipeline used
for the project's infographics.  No extra Python dependencies.

Examples
--------
    # 2025-2026, three-year, PNG + SVG (default) into ./out
    python3 gen_wheel.py

    # one-year historic, PDF poster for 2026-2027
    python3 gen_wheel.py --year 2026 --lectionary one_year --format pdf

    # everything, include minor feasts, custom size
    python3 gen_wheel.py --format all --minor --scale 2
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date

from liturgical_calendar.calculator import LiturgicalCalendar
from liturgical_calendar.wheel import build_wheel_svg

_CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]


def _find_chrome() -> str | None:
    for c in _CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def _svg_size(svg: str) -> tuple[int, int]:
    """Pull the intrinsic width/height (or viewBox) off the SVG root."""
    import re
    w = re.search(r'\bwidth="([\d.]+)"', svg)
    h = re.search(r'\bheight="([\d.]+)"', svg)
    if w and h:
        return round(float(w.group(1))), round(float(h.group(1)))
    vb = re.search(r'viewBox="[\d.\s]*?([\d.]+)\s+([\d.]+)"', svg)
    if vb:
        return round(float(vb.group(1))), round(float(vb.group(2)))
    return 1000, 1000


def _rasterize(svg_path: str, out_path: str, kind: str, w: int, h: int, chrome: str) -> None:
    """Render an SVG file to PNG or PDF using headless Chrome, keeping aspect."""
    wrap = os.path.join(os.path.dirname(svg_path), "_wrap_wheel.html")
    svg_name = os.path.basename(svg_path)
    with open(wrap, "w", encoding="utf-8") as fh:
        fh.write(
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<style>html,body{margin:0;padding:0;background:#f6f1e7}"
            f"img{{display:block;width:{w}px;height:{h}px}}</style></head>"
            f"<body><img src='{svg_name}'></body></html>"
        )
    common = [
        chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-sandbox", "--force-device-scale-factor=1",
    ]
    url = f"file://{os.path.abspath(wrap)}"
    if kind == "png":
        cmd = common + [f"--window-size={w},{h}", f"--screenshot={out_path}", url]
    else:  # pdf
        cmd = common + [f"--print-to-pdf={out_path}", "--no-pdf-header-footer", url]
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        os.remove(wrap)
    except OSError:
        pass


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Render the Liturgical Year wheel poster.")
    ap.add_argument("--year", type=int, default=None,
                    help="Advent year the church year begins (default: current).")
    ap.add_argument("--lectionary", choices=["three_year", "one_year"],
                    default="three_year")
    ap.add_argument("--format", choices=["svg", "png", "pdf", "all"], default="png",
                    help="Output format(s). SVG is always written.")
    ap.add_argument("--minor", action="store_true", help="Include minor feasts.")
    ap.add_argument("--scale", type=float, default=2.0,
                    help="Raster size multiplier of the 1000px base (PNG/PDF).")
    ap.add_argument("--out", default="out", help="Output directory.")
    args = ap.parse_args(argv)

    year = args.year
    if year is None:
        today = date.today()
        # current church year: Advent of this civil year, else last year
        from liturgical_calendar.calculator import advent1_for_year
        year = today.year if today >= advent1_for_year(today.year) else today.year - 1

    cal = LiturgicalCalendar(year)
    events = cal.all_events(include_minor=args.minor, lectionary=args.lectionary)
    svg = build_wheel_svg(cal, events, args.lectionary, include_minor=args.minor)

    os.makedirs(args.out, exist_ok=True)
    stem = f"Liturgical_Year_Wheel_{year}-{year + 1}_{args.lectionary}"
    svg_path = os.path.join(args.out, stem + ".svg")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote {svg_path}")

    want = {"svg": {"svg"}, "png": {"png"}, "pdf": {"pdf"},
            "all": {"png", "pdf"}}[args.format]
    raster = want - {"svg"}
    if raster:
        chrome = _find_chrome()
        if not chrome:
            print("! No Chrome/Chromium found — wrote SVG only. "
                  "Install Chrome or convert the SVG in Affinity Designer.",
                  file=sys.stderr)
            return 0
        base_w, base_h = _svg_size(svg)
        w = int(base_w * args.scale)
        h = int(base_h * args.scale)
        for kind in ("png", "pdf"):
            if kind in raster:
                out_path = os.path.join(args.out, stem + f".{kind}")
                _rasterize(svg_path, out_path, kind, w, h, chrome)
                print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
