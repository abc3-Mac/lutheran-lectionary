"""Inline SVG moon-phase icons, rendered from an illuminated fraction.

Pure string output, no assets. The lit region is drawn as a limb semicircle
plus a terminator half-ellipse whose width tracks the illuminated fraction, so
a single function draws every phase from new through full. Colors are fixed hex
(a physical object) so the disc does not invert in dark mode.
"""

LIT = "#ECEAE2"
SHADOW = "#43423E"
BORDER = "#5F5E5A"


def moon_svg(illumination: float, waxing: bool, size: int = 28,
             label: str = "") -> str:
    """SVG markup for a moon at the given illuminated fraction (0..1)."""
    f = max(0.0, min(1.0, illumination))
    c = size / 2
    r = c - 1
    top, bot = c - r, c + r
    title = f"<title>{label}</title>" if label else ""
    disc = (f'<circle cx="{c:.2f}" cy="{c:.2f}" r="{r:.2f}" '
            f'fill="{SHADOW}" stroke="{BORDER}" stroke-width="0.5"/>')

    if f <= 0.005:
        body = disc
    elif f >= 0.995:
        body = (f'<circle cx="{c:.2f}" cy="{c:.2f}" r="{r:.2f}" '
                f'fill="{LIT}" stroke="{BORDER}" stroke-width="0.5"/>')
    else:
        rx = r * abs(2 * f - 1)
        gibbous = f > 0.5
        if waxing:                       # lit limb on the right
            outer = f'A {r:.2f} {r:.2f} 0 0 1 {c:.2f} {bot:.2f}'
            inner_sweep = 1 if gibbous else 0
        else:                            # lit limb on the left
            outer = f'A {r:.2f} {r:.2f} 0 0 0 {c:.2f} {bot:.2f}'
            inner_sweep = 0 if gibbous else 1
        inner = f'A {rx:.2f} {r:.2f} 0 0 {inner_sweep} {c:.2f} {top:.2f}'
        path = (f'<path d="M {c:.2f} {top:.2f} {outer} {inner} Z" fill="{LIT}"/>')
        body = disc + path

    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'role="img" aria-label="{label or "moon phase"}" '
            f'xmlns="http://www.w3.org/2000/svg">{title}{body}</svg>')


_PRINCIPAL = {
    "New moon":      (0.0, True),
    "First quarter": (0.5, True),
    "Full moon":     (1.0, True),
    "Last quarter":  (0.5, False),
}


def phase_icon(phase_name: str, size: int = 28) -> str:
    """Icon for a named principal phase."""
    illum, waxing = _PRINCIPAL.get(phase_name, (0.0, True))
    return moon_svg(illum, waxing, size=size, label=phase_name)
