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


def civil_holidays_for(d: date, country: str = "USA") -> list[dict]:
    """Civil holidays falling on date `d` for the given country.

    Returns a list of {"name", "kind", "country"} dicts (usually 0 or 1).
    """
    out = []
    for builder, name, kind in HOLIDAYS_BY_COUNTRY.get(country, []):
        if builder(d.year) == d:
            out.append({"name": name, "kind": kind, "country": country})
    return out
