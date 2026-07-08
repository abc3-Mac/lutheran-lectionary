"""
rasterize.py — server-side SVG → PNG rendering.

Renders the wheel SVG to PNG bytes so the browser only ever downloads a plain
image file (works identically on every browser/device, including iOS Safari).

Backend preference:
    1. resvg                    — the container's renderer (pip: resvg-cli)
    2. headless Chrome/Chromium — local-dev fallback (matches gen_wheel.py)

Both handle every feature the wheel uses: <textPath> (season labels + motto),
embedded data-URI images, and preserveAspectRatio.  librsvg is deliberately
NOT used: rsvg-convert 2.62 silently drops <textPath>, so the season names and
the central motto would vanish.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile

_CHROME_APP = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _which(*names: str) -> str | None:
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def _dimensions(svg: str, width: int) -> tuple[int, int]:
    """Target (w, h) preserving the SVG's aspect ratio."""
    w = re.search(r'\bwidth="([\d.]+)"', svg)
    h = re.search(r'\bheight="([\d.]+)"', svg)
    if w and h:
        ratio = float(h.group(1)) / float(w.group(1))
    else:
        vb = re.search(r'viewBox="[\d.\s]*?([\d.]+)\s+([\d.]+)"', svg)
        ratio = (float(vb.group(2)) / float(vb.group(1))) if vb else 1.0
    return width, round(width * ratio)


def _resvg_bin() -> str | None:
    """resvg on PATH (the pip `resvg-cli` package installs a `resvg` binary)."""
    return _which("resvg")


def available_backend() -> str | None:
    """Name of the renderer that will be used, or None if none is available."""
    if _resvg_bin():
        return "resvg"
    if _which("google-chrome", "chromium", "chromium-browser") or os.path.exists(_CHROME_APP):
        return "chrome"
    return None


def svg_to_png(svg: str, width: int = 3000) -> bytes:
    """Rasterize an SVG string to PNG bytes at the given pixel width."""
    w, h = _dimensions(svg, width)
    resvg = _resvg_bin()
    if resvg:
        return _run_file(
            [resvg, "--width", str(w), "--height", str(h), "{in}", "{out}"], svg
        )
    chrome = _which("google-chrome", "chromium", "chromium-browser") or (
        _CHROME_APP if os.path.exists(_CHROME_APP) else None
    )
    if chrome:
        return _run_chrome(chrome, svg, w, h)
    raise RuntimeError(
        "No SVG rasterizer available (install librsvg2-bin, resvg, or Chrome)."
    )


def _run_file(cmd_template: list[str], svg: str) -> bytes:
    """Run a converter that takes an input SVG file and writes an output PNG."""
    with tempfile.TemporaryDirectory() as d:
        inp = os.path.join(d, "wheel.svg")
        out = os.path.join(d, "wheel.png")
        with open(inp, "w", encoding="utf-8") as fh:
            fh.write(svg)
        cmd = [p.replace("{in}", inp).replace("{out}", out) for p in cmd_template]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        with open(out, "rb") as fh:
            return fh.read()


def _run_chrome(chrome: str, svg: str, w: int, h: int) -> bytes:
    """Headless-Chrome fallback (dev only): wrap the SVG and screenshot it."""
    with tempfile.TemporaryDirectory() as d:
        svg_path = os.path.join(d, "wheel.svg")
        wrap = os.path.join(d, "wrap.html")
        out = os.path.join(d, "wheel.png")
        with open(svg_path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        with open(wrap, "w", encoding="utf-8") as fh:
            fh.write(
                "<!doctype html><meta charset='utf-8'>"
                "<style>html,body{margin:0;padding:0;background:#f6f1e7}"
                f"img{{display:block;width:{w}px;height:{h}px}}</style>"
                "<img src='wheel.svg'>"
            )
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--no-sandbox", "--force-device-scale-factor=1",
             f"--window-size={w},{h}", f"--screenshot={out}", f"file://{wrap}"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(out, "rb") as fh:
            return fh.read()
