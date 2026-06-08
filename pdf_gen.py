"""
PDF generation for the Liturgical Calendar using ReportLab.
Produces a landscape, tabular output matching the LCMS Church Year Calendar PDF.

Color palette matches the official LCMS PDF exactly:
  Advent      #0070C0  royal blue
  Lent        #7030A0  purple
  Holy Week   #C00000  crimson
  Ash Wed     #000000  black
  Pentecost   #FF0000  red
  Ordinary    #00B050  green
  White seas  no row color (white rows, bold label)
"""

import io
from datetime import date

from reportlab.lib          import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles   import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units    import inch
from reportlab.platypus     import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.enums    import TA_CENTER, TA_LEFT

from liturgical_calendar.calculator import LiturgicalCalendar

# ---------------------------------------------------------------------------
# Exact LCMS PDF colors
# ---------------------------------------------------------------------------
C_ADVENT   = colors.HexColor("#0070C0")   # Royal blue
C_LENT     = colors.HexColor("#7030A0")   # Purple
C_HOLYWK   = colors.HexColor("#C00000")   # Crimson / Scarlet
C_ASHWED   = colors.HexColor("#1A1A1A")   # Near-black (Ash Wednesday)
C_PENT     = colors.HexColor("#FF0000")   # Bright red (Pentecost, Reformation)
C_GREEN    = colors.HexColor("#00B050")   # Dark green (Ordinary Time)
C_WHITE_LBL= colors.HexColor("#555555")   # Dark gray label for white seasons
C_GOLD     = colors.HexColor("#C9A84C")   # Gold accent for white-season label bg

SEASON_COLORS = {
    "Advent":       (C_ADVENT,    colors.white),
    "Lent":         (C_LENT,      colors.white),
    "Pre-Lent":     (C_LENT,      colors.white),
    "Holy Week":    (C_HOLYWK,    colors.white),
    "Pentecost":    (C_PENT,      colors.white),
    "Ordinary Time":(C_GREEN,     colors.white),
    # White-season labels: dark gray text on very light background
    "Christmas":    (colors.HexColor("#F0F0F0"), colors.HexColor("#222")),
    "Epiphany":     (colors.HexColor("#F0F0F0"), colors.HexColor("#222")),
    "Easter":       (colors.HexColor("#F0F0F0"), colors.HexColor("#222")),
    "Ash Wednesday":(C_ASHWED,    colors.white),
}
# Ash Wednesday slot gets black treatment via color field, not season name
COLOR_OVERRIDES = {
    "Black":   (colors.HexColor("#1A1A1A"), colors.white),
    "Blue":    (C_ADVENT,  colors.white),
    "Purple":  (C_LENT,    colors.white),
    "Scarlet": (C_HOLYWK,  colors.white),
    "Red":     (C_PENT,    colors.white),
    "Green":   (C_GREEN,   colors.white),
}

HEADER_BG = colors.HexColor("#1F3864")   # Dark navy — matches PDF header
ROW_WHITE = colors.white
ROW_ALT   = colors.HexColor("#F5F5F5")

PAGE_W, PAGE_H = landscape(letter)
MARGIN = 0.45 * inch


# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
def _style(name="Normal", **kw):
    styles = getSampleStyleSheet()
    base   = styles.get(name, styles["Normal"])
    return ParagraphStyle(name + "_lc", parent=base, **kw)

TITLE_STYLE  = _style("Title",  fontSize=13, textColor=colors.HexColor("#1F3864"),
                      spaceAfter=2, alignment=TA_CENTER, fontName="Helvetica-Bold")
SUB_STYLE    = _style("Normal", fontSize=9,  textColor=colors.HexColor("#0070C0"),
                      spaceAfter=1, alignment=TA_CENTER, fontName="Helvetica-Bold")
DATE_STYLE   = _style("Normal", fontSize=6,  textColor=colors.HexColor("#888888"),
                      spaceAfter=4, alignment=TA_CENTER)
HEAD_STYLE   = _style("Normal", fontSize=7,  textColor=colors.white,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)
CELL_STYLE   = _style("Normal", fontSize=6.5, leading=8, fontName="Helvetica")
CELL_BOLD    = _style("Normal", fontSize=6.5, leading=8, fontName="Helvetica-Bold")
SEASON_STYLE = _style("Normal", fontSize=7,  textColor=colors.white,
                      fontName="Helvetica-Bold", alignment=TA_CENTER, leading=9)


def _cell(text, bold=False):
    s = CELL_BOLD if bold else CELL_STYLE
    return Paragraph(str(text) if text else "", s)

def _season_cell(text, txt_color=colors.white):
    st = ParagraphStyle("sc", parent=SEASON_STYLE, textColor=txt_color)
    return Paragraph(str(text) if text else "", st)


def _ref_text(readings_parsed, label):
    for r in readings_parsed:
        if r["label"] == label:
            text = r["ref"]
            alts = r.get("alts", [])
            if alts:
                text += " / " + " / ".join(alts)
            return text
    return ""


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
        topMargin=MARGIN,  bottomMargin=MARGIN,
    )

    story = []

    # ---- Title block (matches PDF: bold blue title, bold blue series, orange date range) ----
    story.append(Paragraph(
        f"{cal.advent_year}–{cal.civil_year} Church Year Calendar", TITLE_STYLE
    ))
    story.append(Paragraph(series_label, SUB_STYLE))
    story.append(Paragraph(
        f"{cal.advent_1.strftime('%b. %-d, %Y')} — {cal.last_sunday.strftime('%b. %-d, %Y')}",
        _style("Normal", fontSize=8, textColor=colors.HexColor("#C55A00"),
               alignment=TA_CENTER, fontName="Helvetica-Bold", spaceAfter=6),
    ))

    # ---- Column widths — landscape letter usable ≈ 10" ----
    col_widths = [
        0.70 * inch,  # Season
        0.65 * inch,  # Date
        1.40 * inch,  # Festival / Sunday Name
        1.55 * inch,  # First Reading
        1.05 * inch,  # Psalm
        1.55 * inch,  # Epistle
        2.10 * inch,  # Gospel
    ]

    headers = ["Season", "Date", "Festival / Sunday",
               "First\nReading", "Psalm", "Epistle", "Gospel"]
    header_row = [Paragraph(h, HEAD_STYLE) for h in headers]

    all_rows   = [header_row]
    row_styles = []
    row_idx    = 1

    current_season = None

    for ev in events:
        season  = ev.get("season", "")
        color   = ev.get("color", "")
        d       = ev["date"]
        name    = ev.get("name", "")
        is_feast= ev.get("feast", False)
        rp      = ev.get("readings_parsed", [])

        # Season label — only on first row of each season
        if season != current_season:
            season_label   = season.upper()
            current_season = season
        else:
            season_label = ""

        # Pick label cell color: color field takes priority (handles Ash Wed, Good Fri)
        if color in COLOR_OVERRIDES:
            lbl_bg, lbl_fg = COLOR_OVERRIDES[color]
        else:
            lbl_bg, lbl_fg = SEASON_COLORS.get(season, (C_GREEN, colors.white))

        # Date display
        date_str = d.strftime("%b. %-d")
        if d.year != cal.advent_year and d.year != cal.civil_year:
            date_str += f"\n{d.year}"
        elif d.year == cal.civil_year and d.month <= 2:
            date_str = d.strftime("%b. %-d\n") + str(d.year)

        row = [
            _season_cell(season_label, lbl_fg),
            _cell(date_str),
            _cell(name, bold=is_feast),
            _cell(_ref_text(rp, "First Reading")),
            _cell(_ref_text(rp, "Psalm")),
            _cell(_ref_text(rp, "Epistle")),
            _cell(_ref_text(rp, "Gospel")),
        ]
        all_rows.append(row)

        # Season label cell background
        row_styles.append(("BACKGROUND", (0, row_idx), (0, row_idx), lbl_bg))
        row_styles.append(("TEXTCOLOR",  (0, row_idx), (0, row_idx), lbl_fg))
        row_styles.append(("FONTNAME",   (0, row_idx), (0, row_idx), "Helvetica-Bold"))

        # Data rows: white background, feasts get a subtle cream tint
        if is_feast:
            row_styles.append(("BACKGROUND", (1, row_idx), (-1, row_idx),
                                colors.HexColor("#FFFBF0")))
        elif row_idx % 2 == 0:
            row_styles.append(("BACKGROUND", (1, row_idx), (-1, row_idx), ROW_ALT))
        else:
            row_styles.append(("BACKGROUND", (1, row_idx), (-1, row_idx), ROW_WHITE))

        row_idx += 1

    base_style = [
        # Header row
        ("BACKGROUND",   (0, 0), (-1, 0),  HEADER_BG),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  7),
        ("ALIGN",        (0, 0), (-1, 0),  "CENTER"),
        ("VALIGN",       (0, 0), (-1, 0),  "MIDDLE"),
        # Data rows
        ("VALIGN",       (0, 1), (-1, -1), "TOP"),
        ("FONTSIZE",     (0, 1), (-1, -1), 6.5),
        ("LEADING",      (0, 1), (-1, -1), 8),
        ("ALIGN",        (0, 1), (0, -1),  "CENTER"),   # season col centered
        ("ALIGN",        (1, 1), (1, -1),  "CENTER"),   # date col centered
        # Grid
        ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("LINEBELOW",    (0, 0), (-1, 0),  1.0, colors.white),
        # Padding
        ("LEFTPADDING",  (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
    ] + row_styles

    table = Table(all_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle(base_style))

    story.append(table)
    doc.build(story)
    buf.seek(0)
    return buf
