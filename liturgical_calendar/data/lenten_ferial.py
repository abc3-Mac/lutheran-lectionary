"""
Historic Lenten Weekday (Ferial) Lectionary.

The historic Western rite is unique in providing a *proper Mass for every
weekday of Lent* — Ash Wednesday through Good Friday — not only for Sundays.
Each ferial day has (as a rule) two lessons: an "Epistle," which in Lent is
almost always drawn from the Old Testament (Pentateuch and Major Prophets),
and a Gospel. The Ember Days and the Wednesday and Saturday of Laetare carry
additional lessons, as they historically did.

PROVENANCE (Roman vs. Lutheran)
-------------------------------
The *substance* of this lectionary — the daily framework and every Gospel and
Old-Testament lesson — is the historic Western (Roman-rite) ferial lectionary.
It is attested in the oldest Roman books (the Gregorian Sacramentary; the early
Roman lectionaries such as the Würzburg Comes, 7th c., and the Comes of Murbach,
8th c.) and was codified in the Tridentine Missal (1570 → 1962). Wednesdays and
Fridays are the most ancient (the old Roman "station days"); Thursdays were only
supplied in the 8th century.

The specific recension reproduced here is the one *the Lutherans inherited* —
the late-medieval German use — as reconstructed by **The Lutheran Missal**
project from its catalogue of medieval missals and Lutheran sources
(lutheranmissal.home.blog, "Lenten Lections," 11 Feb 2020). Where the Lutheran /
northeast-German tradition diverges from the mainstream Roman books, this table
follows the Lutheran usage. The clearest example is the Holy Week Monday/Tuesday
Gospels: The Lutheran Missal assigns Mark to Monday and John to Tuesday — the
*minority* order in the wider manuscript record, but the one used by "all of the
Lutheran sources currently cataloged" and the older northeast-German missals,
"as yet unaltered by Rome." (LSB reverses them.)

MARKERS (from The Lutheran Missal's own legend)
-----------------------------------------------
    (none)  historic AND retained in LSB          → origin "core"
    *       historic, but dropped by today's LSB   → origin "hist"  (the most Roman)
    **      in LSB, but NOT historic (modern)      → origin "lsb"

Sundays are included for context (their historic Epistle + Gospel already live in
one_year.py); their ``**`` Old-Testament lesson is the modern LSB third reading.

Source, verbatim: The Lutheran Missal, "Lenten Lections" (11 Feb 2020),
https://lutheranmissal.home.blog/2020/02/11/lenten-lections/ — retrieved
2026-07-01 from page HTML. Public reference; citations transcribed as printed
(e.g. the Ember Saturday "2 Maccabees 1:23, 2-5" is reproduced as given).

This module is tradition-scoped (TRADITION / TRACK) so that additional traditions
(RCL, Roman, etc.) can be added as sibling tracks later.
"""

TRADITION = "lutheran"          # Lutheran (LCMS), via The Lutheran Missal
TRACK = "lenten_ferial"

# --- provenance vocabulary -------------------------------------------------

ORIGIN_LABELS = {
    "core": "Historic Western — retained in LSB",
    "hist": "Historic Western — dropped by LSB",
    "lsb":  "Modern (LSB) — not part of the historic set",
}
ORIGIN_SHORT = {"core": "Historic", "hist": "Historic (pre-LSB)", "lsb": "LSB (modern)"}

MARK_LEGEND = {
    "":   "Historic and retained in the current LSB one-year lectionary.",
    "*":  "Historic Western reading, not found in today's LSB — the older usage.",
    "**": "Found in LSB but not part of the historic set (a modern addition; "
          "usually the third, Old-Testament reading on Sundays).",
}


def _mark_origin(mark):
    return "lsb" if mark == "**" else ("hist" if mark == "*" else "core")


def R(ref, label, mark=""):
    """One reading: scripture reference, slot label, and provenance mark."""
    return {"ref": ref, "label": label, "mark": mark, "origin": _mark_origin(mark)}


# --- the lectionary, grouped by week ---------------------------------------
# Each day: slot, name, anchor (a LiturgicalCalendar date attribute), offset
# (days after that anchor), is_sunday, and its ordered readings.

LENTEN_WEEKS = [
    {
        "key": "ash",
        "name": "Ash Wednesday and the First Days",
        "days": [
            {"slot": "fer_ash_wed", "name": "Ash Wednesday", "anchor": "ash_wednesday", "offset": 0, "is_sunday": False,
             "readings": [R("Joel 2:12-19", "Epistle (Lesson)"), R("2 Peter 1:2-11", "Epistle", "**"), R("Matthew 6:16-21", "Gospel")],
             "note": "Historically the Epistle was Joel alone, with no New Testament reading before the Gospel; the 2 Peter Epistle is a modern LSB addition."},
            {"slot": "fer_ash_thu", "name": "Thursday after Ash Wednesday", "anchor": "ash_wednesday", "offset": 1, "is_sunday": False,
             "readings": [R("Isaiah 38:1-6", "Lesson"), R("Matthew 6:5-8", "Gospel")]},
            {"slot": "fer_ash_fri", "name": "Friday after Ash Wednesday", "anchor": "ash_wednesday", "offset": 2, "is_sunday": False,
             "readings": [R("Isaiah 58:1-9a", "Lesson"), R("Matthew 5:43-6:4", "Gospel")]},
            {"slot": "fer_ash_sat", "name": "Saturday after Ash Wednesday", "anchor": "ash_wednesday", "offset": 3, "is_sunday": False,
             "readings": [R("Isaiah 58:9b-14", "Lesson"), R("Mark 6:47-56", "Gospel")]},
        ],
    },
    {
        "key": "invocavit",
        "name": "Invocavit — First Week in Lent",
        "days": [
            {"slot": "invocavit", "name": "Invocavit (First Sunday in Lent)", "anchor": "lent_1", "offset": 0, "is_sunday": True,
             "readings": [R("Genesis 3:1-21", "Old Testament", "**"), R("2 Corinthians 6:1-10", "Epistle"), R("Matthew 4:1-11", "Gospel")]},
            {"slot": "fer_invocavit_mon", "name": "Monday of Invocavit", "anchor": "lent_1", "offset": 1, "is_sunday": False,
             "readings": [R("Ezekiel 34:11-16", "Lesson"), R("Matthew 25:31-46", "Gospel")]},
            {"slot": "fer_invocavit_tue", "name": "Tuesday of Invocavit", "anchor": "lent_1", "offset": 2, "is_sunday": False,
             "readings": [R("Isaiah 55:6-11", "Lesson"), R("Matthew 21:10-17", "Gospel")]},
            {"slot": "fer_ember_wed", "name": "Ember Wednesday in Lent", "anchor": "lent_1", "offset": 3, "is_sunday": False,
             "readings": [R("Exodus 24:12-18", "First Lesson"), R("1 Kings 19:3b-8", "Second Lesson", "*"), R("Matthew 12:38-50", "Gospel")],
             "note": "An Ember Day — historically provided with two lessons before the Gospel."},
            {"slot": "fer_invocavit_thu", "name": "Thursday of Invocavit", "anchor": "lent_1", "offset": 4, "is_sunday": False,
             "readings": [R("Ezekiel 18:1-9", "Lesson"), R("John 8:31-47a", "Gospel")]},
            {"slot": "fer_ember_fri", "name": "Ember Friday in Lent", "anchor": "lent_1", "offset": 5, "is_sunday": False,
             "readings": [R("Ezekiel 18:20-28", "Lesson"), R("John 5:1-15", "Gospel")]},
            {"slot": "fer_ember_sat", "name": "Ember Saturday in Lent", "anchor": "lent_1", "offset": 6, "is_sunday": False,
             "readings": [R("Deuteronomy 26:15-29", "First Lesson"), R("Deuteronomy 11:22-25", "Second Lesson"),
                          R("2 Maccabees 1:23, 2-5", "Third Lesson"), R("Sirach 36:1-10", "Fourth Lesson"),
                          R("Prayer of Azariah 1:24-28", "Fifth Lesson"), R("1 Thessalonians 5:14-23", "Epistle"),
                          R("Matthew 17:1-9", "Gospel")],
             "note": "An Ember Day — the ancient Saturday of many prophecies (five lessons, then Epistle and Gospel), closing with the Transfiguration."},
        ],
    },
    {
        "key": "reminiscere",
        "name": "Reminiscere — Second Week in Lent",
        "days": [
            {"slot": "reminiscere", "name": "Reminiscere (Second Sunday in Lent)", "anchor": "lent_2", "offset": 0, "is_sunday": True,
             "readings": [R("Genesis 32:22-32", "Old Testament", "**"), R("1 Thessalonians 4:1-7", "Epistle"), R("Matthew 15:21-28", "Gospel")]},
            {"slot": "fer_reminiscere_mon", "name": "Monday of Reminiscere", "anchor": "lent_2", "offset": 1, "is_sunday": False,
             "readings": [R("Daniel 9:15-19", "Lesson"), R("John 8:21-29", "Gospel")]},
            {"slot": "fer_reminiscere_tue", "name": "Tuesday of Reminiscere", "anchor": "lent_2", "offset": 2, "is_sunday": False,
             "readings": [R("1 Kings 17:8-16", "Lesson"), R("Matthew 23:1-12", "Gospel")]},
            {"slot": "fer_reminiscere_wed", "name": "Wednesday of Reminiscere", "anchor": "lent_2", "offset": 3, "is_sunday": False,
             "readings": [R("Esther 13:8-11, 15-17", "Lesson"), R("Matthew 20:17-28", "Gospel")]},
            {"slot": "fer_reminiscere_thu", "name": "Thursday of Reminiscere", "anchor": "lent_2", "offset": 4, "is_sunday": False,
             "readings": [R("Jeremiah 17:5-10", "Lesson"), R("John 5:30-47", "Gospel")]},
            {"slot": "fer_reminiscere_fri", "name": "Friday of Reminiscere", "anchor": "lent_2", "offset": 5, "is_sunday": False,
             "readings": [R("Genesis 37:6-22", "Lesson"), R("Matthew 21:33-46", "Gospel")]},
            {"slot": "fer_reminiscere_sat", "name": "Saturday of Reminiscere", "anchor": "lent_2", "offset": 6, "is_sunday": False,
             "readings": [R("Genesis 27:6-40a", "Lesson"), R("Luke 15:11-32", "Gospel")]},
        ],
    },
    {
        "key": "oculi",
        "name": "Oculi — Third Week in Lent",
        "days": [
            {"slot": "oculi", "name": "Oculi (Third Sunday in Lent)", "anchor": "lent_3", "offset": 0, "is_sunday": True,
             "readings": [R("Jeremiah 26:1-15", "Old Testament", "**"), R("Ephesians 5:1-9", "Epistle"), R("Luke 11:14-28", "Gospel")]},
            {"slot": "fer_oculi_mon", "name": "Monday of Oculi", "anchor": "lent_3", "offset": 1, "is_sunday": False,
             "readings": [R("2 Kings 5:1-15a", "Lesson"), R("Luke 4:23b-30", "Gospel")]},
            {"slot": "fer_oculi_tue", "name": "Tuesday of Oculi", "anchor": "lent_3", "offset": 2, "is_sunday": False,
             "readings": [R("2 Kings 4:1-7", "Lesson"), R("Matthew 18:15-22", "Gospel")]},
            {"slot": "fer_oculi_wed", "name": "Wednesday of Oculi", "anchor": "lent_3", "offset": 3, "is_sunday": False,
             "readings": [R("Exodus 20:12-24a", "Lesson"), R("Matthew 15:1-20", "Gospel")]},
            {"slot": "fer_oculi_thu", "name": "Thursday of Oculi", "anchor": "lent_3", "offset": 4, "is_sunday": False,
             "readings": [R("Jeremiah 7:1-7", "Lesson"), R("John 6:27-35", "Gospel")]},
            {"slot": "fer_oculi_fri", "name": "Friday of Oculi", "anchor": "lent_3", "offset": 5, "is_sunday": False,
             "readings": [R("Numbers 20:2b-13", "Lesson"), R("John 4:5-42", "Gospel")]},
            {"slot": "fer_oculi_sat", "name": "Saturday of Oculi", "anchor": "lent_3", "offset": 6, "is_sunday": False,
             "readings": [R("Susanna 1:1-9, 15-17, 19-62", "Lesson"), R("John 8:1-11", "Gospel")]},
        ],
    },
    {
        "key": "laetare",
        "name": "Laetare — Fourth Week in Lent",
        "days": [
            {"slot": "laetare", "name": "Laetare (Fourth Sunday in Lent)", "anchor": "lent_4", "offset": 0, "is_sunday": True,
             "readings": [R("Exodus 16:2-21", "Old Testament", "**"), R("Galatians 4:22-31", "Epistle"), R("John 6:1-14", "Gospel", "*")],
             "note": "For the Gospel, LSB adds one verse (John 6:1-15)."},
            {"slot": "fer_laetare_mon", "name": "Monday of Laetare", "anchor": "lent_4", "offset": 1, "is_sunday": False,
             "readings": [R("1 Kings 3:16-28", "Lesson"), R("John 2:13-25", "Gospel")]},
            {"slot": "fer_laetare_tue", "name": "Tuesday of Laetare", "anchor": "lent_4", "offset": 2, "is_sunday": False,
             "readings": [R("Exodus 32:7-14", "Lesson"), R("John 7:14-31a", "Gospel")]},
            {"slot": "fer_laetare_wed", "name": "Wednesday of Laetare", "anchor": "lent_4", "offset": 3, "is_sunday": False,
             "readings": [R("Ezekiel 36:23-28", "First Lesson"), R("Isaiah 1:16-19", "Second Lesson"), R("John 9:1-38", "Gospel")],
             "note": "A day of two lessons — the great baptismal Gospel of the man born blind."},
            {"slot": "fer_laetare_thu", "name": "Thursday of Laetare", "anchor": "lent_4", "offset": 4, "is_sunday": False,
             "readings": [R("2 Kings 4:25-38a", "Lesson"), R("John 5:17-29", "Gospel")]},
            {"slot": "fer_laetare_fri", "name": "Friday of Laetare", "anchor": "lent_4", "offset": 5, "is_sunday": False,
             "readings": [R("1 Kings 17:17-24", "Lesson"), R("John 11:1-45", "Gospel")]},
            {"slot": "fer_laetare_sat", "name": "Saturday of Laetare", "anchor": "lent_4", "offset": 6, "is_sunday": False,
             "readings": [R("Isaiah 49:8-15", "First Lesson"), R("Isaiah 55:1-11", "Second Lesson"), R("John 8:12-20", "Gospel")],
             "note": "A day of two lessons."},
        ],
    },
    {
        "key": "judica",
        "name": "Judica — Fifth Week in Lent (Passiontide)",
        "days": [
            {"slot": "judica", "name": "Judica (Fifth Sunday in Lent)", "anchor": "lent_5", "offset": 0, "is_sunday": True,
             "readings": [R("Genesis 22:1-14", "Old Testament", "**"), R("Hebrews 9:11-15", "Epistle"), R("John 8:46-59", "Gospel")]},
            {"slot": "fer_judica_mon", "name": "Monday of Judica", "anchor": "lent_5", "offset": 1, "is_sunday": False,
             "readings": [R("Jonah 3:1-10a", "Lesson"), R("John 7:32b-39a", "Gospel")]},
            {"slot": "fer_judica_tue", "name": "Tuesday of Judica", "anchor": "lent_5", "offset": 2, "is_sunday": False,
             "readings": [R("Bel and the Dragon 1:29-42, Daniel 6:25-27", "Lesson"), R("John 7:1-13", "Gospel")]},
            {"slot": "fer_judica_wed", "name": "Wednesday of Judica", "anchor": "lent_5", "offset": 3, "is_sunday": False,
             "readings": [R("Leviticus 19:1-2a, 10b-19a, 25b", "Lesson"), R("John 10:22-38", "Gospel")]},
            {"slot": "fer_judica_thu", "name": "Thursday of Judica", "anchor": "lent_5", "offset": 4, "is_sunday": False,
             "readings": [R("Prayer of Azariah 1:11-22", "Lesson"), R("John 7:40-53", "Gospel")]},
            {"slot": "fer_judica_fri", "name": "Friday of Judica", "anchor": "lent_5", "offset": 5, "is_sunday": False,
             "readings": [R("Jeremiah 17:13-18", "Lesson"), R("John 11:47-54", "Gospel")]},
            {"slot": "fer_judica_sat", "name": "Saturday of Judica", "anchor": "lent_5", "offset": 6, "is_sunday": False,
             "readings": [R("Jeremiah 18:18-23", "Lesson"), R("John 17:1-26", "Gospel")]},
        ],
    },
    {
        "key": "holy_week",
        "name": "Holy Week (Palmarum through Good Friday)",
        "days": [
            {"slot": "palmarum", "name": "Palmarum (Palm Sunday / Sixth Sunday in Lent)", "anchor": "palm_sunday", "offset": 0, "is_sunday": True,
             "readings": [R("Zechariah 9:9-12", "Old Testament", "**"), R("Philippians 2:5-11", "Epistle"), R("Matthew 26:1-27:66", "Gospel (Passion)")]},
            {"slot": "fer_holyweek_mon", "name": "Monday of Holy Week", "anchor": "palm_sunday", "offset": 1, "is_sunday": False,
             "readings": [R("Isaiah 50:5-10", "Lesson"), R("Mark 14:1-15:46", "Gospel (Passion)", "*")],
             "note": "The Lutheran / northeast-German order assigns Mark to Monday (LSB has John here)."},
            {"slot": "fer_holyweek_tue", "name": "Tuesday of Holy Week", "anchor": "palm_sunday", "offset": 2, "is_sunday": False,
             "readings": [R("Jeremiah 11:18-20", "Lesson"), R("John 12:1-36", "Gospel", "*")],
             "note": "The Lutheran / northeast-German order assigns John to Tuesday (LSB has Mark here)."},
            {"slot": "fer_holyweek_wed", "name": "Wednesday of Holy Week", "anchor": "palm_sunday", "offset": 3, "is_sunday": False,
             "readings": [R("Isaiah 62:11-63:5, 7a", "First Lesson"), R("Isaiah 53:1-12", "Second Lesson", "*"), R("Luke 22:1-23:53", "Gospel (Passion)")],
             "note": "'Spy Wednesday' — two lessons, closing with the Passion according to St. Luke. Isaiah 53 stands here (historically), not on Good Friday."},
            {"slot": "maundy_thursday_fer", "name": "Maundy Thursday", "anchor": "maundy_thursday", "offset": 0, "is_sunday": False,
             "readings": [R("Exodus 24:3-11", "Old Testament", "**"), R("1 Corinthians 11:20-32", "Epistle", "*"), R("John 13:1-15", "Gospel")]},
            {"slot": "good_friday_fer", "name": "Good Friday", "anchor": "good_friday", "offset": 0, "is_sunday": False,
             "readings": [R("Hosea 5:15b-6:6", "First Lesson", "*"), R("Exodus 12:1-11", "Second Lesson", "*"), R("John 18:1-19:42", "Gospel (Passion)")],
             "note": "Exodus 12 (the Passover lamb) stands here historically, not on Maundy Thursday."},
        ],
    },
]

# The Lutheran Missal's own caution on the Holy Week Gospels (for the help page).
HOLY_WEEK_NOTE = (
    "For Monday and Tuesday of Holy Week, The Lutheran Missal follows the order used by "
    "every catalogued Lutheran source and by the older northeast-German missals — Mark on "
    "Monday, John on Tuesday — even though the wider manuscript record favors the reverse "
    "(the order LSB uses) roughly two to one. The Lutheran usage is taken to preserve an "
    "older tradition 'as yet unaltered by Rome.'"
)

SOURCE_CITATION = (
    "The Lutheran Missal, \"Lenten Lections\" (11 February 2020), "
    "https://lutheranmissal.home.blog/2020/02/11/lenten-lections/ — the historic Western "
    "(Roman-rite) Lenten ferial lectionary in its late-medieval German / Lutheran recension."
)


# --- convenience accessors -------------------------------------------------

def iter_days(include_sundays=True):
    """Yield (week, day) for every entry, in calendar order."""
    for week in LENTEN_WEEKS:
        for day in week["days"]:
            if not include_sundays and day.get("is_sunday"):
                continue
            yield week, day


def all_slots():
    return {day["slot"] for _, day in iter_days()}


def resolve_date(day, cal):
    """Return the calendar date of a ferial day for a given LiturgicalCalendar."""
    from datetime import timedelta
    anchor = getattr(cal, day["anchor"])
    return anchor + timedelta(day["offset"])
