"""
The History of the Passion — Common Service Book of the Lutheran Church (1917).

"The History of the Passion of our Lord as Recorded by the Four Evangelists"
(Common Service Book, 1917, pp. 250–262) is a harmony of the four Gospels'
Passion narratives, arranged by John Caspar Mattes and divided into SEVEN Parts.
It is the distinctly Lutheran way of keeping the Passion in the weeks of Lent
and Holy Week — a continuous reading, as opposed to the Roman daily ferial
Mass lectionary (see lenten_ferial.py).

THE CSB'S OWN RUBRICS (p. 250), which authorize both reading schedules:
  ¶ The History of the Passion may be read as the Lesson at Matins or Vespers
    during Holy Week, beginning with the Vespers of Palm Sunday.
  ¶ Or it may be read during Lent, and repeated during Holy Week.
  ¶ Suitable hymns may be sung between the paragraphs of each Part of the History.

TEXT POLICY
-----------
We reproduce the CSB's *division markers* (the seven Parts, their scope, and its
rubrics) but do NOT re-key the Passion text from the archive.org OCR, which is
error-laden — that would risk corrupting Scripture (cf. the standing rule to
never hand-type liturgical data). Instead each Part links to the clean public-
domain **KJV** text of the passages it harmonizes (the CSB text is itself KJV-
based). The scan of the CSB arrangement is linked for the exact wording.

The two schedules map the seven Parts onto seven days. There are, providentially,
exactly seven Wednesdays from Ash Wednesday through Wednesday of Holy Week, so the
Lenten-midweek schedule assigns one Part to each. The Holy Week schedule follows
the rubric, "beginning with the Vespers of Palm Sunday," one Part per day through
Holy Saturday.

Source: Common Service Book of the Lutheran Church (Philadelphia, 1917),
"The History of the Passion," pp. 250–262 — public domain. Scan:
https://archive.org/details/commonserviceboo1917phil
"""

TRADITION = "lutheran"
TRACK = "passion_history"

BIBLE_VERSION = "KJV"   # the CSB Passion History is KJV-based

CSB_RUBRICS = [
    "The History of the Passion may be read as the Lesson at Matins or Vespers "
    "during Holy Week, beginning with the Vespers of Palm Sunday.",
    "Or it may be read during Lent, and repeated during Holy Week.",
    "Suitable hymns may be sung between the paragraphs of each Part of the History.",
]

SCAN_URL = "https://archive.org/details/commonserviceboo1917phil/page/250"

SOURCE_CITATION = (
    "Common Service Book of the Lutheran Church (Philadelphia, 1917), "
    "\"The History of the Passion of our Lord as Recorded by the Four Evangelists\" "
    "(arr. John Caspar Mattes), pp. 250–262 — public domain."
)

# --- the seven Parts -------------------------------------------------------
# `refs` are the principal Gospel passages the Part harmonizes (in narrative
# order); the CSB weaves all four Evangelists together within each Part.

PARTS = [
    {
        "n": 1, "title": "The Anointing at Bethany and the Entry into Jerusalem",
        "incipit": "Then Jesus six days before the passover came to Bethany…",
        "summary": "The supper at Bethany and Mary's anointing, the triumphal entry into "
                   "Jerusalem, and the days of teaching in the temple.",
        "refs": ["John 12:1-36", "Matthew 21:1-17", "Mark 11:1-26", "Luke 19:29-48"],
    },
    {
        "n": 2, "title": "The Betrayal Plotted and the Last Supper",
        "incipit": "Now the feast of unleavened bread drew nigh…",
        "summary": "The rulers' plot, Judas' bargain for thirty pieces of silver, the "
                   "preparing of the Passover, and the Last Supper with the institution "
                   "of the Lord's Supper.",
        "refs": ["Matthew 26:1-35", "Mark 14:1-31", "Luke 22:1-38", "John 13:1-38"],
    },
    {
        "n": 3, "title": "The High-Priestly Prayer and Gethsemane",
        "incipit": "These words spake Jesus, and lifted up his eyes to heaven…",
        "summary": "Our Lord's high-priestly prayer, the agony in the Garden of "
                   "Gethsemane, and the betrayal and arrest.",
        "refs": ["John 17:1-26", "John 18:1-11", "Matthew 26:36-56", "Mark 14:32-52", "Luke 22:39-53"],
    },
    {
        "n": 4, "title": "Before the High Priest; Peter's Denial",
        "incipit": "Then the band and the captain and officers of the Jews took Jesus…",
        "summary": "Jesus led to Annas and Caiaphas, the false witnesses and the high "
                   "priest's adjuration, and Peter's threefold denial.",
        "refs": ["John 18:12-27", "Matthew 26:57-75", "Mark 14:53-72", "Luke 22:54-71"],
    },
    {
        "n": 5, "title": "The Trial before Pilate",
        "incipit": "Then led they Jesus from Caiaphas unto the hall of judgment…",
        "summary": "Jesus before Pilate and Herod, the end of Judas, Barabbas, the "
                   "scourging and mocking, and the sentence of death.",
        "refs": ["John 18:28-19:16", "Matthew 27:1-31", "Mark 15:1-20", "Luke 23:1-25"],
    },
    {
        "n": 6, "title": "The Crucifixion and Death of Our Lord",
        "incipit": "And they took Jesus, and when they had mocked him…",
        "summary": "The way to Golgotha, the crucifixion between the two thieves, the "
                   "seven words, and the death of Jesus.",
        "refs": ["Matthew 27:31-50", "Mark 15:20-37", "Luke 23:26-46", "John 19:16-30"],
        "rubric": "At the words, \"He bowed his head, and gave up the ghost,\" all may kneel "
                  "and silently say the Lord's Prayer or other suitable prayers.",
    },
    {
        "n": 7, "title": "The Burial and the Sealing of the Tomb",
        "incipit": "There were also women looking on afar off…",
        "summary": "The women who watched from afar, the piercing of Jesus' side, the "
                   "burial by Joseph of Arimathea and Nicodemus, and the sealing and "
                   "guarding of the sepulchre.",
        "refs": ["Matthew 27:51-66", "Mark 15:38-47", "Luke 23:47-56", "John 19:31-42"],
    },
]

# --- schedules: (anchor attribute, offset days) per Part, in order ----------

SCHEDULES = {
    "wednesdays": {
        "label": "Wednesdays of Lent",
        "blurb": "One Part at each Lenten midweek service — the seven Wednesdays from "
                 "Ash Wednesday through Wednesday of Holy Week.",
        "days": [
            ("Ash Wednesday",           "ash_wednesday", 0),
            ("Wednesday of Invocavit",  "lent_1", 3),
            ("Wednesday of Reminiscere","lent_2", 3),
            ("Wednesday of Oculi",      "lent_3", 3),
            ("Wednesday of Laetare",    "lent_4", 3),
            ("Wednesday of Judica",     "lent_5", 3),
            ("Wednesday of Holy Week",  "palm_sunday", 3),
        ],
    },
    "holy_week": {
        "label": "Holy Week",
        "blurb": "One Part per day through Holy Week, beginning with the Vespers of Palm "
                 "Sunday, as the CSB's first rubric directs.",
        "days": [
            ("Palm Sunday (Vespers)", "palm_sunday", 0),
            ("Monday of Holy Week",   "palm_sunday", 1),
            ("Tuesday of Holy Week",  "palm_sunday", 2),
            ("Wednesday of Holy Week","palm_sunday", 3),
            ("Maundy Thursday",       "maundy_thursday", 0),
            ("Good Friday",           "good_friday", 0),
            ("Holy Saturday",         "good_friday", 1),
        ],
    },
}


def resolve_schedule(schedule_key, cal):
    """Return list of (part, day_label, date) for a schedule in a given year."""
    from datetime import timedelta
    sched = SCHEDULES[schedule_key]
    out = []
    for part, (label, anchor, offset) in zip(PARTS, sched["days"]):
        d = getattr(cal, anchor) + timedelta(offset)
        out.append((part, label, d))
    return out
