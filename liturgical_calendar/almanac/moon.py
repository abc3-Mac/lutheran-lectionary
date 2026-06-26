"""Astronomical Moon phases — Meeus, *Astronomical Algorithms* (2nd ed.), ch. 49.

Computes the four principal phases (new, first quarter, full, last quarter) to
roughly a minute of accuracy for the modern era, returned as UT datetimes.
Pure Python, no dependencies. Results are cross-validated against USNO published
phase times in the test-suite (per the project's data-verification rule).

Times are TD (Dynamical Time) from Meeus' series; we subtract Delta-T to return
UT, which is what USNO and civil clocks use. Delta-T uses the Espenak-Meeus
polynomials.

Public API:
    phases_in_range(start, end)  -> list[MoonPhase]   (all four phases)
    full_moons(year) / new_moons(year)
    blue_moons(year)             -> monthly + seasonal blue moons
    phase_at(date)               -> (illuminated_fraction, phase_name, waxing)
"""

import math
from datetime import date, datetime, timedelta

from .convert import (jd_to_datetime, datetime_to_jd, jd_to_gregorian,
                      jd_to_julian, gregorian_to_jd)

_RAD = math.pi / 180.0

NEW_MOON = "New moon"
FIRST_QUARTER = "First quarter"
FULL_MOON = "Full moon"
LAST_QUARTER = "Last quarter"

_PHASE_NAMES = {0.0: NEW_MOON, 0.25: FIRST_QUARTER, 0.5: FULL_MOON, 0.75: LAST_QUARTER}


class MoonPhase:
    """A single principal phase event."""

    __slots__ = ("dt", "phase", "jde")

    def __init__(self, dt: datetime, phase: str, jde: float):
        self.dt = dt            # UT datetime (naive)
        self.phase = phase      # one of the four phase-name constants
        self.jde = jde          # Julian Ephemeris Day (TD) of the phase

    @property
    def date(self) -> date:
        return self.dt.date()

    def __repr__(self):
        return f"MoonPhase({self.dt:%Y-%m-%d %H:%M} UT, {self.phase})"


def delta_t_seconds(year: float) -> float:
    """Delta-T (TD - UT) in seconds, Espenak & Meeus polynomial fit."""
    y = year
    if y < -500:
        u = (y - 1820) / 100.0
        return -20 + 32 * u * u
    if y < 500:
        u = y / 100.0
        return (10583.6 - 1014.41 * u + 33.78311 * u**2 - 5.952053 * u**3
                - 0.1798452 * u**4 + 0.022174192 * u**5 + 0.0090316521 * u**6)
    if y < 1600:
        u = (y - 1000) / 100.0
        return (1574.2 - 556.01 * u + 71.23472 * u**2 + 0.319781 * u**3
                - 0.8503463 * u**4 - 0.005050998 * u**5 + 0.0083572073 * u**6)
    if y < 1700:
        t = y - 1600
        return 120 - 0.9808 * t - 0.01532 * t**2 + t**3 / 7129.0
    if y < 1800:
        t = y - 1700
        return (8.83 + 0.1603 * t - 0.0059285 * t**2 + 0.00013336 * t**3
                - t**4 / 1174000.0)
    if y < 1860:
        t = y - 1800
        return (13.72 - 0.332447 * t + 0.0068612 * t**2 + 0.0041116 * t**3
                - 0.00037436 * t**4 + 0.0000121272 * t**5
                - 0.0000001699 * t**6 + 0.000000000875 * t**7)
    if y < 1900:
        t = y - 1860
        return (7.62 + 0.5737 * t - 0.251754 * t**2 + 0.01680668 * t**3
                - 0.0004473624 * t**4 + t**5 / 233174.0)
    if y < 1920:
        t = y - 1900
        return (-2.79 + 1.494119 * t - 0.0598939 * t**2 + 0.0061966 * t**3
                - 0.000197 * t**4)
    if y < 1941:
        t = y - 1920
        return 21.20 + 0.84493 * t - 0.076100 * t**2 + 0.0020936 * t**3
    if y < 1961:
        t = y - 1950
        return 29.07 + 0.407 * t - t**2 / 233.0 + t**3 / 2547.0
    if y < 1986:
        t = y - 1975
        return 45.45 + 1.067 * t - t**2 / 260.0 - t**3 / 718.0
    if y < 2005:
        t = y - 2000
        return (63.86 + 0.3345 * t - 0.060374 * t**2 + 0.0017275 * t**3
                + 0.000651814 * t**4 + 0.00002373599 * t**5)
    if y < 2050:
        t = y - 2000
        return 62.92 + 0.32217 * t + 0.005589 * t**2
    if y < 2150:
        return -20 + 32 * ((y - 1820) / 100.0) ** 2 - 0.5628 * (2150 - y)
    u = (y - 1820) / 100.0
    return -20 + 32 * u * u


def _mean_phase_jde(k: float) -> tuple[float, float]:
    """Mean JDE of phase k and the time argument T."""
    T = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k
           + 0.00015437 * T**2 - 0.000000150 * T**3 + 0.00000000073 * T**4)
    return jde, T


def _phase_correction(k: float, T: float, phase_frac: float) -> float:
    """Periodic corrections (days) to add to the mean phase JDE."""
    E = 1 - 0.002516 * T - 0.0000074 * T**2
    M = (2.5534 + 29.10535670 * k - 0.0000014 * T**2 - 0.00000011 * T**3) * _RAD
    Mp = (201.5643 + 385.81693528 * k + 0.0107582 * T**2
          + 0.00001238 * T**3 - 0.000000058 * T**4) * _RAD
    F = (160.7108 + 390.67050284 * k - 0.0016118 * T**2
         - 0.00000227 * T**3 + 0.000000011 * T**4) * _RAD
    Om = (124.7746 - 1.56375588 * k + 0.0020672 * T**2 + 0.00000215 * T**3) * _RAD

    sin = math.sin
    cos = math.cos

    if phase_frac in (0.0, 0.5):   # new moon / full moon share the same table
        if phase_frac == 0.0:
            c = -0.40720 * sin(Mp)
        else:
            c = -0.40614 * sin(Mp)
        c += (0.17241 * E * sin(M)
              + 0.01608 * sin(2 * Mp)
              + 0.01039 * sin(2 * F)
              + 0.00739 * E * sin(Mp - M)
              - 0.00514 * E * sin(Mp + M)
              + 0.00208 * E * E * sin(2 * M)
              - 0.00111 * sin(Mp - 2 * F)
              - 0.00057 * sin(Mp + 2 * F)
              + 0.00056 * E * sin(2 * Mp + M)
              - 0.00042 * sin(3 * Mp)
              + 0.00042 * E * sin(M + 2 * F)
              + 0.00038 * E * sin(M - 2 * F)
              - 0.00024 * E * sin(2 * Mp - M)
              - 0.00017 * sin(Om)
              - 0.00007 * sin(Mp + 2 * M)
              + 0.00004 * sin(2 * Mp - 2 * F)
              + 0.00004 * sin(3 * M)
              + 0.00003 * sin(Mp + M - 2 * F)
              + 0.00003 * sin(2 * Mp + 2 * F)
              - 0.00003 * sin(Mp + M + 2 * F)
              + 0.00003 * sin(Mp - M + 2 * F)
              - 0.00002 * sin(Mp - M - 2 * F)
              - 0.00002 * sin(3 * Mp + M)
              + 0.00002 * sin(4 * Mp))
    else:                          # first / last quarter
        c = (-0.62801 * sin(Mp)
             + 0.17172 * E * sin(M)
             - 0.01183 * E * sin(Mp + M)
             + 0.00862 * sin(2 * Mp)
             + 0.00804 * sin(2 * F)
             + 0.00454 * E * sin(Mp - M)
             + 0.00204 * E * E * sin(2 * M)
             - 0.00180 * sin(Mp - 2 * F)
             - 0.00070 * sin(Mp + 2 * F)
             - 0.00040 * sin(3 * Mp)
             - 0.00034 * E * sin(2 * Mp - M)
             + 0.00032 * E * sin(M + 2 * F)
             + 0.00032 * E * sin(M - 2 * F)
             - 0.00028 * E * E * sin(Mp + 2 * M)
             + 0.00027 * E * sin(2 * Mp + M)
             - 0.00017 * sin(Om)
             - 0.00005 * sin(Mp - M - 2 * F)
             + 0.00004 * sin(2 * Mp + 2 * F)
             - 0.00004 * sin(Mp + M + 2 * F)
             + 0.00004 * sin(Mp - 2 * M)
             + 0.00003 * sin(Mp + M - 2 * F)
             + 0.00003 * sin(3 * M)
             + 0.00002 * sin(2 * Mp - 2 * F)
             + 0.00002 * sin(Mp - M + 2 * F)
             - 0.00002 * sin(3 * Mp + M))
        W = (0.00306 - 0.00038 * E * cos(M) + 0.00026 * cos(Mp)
             - 0.00002 * cos(Mp - M) + 0.00002 * cos(Mp + M) + 0.00002 * cos(2 * F))
        c += W if phase_frac == 0.25 else -W

    # Planetary-argument corrections (common to all phases)
    A = [
        (299.77 + 0.107408 * k - 0.009173 * T**2, 0.000325),
        (251.88 + 0.016321 * k, 0.000165),
        (251.83 + 26.651886 * k, 0.000164),
        (349.42 + 36.412478 * k, 0.000126),
        (84.66 + 18.206239 * k, 0.000110),
        (141.74 + 53.303771 * k, 0.000062),
        (207.14 + 2.453732 * k, 0.000060),
        (154.84 + 7.306860 * k, 0.000056),
        (34.52 + 27.261239 * k, 0.000047),
        (207.19 + 0.121824 * k, 0.000042),
        (291.34 + 1.844379 * k, 0.000040),
        (161.72 + 24.198154 * k, 0.000037),
        (315.56 + 2.512799 * k, 0.000035),
        (105.18 + 5.323105 * k, 0.000023),
        (202.94 + 0.943311 * k, 0.000023),
    ]
    for angle_deg, coeff in A:
        c += coeff * sin(angle_deg * _RAD)
    return c


def _phase_jde(k_int: int, phase_frac: float) -> float:
    """JDE (TD) of the phase with integer index k_int and fraction phase_frac."""
    k = k_int + phase_frac
    jde, T = _mean_phase_jde(k)
    return jde + _phase_correction(k, T, phase_frac)


def _k_for_date(d: date) -> float:
    """Approximate (real) lunation index near date d."""
    y = d.year + (d.timetuple().tm_yday - 1) / 365.25
    return (y - 2000) * 12.3685


def phases_in_range(start: date, end: date) -> list[MoonPhase]:
    """All principal phases with UT date in [start, end], chronological."""
    k0 = math.floor(_k_for_date(start)) - 2
    k1 = math.ceil(_k_for_date(end)) + 2
    out = []
    for k_int in range(k0, k1 + 1):
        for frac in (0.0, 0.25, 0.5, 0.75):
            jde = _phase_jde(k_int, frac)
            dt = jd_to_datetime(jde)
            # convert TD -> UT
            dt -= timedelta(seconds=delta_t_seconds(dt.year + (dt.month - 1) / 12))
            if start <= dt.date() <= end:
                out.append(MoonPhase(dt, _PHASE_NAMES[frac], jde))
    out.sort(key=lambda p: p.dt)
    return out


def full_moons(year: int) -> list[MoonPhase]:
    return [p for p in phases_in_range(date(year, 1, 1), date(year, 12, 31))
            if p.phase == FULL_MOON]


def new_moons(year: int) -> list[MoonPhase]:
    return [p for p in phases_in_range(date(year, 1, 1), date(year, 12, 31))
            if p.phase == NEW_MOON]


def nearest_full_moon(d: date) -> MoonPhase:
    """The astronomical full moon whose UT date is closest to d."""
    candidates = phases_in_range(d - timedelta(days=20), d + timedelta(days=20))
    fulls = [p for p in candidates if p.phase == FULL_MOON]
    return min(fulls, key=lambda p: abs((p.date - d).days))


def blue_moons(year: int) -> list[dict]:
    """Blue moons in a calendar year, both common definitions.

    - "monthly": the second full moon within a single calendar month.
    - "seasonal": the third full moon in an astronomical season that has four
      (the older, almanac, definition).
    """
    fulls = full_moons(year)
    out = []

    by_month: dict[int, list[MoonPhase]] = {}
    for p in fulls:
        by_month.setdefault(p.dt.month, []).append(p)
    for month, ps in by_month.items():
        if len(ps) >= 2:
            out.append({"kind": "monthly", "date": ps[1].date, "phase": ps[1]})

    for season_start, season_end, label in _seasons(year):
        seasonal = [p for p in phases_in_range(season_start, season_end)
                    if p.phase == FULL_MOON]
        if len(seasonal) == 4 and seasonal[2].dt.year == year:
            out.append({"kind": "seasonal", "season": label,
                        "date": seasonal[2].date, "phase": seasonal[2]})

    out.sort(key=lambda b: b["date"])
    return out


# ---------------------------------------------------------------------------
# BC-capable path (works in Julian Day space; no Python date/datetime, so it
# handles years <= 0, which datetime cannot represent). Used for the Passover
# reconstruction back to the Exodus era. Years are astronomical numbering
# (0 = 1 BC, -1 = 2 BC, ...).
# ---------------------------------------------------------------------------

# Nominal March equinox on the (proleptic) Gregorian calendar; the Gregorian
# calendar is designed to hold the equinox near March 20, and the proleptic
# extension keeps it there for ancient years too. Good enough for classifying
# the "first full moon after the equinox" (Passover/Paschal moon).
_NOMINAL_MARCH_EQUINOX_DAY = 20.5


def _full_moon_jd_ut(k_int: int) -> tuple[float, float]:
    """(jd_ut, jde) for the full moon of integer lunation index k_int."""
    jde = _phase_jde(k_int, 0.5)
    gy, gm, _ = jd_to_gregorian(jde)
    jd_ut = jde - delta_t_seconds(gy + (gm - 1) / 12.0) / 86400.0
    return jd_ut, jde


def _moment(jd_ut: float, jde: float) -> dict:
    """Describe a JD instant on both calendars, BC-safe (tuples, not dates)."""
    gy, gm, gday = jd_to_gregorian(jd_ut)
    jy, jm, jday = jd_to_julian(jd_ut)
    frac = gday - int(gday)
    hours = frac * 24.0
    h = int(hours)
    mi = int(round((hours - h) * 60))
    if mi == 60:
        h, mi = h + 1, 0
    return {
        "jd_ut": jd_ut, "jde": jde,
        "gregorian": (gy, gm, int(gday)),
        "julian": (jy, jm, int(jday)),
        "hour": h, "minute": mi,
    }


def full_moon_near(jd_target: float) -> dict:
    """The full moon whose UT instant is closest to jd_target. BC-safe."""
    gy, gm, _ = jd_to_gregorian(jd_target)
    kf = (gy + (gm - 1) / 12.0 - 2000) * 12.3685
    best = None
    for k_int in range(math.floor(kf) - 2, math.floor(kf) + 3):
        jd_ut, jde = _full_moon_jd_ut(k_int)
        if best is None or abs(jd_ut - jd_target) < abs(best[0] - jd_target):
            best = (jd_ut, jde)
    return _moment(*best)


def spring_full_moon(year: int) -> dict:
    """First full moon on or after the March equinox (the Passover / Paschal
    full moon), for any astronomical year including BC. BC-safe."""
    equinox_jd = gregorian_to_jd(year, 3, _NOMINAL_MARCH_EQUINOX_DAY)
    kf = (year + 0.22 - 2000) * 12.3685     # ~late March of `year`
    for k_int in range(math.floor(kf) - 3, math.floor(kf) + 4):
        jd_ut, jde = _full_moon_jd_ut(k_int)
        if jd_ut >= equinox_jd:
            return _moment(jd_ut, jde)
    raise ValueError(f"no spring full moon found for year {year}")


_SYNODIC = 29.530588861   # mean length of a lunation, days


def phase_at(d: date) -> dict:
    """Approximate Moon appearance at noon UT on date d.

    Returns {age_days, illumination (0..1), waxing (bool), phase} where phase is
    the nearest descriptive name. Age-based — accurate enough to drive a phase
    icon; for exact event times use phases_in_range()."""
    noon = datetime(d.year, d.month, d.day, 12)
    window = phases_in_range(d - timedelta(days=40), d + timedelta(days=40))
    new_before = [p for p in window if p.phase == NEW_MOON and p.dt <= noon]
    if not new_before:
        age = 0.0
    else:
        age = (noon - new_before[-1].dt).total_seconds() / 86400.0
    frac = (age % _SYNODIC) / _SYNODIC
    illum = (1 - math.cos(2 * math.pi * frac)) / 2
    waxing = frac < 0.5
    phase = _describe(frac)
    return {"age_days": age, "illumination": illum, "waxing": waxing, "phase": phase}


def _describe(frac: float) -> str:
    """Descriptive phase name for a fraction-of-lunation in [0, 1)."""
    eighth = 1.0 / 8
    if frac < eighth / 2 or frac >= 1 - eighth / 2:
        return NEW_MOON
    if frac < 0.25 - eighth / 2:
        return "Waxing crescent"
    if frac < 0.25 + eighth / 2:
        return FIRST_QUARTER
    if frac < 0.5 - eighth / 2:
        return "Waxing gibbous"
    if frac < 0.5 + eighth / 2:
        return FULL_MOON
    if frac < 0.75 - eighth / 2:
        return "Waning gibbous"
    if frac < 0.75 + eighth / 2:
        return LAST_QUARTER
    return "Waning crescent"


def _seasons(year: int):
    """Approximate astronomical season boundaries (UT) for blue-moon counting.

    Equinox/solstice dates vary by ~a day; for counting full moons per season a
    fixed-date approximation is sufficient and deterministic. Seasons that span
    the year boundary are clipped to the calendar year."""
    return [
        (date(year, 3, 20), date(year, 6, 20), "spring"),
        (date(year, 6, 21), date(year, 9, 21), "summer"),
        (date(year, 9, 22), date(year, 12, 20), "autumn"),
        (date(year, 12, 21), date(year, 12, 31), "winter"),
    ]
