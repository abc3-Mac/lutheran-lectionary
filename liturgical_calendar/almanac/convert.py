"""Calendar conversion: Julian Day Number <-> Julian / Gregorian calendars.

Algorithms from Meeus, *Astronomical Algorithms* (2nd ed.), ch. 7, which
reproduce the method of the *Explanatory Supplement*. Valid for any date in
either calendar; the Julian Day count is continuous across the calendars.

A "Julian Day" (JD) is a continuous count of days since noon UT on
January 1, 4713 BC (Julian). The integer JD changes at noon; the fractional
part measures time from the preceding noon.
"""

import math
from datetime import date, datetime, timedelta


def gregorian_to_jd(year: int, month: int, day: float) -> float:
    """Julian Day for a Gregorian calendar date (day may be fractional)."""
    return _to_jd(year, month, day, gregorian=True)


def julian_to_jd(year: int, month: int, day: float) -> float:
    """Julian Day for a Julian (old-style) calendar date."""
    return _to_jd(year, month, day, gregorian=False)


def _to_jd(year: int, month: int, day: float, gregorian: bool) -> float:
    if month <= 2:
        year -= 1
        month += 12
    if gregorian:
        a = year // 100
        b = 2 - a + a // 4
    else:
        b = 0
    return (int(365.25 * (year + 4716))
            + int(30.6001 * (month + 1))
            + day + b - 1524.5)


def jd_to_gregorian(jd: float) -> tuple[int, int, float]:
    """(year, month, day) in the Gregorian calendar for a Julian Day.

    day is fractional (e.g. 15.5 = noon on the 15th)."""
    return _from_jd(jd, force_julian=False)


def jd_to_julian(jd: float) -> tuple[int, int, float]:
    """(year, month, day) in the Julian calendar for a Julian Day."""
    return _from_jd(jd, force_julian=True)


def _from_jd(jd: float, force_julian: bool) -> tuple[int, int, float]:
    jd += 0.5
    z = int(jd)
    f = jd - z
    # jd_to_gregorian is ALWAYS proleptic Gregorian; jd_to_julian is ALWAYS
    # Julian. (A date-aware hybrid converter would switch at the 1582 reform,
    # but these explicit functions must not.)
    if force_julian:
        a = z
    else:
        # floor, not int(): the argument goes negative before ~AD 400 and
        # int() truncates toward zero, shifting ancient dates by a day.
        alpha = math.floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day


def jd_to_datetime(jd: float) -> datetime:
    """Convert a Julian Day to a (naive, UT) Gregorian datetime."""
    year, month, day_frac = jd_to_gregorian(jd)
    day = int(day_frac)
    rem = day_frac - day
    # Build the date, then add the fractional-day remainder as a timedelta so
    # month/year roll-over is handled by datetime arithmetic.
    base = datetime(year, month, day)
    return base + timedelta(days=rem)


def datetime_to_jd(dt: datetime) -> float:
    """Julian Day for a (UT) Gregorian datetime."""
    day = dt.day + (dt.hour + (dt.minute + (dt.second + dt.microsecond / 1e6) / 60) / 60) / 24
    return gregorian_to_jd(dt.year, dt.month, day)


def julian_to_gregorian(year: int, month: int, day: int) -> date:
    """Convert a Julian-calendar date to the equivalent Gregorian date."""
    jd = julian_to_jd(year, month, day)
    gy, gm, gd = jd_to_gregorian(jd + 0.5)   # +0.5 so integer-noon rounds to the civil day
    return date(gy, gm, int(gd))


def gregorian_to_julian(d: date) -> tuple[int, int, int]:
    """Convert a Gregorian date to the equivalent Julian-calendar (y, m, d)."""
    jd = gregorian_to_jd(d.year, d.month, d.day)
    jy, jm, jd_day = jd_to_julian(jd + 0.5)
    return jy, jm, int(jd_day)


def weekday_name(d: date) -> str:
    """Day of the week for a date (works via the proleptic Gregorian datetime)."""
    return ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"][d.weekday()]
