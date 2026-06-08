"""
PDF generation for the Liturgical Calendar using ReportLab.
Produces a landscape, tabular output modeled on the LCMS Church Year Calendar PDF.
"""

import io
from datetime import date

from reportlab.lib         import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles  import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units   import inch
from reportlab.platypus    import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, KeepTogether
)
from reportlab.lib.enums   import TA_CENTER, TA_LEFT

from liturgical_calendar.calculator import LiturgicalCalendar

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
SEASON_COLORS = {
    "Advent":    colors.HexColor("#4B6FA5"),
    "Christmas": colors.HexColor("#B8860B"),
    "Epiphany":  colors.HexColor("#2E8B57"),
    "Lent":      colors.HexColor("#6B2FA0"),
    "Holy Week": colors.HexColor("#8B0000"),
    "Easter":    colors.HexColor("#B8860B"),
    "Pentecost": colors.HexColor("#CC0000"),
    "Trinity":   colors.HexColor("#006400"),
    "Pre-Lent":  colors.HexColor("#6B2FA0"),
}

HEADER_BG  = colors.HexColor("#1A3A5C")
ROW_ALT    = colors.HexColor("#F0F4F8")
ROW_FEAST  = colors.HexColor("#FFF8DC")

PAGE_W, PAGE_H = landscape(letter)
MARGIN = 0.5 * inch


def _style(name="Normal", **kwargs):
    styles = getSampleStyleSheet()
    base   = styles.get(name, styles["Normal"])
    return ParagraphStyle(name + "_custom", parent=base, **kwargs)


TITLE_STYLE = _style("Title", fontSize=14, textColor=colors.HexColor("#1A3A5C"),
                     spaceAfter=4, alignment=TA_CENTER)
SUB_STYLE   = _style("Normal", fontSize=9,  textColor=colors.grey,
                     spaceAfter=2, alignment=TA_CENTER)
HEAD_STYLE  = _style("Normal", fontSize=7,  textColor=colors.white,
                     fontName="Helvetica-Bold", alignment=TA_CENTER)
CELL_STYLE  = _style("Normal", fontSize=6.5, leading=8)
SEASON_STYLE= _style("Normal", fontSize=8,  textColor=colors.white,
                     fontName="Helvetica-Bold", alignment=TA_CENTER)


def _cell(text, style=None):
    if style is None:
        style = CELL_STYLE
    return Paragraph(str(text) if text else "", style)


def _reading_cell(readings_parsed: list) -> str:
    parts = []
    for r in readings_parsed:
        ref = r.get("ref", "")
        alts = r.get("alts", [])
        if alts:
            ref += " / " + " / ".join(alts)
        parts.append(ref)
    return "\n".join(parts)


def build_pdf(cal: LiturgicalCalendar, events: list, lectionary: str) -> io.BytesIO:
    buf = io.BytesIO()

    series_label = (
        f"Three-Year Series {cal.series}" if lectionary == "three_year"
        else "One-Year (Historic) Series"
    )

    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(letter),
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    story = []

    # ---- Title block ----
    story.append(Paragraph(
        f"{cal.advent_year}–{cal.civil_year} Church Year Calendar", TITLE_STYLE
    ))
    story.append(Paragraph(series_label, SUB_STYLE))
    story.append(Paragraph(
        f"{cal.advent_1.strftime('%-d %b %Y')} — {cal.last_sunday.strftime('%-d %b %Y')}",
        SUB_STYLE
    ))
    story.append(Spacer(1, 0.1 * inch))

    # ---- Column widths (landscape letter = 11" x 8.5", usable ≈ 10") ----
    usable = PAGE_W - 2 * MARGIN
    col_widths = [
        0.65 * inch,  # Season
        0.70 * inch,  # Date
        1.45 * inch,  # Festival / Sunday Name
        1.55 * inch,  # First Reading
        1.10 * inch,  # Psalm
        1.55 * inch,  # Epistle
        2.00 * inch,  # Gospel
    ]

    headers = ["Season", "Date", "Festival / Sunday", "First Reading", "Psalm", "Epistle", "Gospel"]
    header_row = [Paragraph(h, HEAD_STYLE) for h in headers]

    # Group events by season
    sections: dict[str, list] = {}
    for ev in events:
        s = ev.get("season", "Other")
        sections.setdefault(s, []).append(ev)

    # Build one big table per season section
    all_rows    = [header_row]
    row_styles  = []
    row_idx     = 1  # header is row 0

    current_season = None
    season_start   = 1

    for ev in events:
        season = ev.get("season", "")
        d      = ev["date"]
        name   = ev.get("name", "")
        rp     = ev.get("readings_parsed", [])

        def _ref(label):
            for r in rp:
                if r["label"] == label:
                    text = r["ref"]
                    if r["alts"]:
                        text += " / " + " / ".join(r["alts"])
                    return text
            return ""

        # Season label cell (merge down handled via style later)
        if season != current_season:
            season_label = season
            current_season = season
        else:
            season_label = ""

        date_str = d.strftime("%-d %b") if d.isoweekday() == 7 or ev.get("is_feast") else d.strftime("%-d %b (%a)")

        row = [
            _cell(season_label),
            _cell(date_str),
            _cell(name),
            _cell(_ref("First Reading")),
            _cell(_ref("Psalm")),
            _cell(_ref("Epistle")),
            _cell(_ref("Gospel")),
        ]
        all_rows.append(row)

        # Row background
        if ev.get("is_feast"):
            row_styles.append(("BACKGROUND", (0, row_idx), (-1, row_idx), ROW_FEAST))
        elif row_idx % 2 == 0:
            row_styles.append(("BACKGROUND", (0, row_idx), (-1, row_idx), ROW_ALT))

        # Season color on first cell
        if season_label:
            sc = SEASON_COLORS.get(season, colors.grey)
            row_styles.append(("BACKGROUND", (0, row_idx), (0, row_idx), sc))
            row_styles.append(("TEXTCOLOR",  (0, row_idx), (0, row_idx), colors.white))
            row_styles.append(("FONTNAME",   (0, row_idx), (0, row_idx), "Helvetica-Bold"))

        row_idx += 1

    # Table style
    base_style = [
        # Header
        ("BACKGROUND",  (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  7),
        ("ALIGN",       (0, 0), (-1, 0),  "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE",    (0, 1), (-1, -1), 6.5),
        ("LEADING",     (0, 1), (-1, -1), 8),
        ("GRID",        (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",(0, 0), (-1, -1), 2),
        ("TOPPADDING",  (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0,0), (-1, -1), 2),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),  [colors.white, ROW_ALT]),
    ] + row_styles

    table = Table(all_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle(base_style))

    story.append(table)

    doc.build(story)
    buf.seek(0)
    return buf
