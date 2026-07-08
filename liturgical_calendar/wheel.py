"""
wheel.py — Render the church year as a circular "Liturgical Year" wheel (SVG).

The wheel is a radial band chart driven entirely by
``LiturgicalCalendar.all_events()``:

    * one colored wedge per liturgical event, filled with its liturgical color,
      labelled with radial text (the day's name);
    * an outer band grouping the wedges into their seasons (ADVENT, CHRISTMAS,
      EPIPHANY, LENT, HOLY WEEK, EASTER, PENTECOST, ORDINARY TIME / TRINITY);
    * a central emblem area carrying the Agnus Dei motto.

Output is a single self-contained SVG string (no external fonts or images), so
it renders natively in the browser, downloads as a vector poster, opens in
Affinity Designer, and rasterises to PNG/PDF via headless Chrome.

The renderer is lectionary-agnostic: pass the event list produced for either
``three_year`` or ``one_year`` and it draws whatever it is given.
"""

from __future__ import annotations

import base64
import functools
import math
import os
from datetime import date
from html import escape


@functools.lru_cache(maxsize=1)
def default_emblem_data_uri() -> str | None:
    """The bundled Agnus Dei emblem as a ``data:`` URI, or None if absent."""
    path = os.path.join(os.path.dirname(__file__), "assets", "agnus-dei.png")
    try:
        with open(path, "rb") as fh:
            return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")
    except OSError:
        return None

# Liturgical-color → hex.  Kept in step with liturgical_calendar.ical_export.
try:  # pragma: no cover - trivial import guard
    from liturgical_calendar.ical_export import _COLOR_HEX as COLOR_HEX
except Exception:  # pragma: no cover
    COLOR_HEX = {
        "Blue":    "#1a4c8b",
        "White":   "#f5f5f0",
        "Red":     "#c0392b",
        "Scarlet": "#8b0000",
        "Purple":  "#6a0dad",
        "Black":   "#2c2c2c",
        "Green":   "#2e7d32",
    }

# Gold used wherever a "white" liturgical color would vanish on a light ground
# (Christmas / Easter bands, wedge borders, the central ring).
GOLD = "#b08d2f"
INK  = "#3a3128"     # warm near-black for text on light grounds
CREAM = "#f6f1e7"    # page ground, matches the printed poster

# Season → the color used for the *outer season band* (distinct from the
# per-day wedge color).  White seasons use gold so the band stays legible.
_SEASON_BAND = {
    "Advent":        "#3a4a8c",
    "Christmas":     GOLD,
    "Epiphany":      "#2e7d32",
    "Pre-Lent":      "#7a5a9e",
    "Gesima":        "#7a5a9e",
    "Lent":          "#5b2a86",
    "Holy Week":     "#7a1420",
    "Easter":        GOLD,
    "Pentecost":     "#b23a2e",
    "Trinity":       "#2e7d32",
    "Ordinary Time": "#2e7d32",
}

# Season → the wording shown on the outer band (defaults to the season name).
# The long green stretch is the Time after Pentecost / Trinity, so it is named
# rather than left blank.
_SEASON_LABEL = {
    "Ordinary Time": "Season after Pentecost",
    "Trinity":       "Season after Trinity",
    "Pre-Lent":      "Pre-Lent",
    "Gesima":        "Pre-Lent",
}


# ---------------------------------------------------------------------------
# Geometry helpers  (angle measured in degrees, 0° = 12 o'clock, clockwise)
# ---------------------------------------------------------------------------
def _polar(cx: float, cy: float, r: float, ang: float) -> tuple[float, float]:
    t = math.radians(ang - 90.0)
    return (cx + r * math.cos(t), cy + r * math.sin(t))


def _fmt(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def _annular_sector(cx, cy, r_in, r_out, a0, a1) -> str:
    """SVG path for the wedge between radii r_in..r_out and angles a0..a1."""
    laf = 1 if (a1 - a0) % 360 > 180 else 0
    x1, y1 = _polar(cx, cy, r_out, a0)
    x2, y2 = _polar(cx, cy, r_out, a1)
    x3, y3 = _polar(cx, cy, r_in, a1)
    x4, y4 = _polar(cx, cy, r_in, a0)
    return (
        f"M{_fmt(x1)},{_fmt(y1)} "
        f"A{_fmt(r_out)},{_fmt(r_out)} 0 {laf} 1 {_fmt(x2)},{_fmt(y2)} "
        f"L{_fmt(x3)},{_fmt(y3)} "
        f"A{_fmt(r_in)},{_fmt(r_in)} 0 {laf} 0 {_fmt(x4)},{_fmt(y4)} Z"
    )


def _arc_between(cx, cy, r, a_from, a_to, clockwise: bool) -> str:
    """
    Bare arc from ``a_from`` to ``a_to`` for a textPath baseline.

    ``clockwise`` picks the traversal direction (angles increase clockwise in
    this module's convention), which fixes glyph orientation: sweep the top of
    a band clockwise so text reads left-to-right; sweep the bottom
    counter-clockwise so text stays upright rather than upside-down.
    """
    span = (a_to - a_from) % 360 if clockwise else (a_from - a_to) % 360
    laf = 1 if span > 180 else 0
    sweep = 1 if clockwise else 0
    x1, y1 = _polar(cx, cy, r, a_from)
    x2, y2 = _polar(cx, cy, r, a_to)
    return f"M{_fmt(x1)},{_fmt(y1)} A{_fmt(r)},{_fmt(r)} 0 {laf} {sweep} {_fmt(x2)},{_fmt(y2)}"


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def _text_on(fill: str) -> str:
    """Readable text color for a given wedge fill."""
    return INK if _luminance(fill) > 0.6 else "#ffffff"


def _shorten(name: str, limit: int = 52) -> str:
    if len(name) <= limit:
        return name
    return name[: limit - 1].rstrip() + "…"


# ---------------------------------------------------------------------------
# Main renderer
# ---------------------------------------------------------------------------
def build_wheel_svg(
    cal,
    events: list[dict],
    lectionary: str = "three_year",
    *,
    title: str = "The Liturgical Year",
    include_minor: bool = False,
    emblem_href: str | None = None,
) -> str:
    """
    Build the wheel as an SVG string.

    Parameters
    ----------
    cal : LiturgicalCalendar
        Used only for the year label in the subtitle.
    events : list[dict]
        Output of ``LiturgicalCalendar.all_events(...)`` (or the app's enriched
        version).  Each event needs ``name``, ``season`` and ``color``.
    lectionary : str
        Only affects the subtitle wording.
    include_minor : bool
        When False, drop events flagged ``minor`` so the ring isn't overcrowded.
    emblem_href : str, optional
        URL or ``data:`` URI of a central emblem image (e.g. an Agnus Dei).
        When given it is placed in the middle of the wheel in place of the
        built-in cross-and-banner placeholder.
    """
    evs = [e for e in events if include_minor or not e.get("minor")]
    if not evs:
        raise ValueError("no events to render")

    n = len(evs)
    # Taller than wide so the wheel clears the title band on top and the
    # lectionary footer on the bottom without clipping.
    W = 1000.0
    H = 1090.0
    cx, cy = W / 2.0, 583.0

    R_band_out = 465.0
    R_band_in  = 428.0
    R_evt_out  = 422.0
    R_evt_in   = 165.0
    R_center   = 158.0
    R_motto    = 138.0

    # Radial text stays inside this window so no label runs into the band.
    LBL_IN   = R_evt_in + 12.0
    LBL_SPAN = R_evt_out - LBL_IN - 9.0
    LBL_SIZE = 10.5

    step = 360.0 / n
    start = -90.0 - step / 2.0   # centre the first wedge at the top (12 o'clock)

    parts: list[str] = []
    defs: list[str] = []

    # ---- background ----------------------------------------------------
    parts.append(f'<rect x="0" y="0" width="{_fmt(W)}" height="{_fmt(H)}" fill="{CREAM}"/>')

    # ---- event wedges + radial labels ----------------------------------
    for i, ev in enumerate(evs):
        a0 = start + i * step
        a1 = a0 + step
        fill = COLOR_HEX.get(ev.get("color", "Green"), COLOR_HEX["Green"])
        parts.append(
            f'<path d="{_annular_sector(cx, cy, R_evt_in, R_evt_out, a0, a1)}" '
            f'fill="{fill}" stroke="{CREAM}" stroke-width="1.1"/>'
        )

        # Radial label, kept upright and confined to the ring: right half reads
        # outward from the inner radius; left half is flipped 180° and reads
        # inward from the outer radius.
        mid = (a0 + a1) / 2.0
        raw = str(ev.get("name", ""))
        label = escape(_shorten(raw))
        txt_fill = _text_on(fill)
        left = (mid % 360) > 180
        if not left:
            bx, by = _polar(cx, cy, LBL_IN, mid)
            rot, anchor = mid - 90, "start"
        else:
            bx, by = _polar(cx, cy, R_evt_out - 9, mid)
            rot, anchor = mid + 90, "start"
        # Compress only the labels that would otherwise overrun the ring so
        # nothing collides with the outer season band.
        est = len(label) * LBL_SIZE * 0.5
        tl = f' textLength="{_fmt(LBL_SPAN)}" lengthAdjust="spacingAndGlyphs"' if est > LBL_SPAN else ""
        parts.append(
            f'<text x="{_fmt(bx)}" y="{_fmt(by)}" transform="rotate({_fmt(rot)} {_fmt(bx)} {_fmt(by)})" '
            f'text-anchor="{anchor}" dominant-baseline="middle"{tl} '
            f'font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" font-size="{LBL_SIZE}" '
            f'fill="{txt_fill}">{label}</text>'
        )

    # ---- outer season band ---------------------------------------------
    # Contiguous runs of the same season -> one arc segment + curved label.
    seg_start = 0
    for i in range(1, n + 1):
        if i == n or evs[i].get("season") != evs[seg_start].get("season"):
            season = evs[seg_start].get("season", "")
            a0 = start + seg_start * step
            a1 = start + i * step
            band = _SEASON_BAND.get(season, "#6b6b6b")
            parts.append(
                f'<path d="{_annular_sector(cx, cy, R_band_in, R_band_out, a0, a1)}" '
                f'fill="{band}" stroke="{CREAM}" stroke-width="1.4"/>'
            )
            # Curved season label centred on the band.  On the top half sweep
            # clockwise; on the bottom half sweep counter-clockwise so the text
            # stays upright instead of upside-down.
            mid = (a0 + a1) / 2.0
            r_lbl = (R_band_in + R_band_out) / 2.0
            label_text = _SEASON_LABEL.get(season, season).upper()
            # Skip the label when the arc is too short to hold it (e.g. the lone
            # Day of Pentecost wedge) so it doesn't smear across neighbours.
            arc_len = r_lbl * math.radians(a1 - a0)
            text_w = len(label_text) * 8.6 + 2 * (len(label_text) - 1)
            if text_w <= arc_len * 0.95:
                if 90 < (mid % 360) < 270:
                    arc = _arc_between(cx, cy, r_lbl + 4, a1 - 1.5, a0 + 1.5, clockwise=False)
                else:
                    arc = _arc_between(cx, cy, r_lbl - 4, a0 + 1.5, a1 - 1.5, clockwise=True)
                pid = f"seasonarc{seg_start}"
                defs.append(f'<path id="{pid}" d="{arc}" fill="none"/>')
                label = escape(label_text)
                band_txt = _text_on(band)
                parts.append(
                    f'<text font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" '
                    f'font-size="15" letter-spacing="2" font-weight="600" fill="{band_txt}">'
                    f'<textPath href="#{pid}" xlink:href="#{pid}" startOffset="50%" text-anchor="middle">{label}</textPath></text>'
                )
            seg_start = i

    # ---- thin gold rules framing the event ring ------------------------
    for r in (R_evt_in - 3, R_evt_out + 3, R_band_out + 2):
        parts.append(
            f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r)}" '
            f'fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="0.8"/>'
        )

    # ---- central emblem + motto ----------------------------------------
    parts.append(
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(R_center)}" '
        f'fill="{CREAM}" stroke="{GOLD}" stroke-width="2"/>'
    )
    # Motto around the centre (full circle, starting at the top).
    motto_path = (
        f"M {_fmt(cx)},{_fmt(cy - R_motto)} "
        f"A {_fmt(R_motto)},{_fmt(R_motto)} 0 1 1 {_fmt(cx - 0.01)},{_fmt(cy - R_motto)}"
    )
    defs.append(f'<path id="mottoarc" d="{motto_path}" fill="none"/>')
    parts.append(
        '<text font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" font-style="italic" '
        f'font-size="15" letter-spacing="1" fill="{INK}">'
        '<textPath href="#mottoarc" xlink:href="#mottoarc" startOffset="50%" text-anchor="middle">'
        'Behold, the Lamb of God, who takes away the sin of the world'
        '</textPath></text>'
    )
    # Central emblem: a supplied image (e.g. an Agnus Dei) sized to sit *inside*
    # the motto ring, else the built-in cross-and-banner placeholder.
    if emblem_href is None:
        emblem_href = default_emblem_data_uri()
    if emblem_href:
        r_img = R_motto - 18
        href = escape(emblem_href)
        # Both href and xlink:href so the emblem survives <img>-based
        # rasterization (client-side PNG export) across browsers.
        parts.append(
            f'<image href="{href}" xlink:href="{href}" '
            f'x="{_fmt(cx - r_img)}" y="{_fmt(cy - r_img)}" '
            f'width="{_fmt(2 * r_img)}" height="{_fmt(2 * r_img)}" '
            f'preserveAspectRatio="xMidYMid meet"/>'
        )
    else:
        parts.append(_agnus_dei_placeholder(cx, cy))

    # ---- title & subtitle ----------------------------------------------
    yr = getattr(cal, "advent_year", None)
    if yr is not None:
        subtitle = f"{yr}–{yr + 1} Calendar of the Christian Year"
    else:
        subtitle = "Calendar of the Christian Year"
    series = getattr(cal, "series", "")
    lect_lbl = "One-Year Historic Lectionary" if lectionary == "one_year" \
        else f"Three-Year Lectionary — Series {series}" if series else "Three-Year Lectionary"

    parts.append(
        f'<text x="{_fmt(cx)}" y="66" text-anchor="middle" '
        f'font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" font-size="46" '
        f'fill="{GOLD}" letter-spacing="1">{escape(title)}</text>'
    )
    parts.append(
        f'<text x="{_fmt(cx)}" y="96" text-anchor="middle" '
        f'font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" font-style="italic" '
        f'font-size="18" fill="{INK}">{escape(subtitle)}</text>'
    )
    parts.append(
        f'<text x="{_fmt(cx)}" y="{_fmt(H - 26)}" text-anchor="middle" '
        f'font-family="Georgia, \'Liberation Serif\', \'Times New Roman\', \'DejaVu Serif\', serif" font-size="12.5" '
        f'fill="{INK}" opacity="0.8">{escape(lect_lbl)}</text>'
    )

    svg_defs = "<defs>" + "".join(defs) + "</defs>"
    body = "".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {_fmt(W)} {_fmt(H)}" '
        f'width="{_fmt(W)}" height="{_fmt(H)}" role="img" '
        f'aria-label="{escape(title)}, {escape(subtitle)}">'
        f'{svg_defs}{body}</svg>'
    )


def _agnus_dei_placeholder(cx: float, cy: float) -> str:
    """A simple cross-and-banner glyph standing in for the Agnus Dei."""
    g = []
    # halo
    g.append(
        f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy - 8)}" r="70" '
        f'fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.55"/>'
    )
    # cross-staff
    sx = cx - 2
    g.append(
        f'<line x1="{_fmt(sx)}" y1="{_fmt(cy - 78)}" x2="{_fmt(sx)}" y2="{_fmt(cy + 52)}" '
        f'stroke="{INK}" stroke-width="4"/>'
    )
    g.append(
        f'<line x1="{_fmt(sx - 22)}" y1="{_fmt(cy - 44)}" x2="{_fmt(sx + 22)}" y2="{_fmt(cy - 44)}" '
        f'stroke="{INK}" stroke-width="4"/>'
    )
    # banner
    g.append(
        f'<path d="M{_fmt(sx)},{_fmt(cy - 72)} L{_fmt(sx + 58)},{_fmt(cy - 66)} '
        f'L{_fmt(sx + 50)},{_fmt(cy - 50)} L{_fmt(sx + 58)},{_fmt(cy - 34)} '
        f'L{_fmt(sx)},{_fmt(cy - 40)} Z" fill="#ffffff" stroke="#c0392b" stroke-width="1.5"/>'
    )
    g.append(
        f'<line x1="{_fmt(sx + 12)}" y1="{_fmt(cy - 70)}" x2="{_fmt(sx + 12)}" y2="{_fmt(cy - 40)}" stroke="#c0392b" stroke-width="2.5"/>'
        f'<line x1="{_fmt(sx + 2)}" y1="{_fmt(cy - 55)}" x2="{_fmt(sx + 22)}" y2="{_fmt(cy - 55)}" stroke="#c0392b" stroke-width="2.5"/>'
    )
    return "<g>" + "".join(g) + "</g>"
