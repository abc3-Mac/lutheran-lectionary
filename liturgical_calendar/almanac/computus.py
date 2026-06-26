"""Date of Easter and the movable feasts that hang off it.

Western (Gregorian) Easter uses the anonymous Gregorian algorithm (Meeus/Gauss);
Eastern (Orthodox) Easter uses the Julian computus, returned as the equivalent
Gregorian date. Both are exact integer arithmetic.

The movable-feast offsets are fixed counts of days from Easter, so the same
helper serves either tradition.
"""

from datetime import date, timedelta

from .convert import (julian_to_gregorian, julian_to_jd, jd_to_julian,
                      gregorian_to_julian)

# The Julian/Gregorian split: the Gregorian calendar begins 1582-10-15.
# Dates in earlier years are reckoned on the Julian calendar.
GREGORIAN_START_YEAR = 1583
NICAEA_YEAR = 325


def gregorian_easter(year: int) -> date:
    """Western (Gregorian) Easter Sunday. Valid 1583 onward."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def golden_number(year: int) -> int:
    """Golden number (year's place in the 19-year Metonic cycle), 1..19."""
    return year % 19 + 1


# The ecclesiastical equinox is FIXED at March 21 by the computus — it does not
# track the (variable) astronomical equinox, which falls on March 19-20 today.
ECCLESIASTICAL_EQUINOX = (3, 21)


def paschal_full_moon(year: int) -> date:
    """Ecclesiastical Paschal Full Moon (Gregorian date).

    This is the *tabular* full moon of the computus, not the astronomical one:
    Easter is the first Sunday strictly after this date. It can differ from the
    true astronomical full moon by a day or more, because the lunar calendar is
    an approximation reset on a 19-year cycle with Gregorian corrections."""
    a = year % 19
    b = year // 100
    d = b // 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    # Clavius lunar corrections so the ecclesiastical full moon stays in bounds.
    if h == 29:
        offset = 28          # -> April 18
    elif h == 28 and a > 10:
        offset = 27          # -> April 17
    else:
        offset = h
    return date(year, 3, 21) + timedelta(days=offset)


def julian_easter_old_style(year: int) -> tuple[int, int, int]:
    """Julian (Alexandrian) computus Easter as an Old-Style (y, m, d) tuple.

    This is the date as reckoned and observed on the *Julian* calendar. It is
    the basis of both the pre-1582 Western Easter and the modern Orthodox
    Easter, and can be projected to any year (though it is only *historical*
    from roughly the 4th century — see paschal-controversy note in the docs)."""
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31      # 3 = March, 4 = April (Julian calendar)
    day = ((d + e + 114) % 31) + 1
    return year, month, day


def julian_paschal_full_moon_old_style(year: int) -> tuple[int, int, int]:
    """Julian-computus Paschal full moon, Old-Style (y, m, d).

    The Julian ecclesiastical full moon is simply d days after March 21
    (Julian); unlike the Gregorian computus it carries no Clavius corrections."""
    c = year % 19
    d = (19 * c + 15) % 30
    total = 21 + d                       # day-of-March; March has 31 days
    if total <= 31:
        return year, 3, total
    return year, 4, total - 31


def orthodox_easter(year: int) -> date:
    """Eastern (Orthodox) Easter Sunday, as a Gregorian date.

    The Julian computus result converted from the Julian to the Gregorian
    calendar (so it can be placed on a modern calendar)."""
    y, m, d = julian_easter_old_style(year)
    return julian_to_gregorian(y, m, d)


# Movable feasts as day-offsets from Easter Sunday.
MOVABLE_OFFSETS = {
    "septuagesima":   -63,
    "sexagesima":     -56,
    "quinquagesima":  -49,
    "ash_wednesday":  -46,
    "lent_1":         -42,
    "palm_sunday":     -7,
    "maundy_thursday": -3,
    "good_friday":     -2,
    "holy_saturday":   -1,
    "easter":           0,
    "ascension":       39,
    "pentecost":       49,
    "trinity":         56,
    "corpus_christi":  60,
}


def movable_feasts(year: int, tradition: str = "western") -> dict[str, date]:
    """All movable feasts for a year, keyed by name. tradition: western|eastern."""
    easter = orthodox_easter(year) if tradition == "eastern" else gregorian_easter(year)
    return {name: easter + timedelta(days=off) for name, off in MOVABLE_OFFSETS.items()}


def easter_moon_comparison(year: int) -> dict:
    """Contrast the ecclesiastical computus with the astronomical sky.

    Shows that Easter's "first full moon after the equinox" uses the *tabular*
    moon and a *fixed* March 21 equinox — which need not match the astronomical
    full moon. `delta_days` is the gap between the ecclesiastical and the nearest
    astronomical full moon.

    Era-aware: from 1583 it uses the Gregorian computus on the Gregorian
    calendar; earlier it uses the Julian (Alexandrian) computus on the Julian
    calendar. All date fields are returned as proleptic-Gregorian `date`s for
    plotting against the astronomical sky; `*_os` give the Old-Style Julian
    (y, m, d) when the Julian calendar applies, else None."""
    from . import moon

    gregorian = year >= GREGORIAN_START_YEAR
    if gregorian:
        pfm = paschal_full_moon(year)                 # Gregorian-calendar date
        equinox = date(year, *ECCLESIASTICAL_EQUINOX)
        easter = gregorian_easter(year)
        pfm_os = equinox_os = easter_os = None
    else:
        pfm_os = julian_paschal_full_moon_old_style(year)
        pfm = julian_to_gregorian(*pfm_os)            # Gregorian-equivalent
        equinox_os = (year, 3, 21)
        equinox = julian_to_gregorian(*equinox_os)
        easter_os = julian_easter_old_style(year)
        easter = julian_to_gregorian(*easter_os)

    astro = moon.nearest_full_moon(pfm)
    return {
        "year": year,
        "calendar": "Gregorian" if gregorian else "Julian",
        "before_nicaea": year < NICAEA_YEAR,
        "golden_number": golden_number(year),
        "ecclesiastical_equinox": equinox,
        "ecclesiastical_equinox_os": equinox_os,
        "ecclesiastical_full_moon": pfm,
        "ecclesiastical_full_moon_os": pfm_os,
        "astronomical_full_moon": astro.date,
        "astronomical_full_moon_ut": astro.dt,
        "delta_days": (astro.date - pfm).days,
        "easter": easter,
        "easter_os": easter_os,
    }


def historical_easter(year: int) -> dict:
    """Date of Easter with the historically-appropriate reckoning and calendar.

    Returns Gregorian-equivalent `date`s plus Old-Style (y, m, d) for the Julian
    era, and flags so callers can label retrojections honestly."""
    gregorian = year >= GREGORIAN_START_YEAR
    julian_os = julian_easter_old_style(year)
    return {
        "year": year,
        "calendar": "Gregorian" if gregorian else "Julian",
        "before_nicaea": year < NICAEA_YEAR,
        "western": gregorian_easter(year) if gregorian else None,
        "easter_os": None if gregorian else julian_os,
        "easter": gregorian_easter(year) if gregorian else julian_to_gregorian(*julian_os),
        "orthodox_os": julian_os,
        "orthodox_gregorian": orthodox_easter(year),
    }


def easter_table(start_year: int, end_year: int, tradition: str = "western") -> list[dict]:
    """Rows of {year, easter, ...key movable feasts} for a year range."""
    fn = orthodox_easter if tradition == "eastern" else gregorian_easter
    rows = []
    for y in range(start_year, end_year + 1):
        e = fn(y)
        rows.append({
            "year": y,
            "ash_wednesday": e + timedelta(days=-46),
            "easter": e,
            "ascension": e + timedelta(days=39),
            "pentecost": e + timedelta(days=49),
        })
    return rows
