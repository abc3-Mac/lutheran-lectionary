"""
Civil / secular holiday awareness (Roadmap E).

These are *informational overlays only* — civil observances that fall on or near
a Sunday affect attendance, themes, and announcements, so planners like to see
them next to the liturgical day. They are NEVER liturgical propers and must
never be confused with feasts of the Church.

Moveable holidays (Mother's/Father's Day, Memorial Day, Thanksgiving, …) are
derived programmatically rather than hand-typed, per the project's
data-verification rule. Fixed-date holidays use their actual calendar date, not
the Monday on which a federal office may *observe* them — the point is awareness
of the day people associate with the holiday, including when it lands on a
Sunday.

Scope: USA first. The registry is keyed by country so other countries can be
added later (per-country opt-in), dovetailing with the multi-tradition/locale
work on the roadmap.
"""

from datetime import date, timedelta


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """The n-th `weekday` of a month. weekday uses isoweekday: Mon=1 … Sun=7."""
    first = date(year, month, 1)
    offset = (weekday - first.isoweekday()) % 7
    return first + timedelta(offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    """The last `weekday` of a month. weekday uses isoweekday: Mon=1 … Sun=7."""
    if month == 12:
        last = date(year, 12, 31)
    else:
        last = date(year, month + 1, 1) - timedelta(1)
    return last - timedelta((last.isoweekday() - weekday) % 7)


def _nearest_sunday(d: date) -> date:
    """The Sunday nearest to date d (ties go forward — same rule the church-year
    calculator uses for observed feasts like St. Michael)."""
    dow = d.isoweekday()  # Mon=1 … Sun=7
    if dow == 7:
        return d
    back = dow            # days back to the previous Sunday
    fwd = 7 - dow         # days forward to the next Sunday
    return d - timedelta(back) if back <= fwd else d + timedelta(fwd)


def _when(d: date) -> str:
    """Human-friendly 'Saturday, July 4' — no %-d, for cross-platform safety."""
    return f"{d.strftime('%A, %B')} {d.day}"


# Each entry: (builder(year) -> date, name, kind). kind is "federal" (a U.S.
# federal holiday) or "observance" (widely kept but not a federal holiday).
# isoweekday: Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=7.
USA_HOLIDAYS = [
    (lambda y: date(y, 1, 1),                  "New Year's Day",                        "federal"),
    (lambda y: _nth_weekday(y, 1, 1, 3),       "Martin Luther King Jr. Day",            "federal"),
    (lambda y: date(y, 2, 2),                  "Groundhog Day",                         "observance"),
    (lambda y: date(y, 2, 14),                 "Valentine's Day",                       "observance"),
    (lambda y: _nth_weekday(y, 2, 1, 3),       "Presidents' Day",                       "federal"),
    (lambda y: date(y, 3, 17),                 "St. Patrick's Day",                     "observance"),
    (lambda y: _nth_weekday(y, 5, 7, 2),       "Mother's Day",                          "observance"),
    (lambda y: _last_weekday(y, 5, 1),         "Memorial Day",                          "federal"),
    (lambda y: date(y, 6, 14),                 "Flag Day",                              "observance"),
    (lambda y: date(y, 6, 19),                 "Juneteenth",                            "federal"),
    (lambda y: _nth_weekday(y, 6, 7, 3),       "Father's Day",                          "observance"),
    (lambda y: date(y, 7, 4),                  "Independence Day",                      "federal"),
    (lambda y: _nth_weekday(y, 9, 1, 1),       "Labor Day",                             "federal"),
    (lambda y: _nth_weekday(y, 10, 1, 2),      "Columbus Day / Indigenous Peoples' Day", "federal"),
    (lambda y: date(y, 10, 31),                "Halloween",                             "observance"),
    (lambda y: date(y, 11, 11),                "Veterans Day",                          "federal"),
    (lambda y: _nth_weekday(y, 11, 4, 4),      "Thanksgiving Day",                      "federal"),
    (lambda y: date(y, 12, 25),                "Christmas Day",                         "federal"),
]

HOLIDAYS_BY_COUNTRY = {
    "USA": USA_HOLIDAYS,
}


def civil_holidays_for(d: date, country: str = "USA",
                       include_nearby: bool = True) -> list[dict]:
    """Civil holidays relevant to date `d` for the given country.

    Each entry is a dict::

        {"name", "kind", "country", "relationship", "date", "when"}

    ``relationship`` is ``"on"`` when the holiday falls exactly on ``d``, or
    ``"nearby"`` when ``d`` is the Sunday nearest to a holiday that falls on
    another day. ``date`` is the holiday's own ISO date and ``when`` a
    human-friendly form of it ("Saturday, July 4").

    The "nearby" surfacing only happens when ``d`` is a Sunday and
    ``include_nearby`` is set: a holiday like Independence Day on a Saturday is
    worth flagging on the adjacent Sunday, since that's the day people gather.
    Pass ``include_nearby=False`` (e.g. for iCal feeds) to get only holidays
    that land squarely on ``d``.

    "on" always takes precedence over "nearby" for the same holiday, and the
    list is ordered "on" first, then nearby ones by how close they are.
    """
    holidays = HOLIDAYS_BY_COUNTRY.get(country, [])
    is_sunday = d.isoweekday() == 7

    on, nearby = [], []
    # Scan adjacent years too so December/January Sundays correctly match
    # holidays that sit just across a year boundary.
    for builder, name, kind in holidays:
        for year in (d.year - 1, d.year, d.year + 1):
            hd = builder(year)
            if hd == d:
                on.append({"name": name, "kind": kind, "country": country,
                           "relationship": "on", "date": d.isoformat(),
                           "when": _when(d)})
                break
            if include_nearby and is_sunday and _nearest_sunday(hd) == d:
                nearby.append((abs((hd - d).days),
                               {"name": name, "kind": kind, "country": country,
                                "relationship": "nearby", "date": hd.isoformat(),
                                "when": _when(hd)}))
                break

    nearby.sort(key=lambda t: t[0])
    return on + [entry for _, entry in nearby]
