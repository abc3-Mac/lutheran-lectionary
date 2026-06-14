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


# ---------------------------------------------------------------------------
# Daily Lectionary PDF — portrait table, one section per month
# ---------------------------------------------------------------------------

def build_daily_pdf(advent_year: int, months: list) -> io.BytesIO:
    """Build a portrait PDF of the full-year LSB Daily Lectionary.

    `months` is the structure produced by app._daily_year_days():
    [{"month": "December 2025", "days": [{"date_str", "ot", "nt"}, ...]}, ...]
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
        title=f"LSB Daily Lectionary {advent_year}–{advent_year + 1}",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DailyTitle", parent=styles["Title"], fontSize=15, spaceAfter=2)
    sub_style = ParagraphStyle(
        "DailySub", parent=styles["Normal"], fontSize=9,
        textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=10)
    month_style = ParagraphStyle(
        "DailyMonth", parent=styles["Heading2"], fontSize=11,
        textColor=colors.HexColor("#1A3A5C"), spaceBefore=10, spaceAfter=3)

    story = [
        Paragraph(f"LSB Daily Lectionary — {advent_year}–{advent_year + 1} Church Year", title_style),
        Paragraph("Two readings for every day — for personal or family devotion", sub_style),
    ]

    col_widths = [1.5 * inch, 2.9 * inch, 2.9 * inch]
    header_bg = colors.HexColor("#1A3A5C")

    for m in months:
        rows = [["Date", "Old Testament", "New Testament"]]
        for d in m["days"]:
            rows.append([d["date_str"], d["ot"], d["nt"]])
        table = Table(rows, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0), header_bg),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 8),
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F5F4F0")]),
            ("GRID",         (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
            ("LEFTPADDING",  (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING",   (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        ]))
        story.append(Paragraph(m["month"], month_style))
        story.append(table)

    doc.build(story)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# One-Year Propers PDF — introit + collect per Sunday, grouped by season
# ---------------------------------------------------------------------------

SEASON_HEX = {
    "season-blue": "#0070C0", "season-white": "#D4AA40", "season-green": "#00B050",
    "season-purple": "#7030A0", "season-scarlet": "#C00000", "season-red": "#FF0000",
    "season-black": "#000000",
}


def _season_hex(color_class: str, violet_advent: bool = False) -> str:
    """Season color hex. When violet_advent is set (the One-Year/historic Advent
    preference), the blue Advent color renders as violet instead."""
    if violet_advent and color_class == "season-blue":
        return SEASON_HEX["season-purple"]
    return SEASON_HEX.get(color_class, "#1A3A5C")


def build_propers_pdf(advent_year: int, sections: list, violet_advent: bool = True) -> io.BytesIO:
    """Portrait PDF of the one-year propers.

    `sections` is the structure from app._propers_sections():
    [{"season": "Advent", "events": [{date_str, name, color_class, introit, collect}, ...]}, ...]
    """
    from reportlab.platypus import KeepTogether

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        title=f"One-Year Propers {advent_year}–{advent_year + 1}",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PropTitle", parent=styles["Title"], fontSize=15, spaceAfter=2)
    sub_style = ParagraphStyle(
        "PropSub", parent=styles["Normal"], fontSize=9,
        textColor=colors.HexColor("#555555"), alignment=TA_CENTER, spaceAfter=12)
    date_style = ParagraphStyle(
        "PropDate", parent=styles["Normal"], fontSize=8,
        textColor=colors.HexColor("#777777"), spaceBefore=8)
    name_style = ParagraphStyle(
        "PropName", parent=styles["Normal"], fontSize=11,
        fontName="Helvetica-Bold", spaceAfter=2)
    introit_style = ParagraphStyle(
        "PropIntroit", parent=styles["Normal"], fontSize=9, spaceAfter=2)
    collect_style = ParagraphStyle(
        "PropCollect", parent=styles["Normal"], fontSize=9, leading=12,
        fontName="Helvetica-Oblique", leftIndent=10, spaceAfter=4)
    source_style = ParagraphStyle(
        "PropSource", parent=styles["Normal"], fontSize=7.5,
        textColor=colors.HexColor("#888888"), spaceBefore=16)

    story = [
        Paragraph(f"One-Year (Historic) Propers — {advent_year}–{advent_year + 1} Church Year", title_style),
        Paragraph("Introit, Collect, Gradual, and Readings for every Sunday and feast day", sub_style),
    ]

    for sec in sections:
        hexcol = _season_hex(sec["events"][0].get("color_class", ""), violet_advent=violet_advent)
        season_style = ParagraphStyle(
            f"Season{sec['season']}", parent=styles["Heading2"], fontSize=12,
            textColor=colors.HexColor(hexcol), spaceBefore=14, spaceAfter=2)
        story.append(Paragraph(sec["season"].upper(), season_style))
        for ev in sec["events"]:
            block = [
                Paragraph(ev["date_str"], date_style),
                Paragraph(ev["name"], name_style),
            ]
            intro = ev.get("introit")
            if intro:
                block.append(Paragraph(
                    f"<b>Introit:</b> <i>{intro['name']}</i> — {intro['ref']}", introit_style))
                if intro.get("text"):
                    block.append(Paragraph(intro["text"], collect_style))
            if ev.get("collect"):
                block.append(Paragraph(f"<b>Collect:</b> {ev['collect']}", collect_style))
            if ev.get("gradual"):
                block.append(Paragraph(f"<b>Gradual:</b> {ev['gradual']}", collect_style))
            rp = ev.get("readings_parsed")
            if rp:
                parts = []
                for r in rp:
                    refs = " or ".join([r["ref"]] + list(r.get("alts") or []))
                    parts.append(f"{r['label']}: {refs}")
                block.append(Paragraph("<b>Readings:</b> " + " &nbsp;·&nbsp; ".join(parts),
                                       introit_style))
            story.append(KeepTogether(block))

    story.append(Paragraph(
        "Introits, Collects, and Graduals from the Common Service Book of the Lutheran Church (1917), "
        "public domain — the same historic wording later carried into The Lutheran Hymnal (TLH, 1941). "
        "For LSB collect and introit texts, see the LSB Altar Book.", source_style))

    doc.build(story)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Single-day "Propers for the Day" sheet — bulletin-friendly one-pager
# ---------------------------------------------------------------------------

def _day_citation(result: dict, lectionary: str) -> str:
    """Source/copyright line for a single-day sheet, accurate to what's on the page.

    The one-year (historic) series draws its introit, collect, and gradual from the
    public-domain CSB 1917; the three-year series carries none of those — only
    LSB readings, hymn-of-the-day numbers, and the LSB Daily Lectionary, all facts.
    Citing the 1917 texts on a three-year sheet would describe content that isn't there.
    """
    has_csb = lectionary == "one_year" and (
        result.get("introit") or result.get("collect") or result.get("gradual"))
    if has_csb:
        return ("Introit, collect, and gradual from the Common Service Book of the Lutheran "
                "Church (1917), public domain. Readings per the LSB Propers of the Day "
                "(CPH, 2007). For LSB collect and introit texts, see the LSB Altar Book.")
    return ("Readings, Hymn of the Day, and Daily Lectionary per the Lutheran Service Book "
            "(CPH, 2006) and the LSB Propers of the Day (CPH, 2007). Reading references and "
            "hymn numbers only; the texts themselves are not reproduced.")


def build_day_pdf(result: dict, lectionary: str, violet_advent: bool = True) -> io.BytesIO:
    """One-page PDF of the propers for a single date.

    `result` is the dict from app._lookup_result(): name, date_str, season,
    color_class, readings_parsed, collect, introit, gradual, hymn_of_the_day,
    daily, minor_feast, church_year, series.
    """
    from reportlab.platypus import KeepTogether, HRFlowable

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        title=f"Propers — {result.get('name', '')}",
    )
    styles = getSampleStyleSheet()
    hexcol = _season_hex(result.get("color_class", ""),
                         violet_advent=(violet_advent and lectionary == "one_year"))

    title_style = ParagraphStyle("DayTitle", parent=styles["Title"], fontSize=18,
                                 textColor=colors.HexColor(hexcol), spaceAfter=2)
    sub_style = ParagraphStyle("DaySub", parent=styles["Normal"], fontSize=10,
                               textColor=colors.HexColor("#555555"), spaceAfter=10)
    h_style = ParagraphStyle("DayH", parent=styles["Heading2"], fontSize=11,
                             textColor=colors.HexColor(hexcol), spaceBefore=12, spaceAfter=3)
    body = ParagraphStyle("DayBody", parent=styles["Normal"], fontSize=9.5, leading=13)
    italic = ParagraphStyle("DayItalic", parent=body, fontName="Helvetica-Oblique",
                            leftIndent=8)
    source_style = ParagraphStyle("DaySource", parent=styles["Normal"], fontSize=7.5,
                                  textColor=colors.HexColor("#888888"), spaceBefore=18)

    if lectionary == "one_year":
        series_label = "One-Year (Historic) Series"
    else:
        series_label = f"Three-Year Series {result.get('series', '')}".strip()

    story = [
        Paragraph(result.get("name", ""), title_style),
        Paragraph(f"{result.get('date_str', '')} &nbsp;·&nbsp; {result.get('season', '')} "
                  f"&nbsp;·&nbsp; {result.get('church_year', '')} Church Year "
                  f"&nbsp;·&nbsp; {series_label}", sub_style),
        HRFlowable(width="100%", thickness=2, color=colors.HexColor(hexcol),
                   spaceBefore=0, spaceAfter=2),
    ]

    rp = result.get("readings_parsed")
    if rp:
        story.append(Paragraph("Appointed Readings", h_style))
        for r in rp:
            refs = " <i>or</i> ".join([r["ref"]] + list(r.get("alts") or []))
            story.append(Paragraph(f"<b>{r['label']}:</b> {refs}", body))

    intro = result.get("introit")
    if intro and (intro.get("name") or intro.get("text")):
        story.append(Paragraph("Introit", h_style))
        story.append(Paragraph(f"<i>{intro.get('name','')}</i> — {intro.get('ref','')}", body))
        if intro.get("text"):
            story.append(Paragraph(intro["text"], italic))
    if result.get("collect"):
        story.append(Paragraph("Collect of the Day", h_style))
        story.append(Paragraph(result["collect"], italic))
    if result.get("gradual"):
        story.append(Paragraph("Gradual", h_style))
        story.append(Paragraph(result["gradual"], italic))

    hod = result.get("hymn_of_the_day")
    if hod:
        story.append(Paragraph("Hymn of the Day", h_style))
        story.append(Paragraph(" <i>or</i> ".join(hod), body))

    daily = result.get("daily")
    if daily:
        story.append(Paragraph("Daily Lectionary", h_style))
        story.append(Paragraph(" &nbsp;·&nbsp; ".join(
            f"<b>{d['label']}:</b> {d['ref']}" for d in daily), body))

    mf = result.get("minor_feast")
    if mf:
        story.append(Paragraph(f"Also Commemorated: {mf.get('name','')}", h_style))
        if mf.get("collect"):
            story.append(Paragraph(mf["collect"], italic))

    story.append(Paragraph(_day_citation(result, lectionary), source_style))

    doc.build(story)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Card-style "Propers for the Day" sheet — mirrors the web lookup card
# ---------------------------------------------------------------------------

def build_day_card_pdf(result: dict, lectionary: str, violet_advent: bool = True) -> io.BytesIO:
    """Single-day propers as a styled card matching the web /lookup view:
    a season-colored header band over a white card with sectioned content.

    Same `result` dict as build_day_pdf; this is the alternate visual style
    offered via ?style=card. Content is identical — only the presentation differs.
    """
    from reportlab.platypus import HRFlowable

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.6 * inch, bottomMargin=0.6 * inch,
        title=f"Propers — {result.get('name', '')}",
    )

    hexcol = _season_hex(result.get("color_class", ""),
                         violet_advent=(violet_advent and lectionary == "one_year"))
    header_bg = colors.HexColor(hexcol)

    CARD_PAD = 20
    inner_w  = doc.width - 2 * CARD_PAD

    white   = colors.white
    soft_w  = colors.Color(1, 1, 1, alpha=0.92)
    c_label = colors.HexColor("#6B7280")
    c_value = colors.HexColor("#1F3A5F")
    c_text  = colors.HexColor("#222222")
    c_muted = colors.HexColor("#8A8A8A")

    s_date  = ParagraphStyle("cDate",  fontSize=10,  textColor=soft_w, fontName="Helvetica",
                             spaceAfter=4)
    s_title = ParagraphStyle("cTitle", fontSize=23,  leading=26, textColor=white,
                             fontName="Helvetica-Bold", spaceAfter=7)
    s_meta  = ParagraphStyle("cMeta",  fontSize=9.5, textColor=soft_w, fontName="Helvetica",
                             leading=12)
    s_sec   = ParagraphStyle("cSec",   fontSize=9,   textColor=c_label,
                             fontName="Helvetica-Bold", spaceAfter=6, leading=11)
    s_collbl= ParagraphStyle("cColL",  fontSize=7.5, textColor=c_label,
                             fontName="Helvetica-Bold", spaceAfter=3, leading=10)
    s_val   = ParagraphStyle("cVal",   fontSize=11,  textColor=c_value, fontName="Helvetica",
                             leading=14)
    s_body  = ParagraphStyle("cBody",  fontSize=11,  textColor=c_text, leading=15,
                             fontName="Helvetica")
    s_it    = ParagraphStyle("cIt",    parent=s_body, fontName="Helvetica-Oblique", leftIndent=6)
    s_cap   = ParagraphStyle("cCap",   fontSize=8.5, textColor=c_muted, fontName="Helvetica",
                             spaceBefore=5)
    s_src   = ParagraphStyle("cSrc",   fontSize=7.5, textColor=c_muted, fontName="Helvetica",
                             leading=10, spaceBefore=4)
    s_fl    = ParagraphStyle("cFL",    fontSize=11,  textColor=colors.HexColor("#333333"),
                             fontName="Courier")

    # ---- Header band content ----
    if lectionary == "one_year":
        series_bit = "One-Year (Historic)"
    else:
        series_bit = f"Series {result.get('series', '')}".strip()
    # Honor the violet-Advent preference in the displayed color name, matching the
    # header band and the web UI (which both render historic Advent as violet, not blue).
    color_name = result.get("color", "")
    if violet_advent and lectionary == "one_year" and color_name == "Blue":
        color_name = "Violet"
    meta_bits = [b for b in (
        result.get("season", ""), series_bit,
        f"{result.get('church_year', '')} Church Year",
        color_name,
    ) if b]
    header = [
        Paragraph(result.get("date_str", ""), s_date),
        Paragraph(result.get("name", ""), s_title),
        Paragraph("&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;&nbsp;".join(meta_bits), s_meta),
    ]

    # ---- Body sections (one table row each, so the card paginates cleanly) ----
    sections = []  # list of (title, [flowables])

    def section(title, flows):
        sections.append((title, flows))

    def grid(pairs, ncols):
        """Table of (label, value) cells laid out in rows of `ncols`."""
        cells = [[Paragraph(lbl.upper(), s_collbl), Paragraph(val, s_val)] for lbl, val in pairs]
        rows = []
        for i in range(0, len(cells), ncols):
            chunk = cells[i:i + ncols]
            chunk += [""] * (ncols - len(chunk))
            rows.append(chunk)
        t = Table(rows, colWidths=[inner_w / ncols] * ncols)
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        return [t]

    rp = result.get("readings_parsed")
    if rp:
        pairs = [(r["label"], " <i>or</i> ".join([r["ref"]] + list(r.get("alts") or [])))
                 for r in rp]
        section("Appointed Readings", grid(pairs, 4))

    intro = result.get("introit")
    if intro and (intro.get("name") or intro.get("text")):
        flows = [Paragraph(f"<i>{intro.get('name','')}</i> &mdash; {intro.get('ref','')}", s_body)]
        if intro.get("text"):
            flows.append(Paragraph(intro["text"], s_it))
        section("Introit", flows)
    if result.get("collect"):
        section("Collect of the Day", [Paragraph(result["collect"], s_it)])
    if result.get("gradual"):
        section("Gradual", [Paragraph(result["gradual"], s_it)])

    hod = result.get("hymn_of_the_day")
    if hod:
        section("Hymn of the Day", [Paragraph("  <i>or</i>  ".join(hod), s_body)])

    daily = result.get("daily")
    if daily:
        pairs = [(d["label"], d["ref"]) for d in daily]
        section("Daily Lectionary", grid(pairs, 2) + [
            Paragraph("LSB Daily Lectionary — two readings for personal or family devotion.", s_cap)])

    mf = result.get("minor_feast")
    if mf:
        flows = [Paragraph(mf["collect"], s_it)] if mf.get("collect") else \
                [Paragraph("Commemorated this day.", s_body)]
        section(f"Also Commemorated: {mf.get('name','')}", flows)

    if result.get("file_label"):
        fl_box = Table([[Paragraph(result["file_label"], s_fl)]], colWidths=[inner_w])
        fl_box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFEEE9")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E0DED7")),
            ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        section("File Label", [
            fl_box,
            Paragraph("Use this as a filename prefix for recordings, videos, or documents "
                      "from this day.", s_cap),
        ])

    # Citation rides along as the final (untitled) row.
    sections.append((None, [Paragraph(_day_citation(result, lectionary), s_src)]))

    # ---- Assemble: colored header row over one white row per section ----
    rows = [[header]]
    for title, flows in sections:
        cell = ([Paragraph(title.upper(), s_sec)] + flows) if title else flows
        rows.append([cell])

    style = [
        ("BACKGROUND", (0, 0), (0, 0), header_bg),
        ("BACKGROUND", (0, 1), (0, -1), white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 22), ("RIGHTPADDING", (0, 0), (0, 0), 22),
        ("TOPPADDING", (0, 0), (0, 0), 20), ("BOTTOMPADDING", (0, 0), (0, 0), 20),
        ("LEFTPADDING", (0, 1), (0, -1), CARD_PAD), ("RIGHTPADDING", (0, 1), (0, -1), CARD_PAD),
        ("TOPPADDING", (0, 1), (0, -1), 13), ("BOTTOMPADDING", (0, 1), (0, -1), 13),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#E0E0E0")),
        ("ROUNDEDCORNERS", [13, 13, 13, 13]),
    ]
    # Thin divider above each section row after the first (skip the header row at 0).
    for r in range(2, len(rows)):
        style.append(("LINEABOVE", (0, r), (0, r), 0.6, colors.HexColor("#E6E6E6")))

    card = Table(rows, colWidths=[doc.width], splitByRow=1)
    card.setStyle(TableStyle(style))

    doc.build([card])
    buf.seek(0)
    return buf
