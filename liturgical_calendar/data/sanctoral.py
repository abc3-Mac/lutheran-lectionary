"""
LCMS Sanctoral Calendar — Principal and Minor Feasts.

Fixed-date observances that may coincide with or displace Sundays.
All readings are per the Lutheran Service Book (LSB).
"""


def _r(ot=None, ps=None, ep=None, go=None):
    return {"ot": ot, "ps": ps, "ep": ep, "go": go}


# Key: slot name used in calculator.py / date_to_slot()
# "month_day" tuple stored alongside for reference

SANCTORAL_SLOTS = {

    # --- November ---
    "st_andrew": {
        "name": "St. Andrew, Apostle",
        "date_str": "Nov 30",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Ezekiel 3:16-21",   "Psalm 19:1-6", "Romans 10:10-18",   "John 1:35-42a"),
    },

    # --- December ---
    "st_thomas": {
        "name": "St. Thomas, Apostle",
        "date_str": "Dec 21",
        "season": "Christmas",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Judges 6:36-40",     "Psalm 136:1-4,23-26","Ephesians 4:7-16","John 20:24-29"),
    },
    "holy_innocents": {
        "name": "The Holy Innocents, Martyrs",
        "date_str": "Dec 28",
        "season": "Christmas",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Jeremiah 31:15-17",  "Psalm 54",     "Revelation 14:1-5", "Matthew 2:13-18"),
    },

    # --- January ---
    "confession_of_st_peter": {
        "name": "The Confession of St. Peter",
        "date_str": "Jan 18",
        "season": "Epiphany",
        "color": "White",
        "feast": True,
        "minor": True,
        "readings": _r("Acts 4:8-13",        "Psalm 118:19-29","2 Peter 1:1-15",   "Mark 8:27-35(36–9:1)"),
    },
    "conversion_of_st_paul": {
        "name": "The Conversion of St. Paul",
        "date_str": "Jan 25",
        "season": "Epiphany",
        "color": "White",
        "feast": True,
        "minor": True,
        "readings": _r("Acts 9:1-22",         "Psalm 67",    "Galatians 1:11-24", "Matthew 19:27-30"),
    },

    # --- February ---
    "presentation_of_lord": {
        "name": "The Presentation of Our Lord",
        "date_str": "Feb 2",
        "season": "Epiphany",
        "color": "White",
        "feast": True,
        "minor": True,
        "readings": _r("Numbers 8:5-22",      "Psalm 84",    "Hebrews 2:14-18",   "Luke 2:22-40"),
    },
    "st_matthias": {
        "name": "St. Matthias, Apostle",
        "date_str": "Feb 24",
        "season": "Epiphany",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Isaiah 66:1-2",       "Psalm 56",    "Acts 1:15-26",      "Matthew 11:25-30"),
    },

    # --- March ---
    "annunciation": {
        "name": "The Annunciation of Our Lord",
        "date_str": "Mar 25",
        "season": "Lent",
        "color": "White",
        "feast": True,
        "minor": False,
        "readings": _r("Isaiah 7:10-14",      "Psalm 45:7-15","Hebrews 10:4-10",  "Luke 1:26-38"),
    },

    # --- April ---
    "st_mark": {
        "name": "St. Mark, Evangelist",
        "date_str": "Apr 25",
        "season": "Easter",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Isaiah 52:7-10",      "Psalm 57",    "Ephesians 4:7-16",  "Mark 16:14-20"),
    },
    "philip_and_james": {
        "name": "St. Philip and St. James, Apostles",
        "date_str": "May 1",
        "season": "Easter",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Isaiah 30:18-21",     "Psalm 49:1-10","James 1:1-12",     "John 14:1-14"),
    },

    # --- May ---
    # (Philip & James above)

    # --- June ---
    "st_barnabas": {
        "name": "St. Barnabas, Apostle",
        "date_str": "Jun 11",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Isaiah 42:5-12",      "Psalm 112",   "Acts 11:19-30",     "Mark 6:7-13"),
    },
    "nativity_of_john_baptist": {
        "name": "The Nativity of St. John the Baptist",
        "date_str": "Jun 24",
        "season": "Pentecost",
        "color": "White",
        "feast": True,
        "minor": False,
        "readings": _r("Isaiah 40:1-5",       "Psalm 85:7-13","Acts 13:13-26",    "Luke 1:57-67,80"),
    },
    "st_peter_st_paul": {
        "name": "St. Peter and St. Paul, Apostles",
        "date_str": "Jun 29",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Ezekiel 34:11-16",    "Psalm 87",    "Acts 15:1-12",      "Mark 8:27-35"),
    },

    # --- July ---
    "st_mary_magdalene": {
        "name": "St. Mary Magdalene",
        "date_str": "Jul 22",
        "season": "Pentecost",
        "color": "White",
        "feast": True,
        "minor": True,
        "readings": _r("Proverbs 31:10-31",   "Psalm 73:23-28","Acts 13:26-33a",  "John 20:11-18"),
    },
    "st_james": {
        "name": "St. James the Elder, Apostle",
        "date_str": "Jul 25",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("1 Kings 19:9-18",     "Psalm 67",    "Acts 11:27–12:3",   "Mark 10:35-45"),
    },

    # --- August ---
    "st_bartholomew": {
        "name": "St. Bartholomew, Apostle",
        "date_str": "Aug 24",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Proverbs 3:1-7",      "Psalm 12",    "2 Corinthians 4:7-10","John 1:43-51"),
    },

    # --- September ---
    "st_matthew": {
        "name": "St. Matthew, Apostle and Evangelist",
        "date_str": "Sep 21",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Ezekiel 2:8–3:11",    "Psalm 119:33-40","Ephesians 4:7-16","Matthew 9:9-13"),
    },
    "st_michael": {
        "name": "St. Michael and All Angels",
        "date_str": "Sep 29",
        "season": "Pentecost",
        "color": "White",
        "feast": True,
        "minor": False,
        "readings": _r("Daniel 10:10-14;12:1-3","Psalm 91", "Revelation 12:7-12","Matthew 18:1-11 | Luke 10:17-20"),
    },
    "st_luke": {
        "name": "St. Luke, Evangelist",
        "date_str": "Oct 18",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Isaiah 35:5-8",       "Psalm 147:1-11","2 Timothy 4:5-18","Luke 10:1-9"),
    },

    # --- October ---
    "simon_and_jude": {
        "name": "St. Simon and St. Jude, Apostles",
        "date_str": "Oct 28",
        "season": "Pentecost",
        "color": "Red",
        "feast": True,
        "minor": True,
        "readings": _r("Jeremiah 26:1-16",    "Psalm 11",    "1 John 4:1-6",      "John 15:17-21"),
    },

    # --- November ---
    "all_saints": {
        "name": "All Saints' Day",
        "date_str": "Nov 1",
        "season": "Pentecost",
        "color": "White",
        "feast": True,
        "minor": False,
        "readings": _r("Revelation 7:(2-8)9-17","Psalm 149", "1 John 3:1-3",     "Matthew 5:1-12"),
    },
}
