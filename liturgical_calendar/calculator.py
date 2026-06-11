"""
Core liturgical calendar date engine for LCMS (Lutheran Church—Missouri Synod)
following the Lutheran Service Book (LSB) lectionary.
"""

from datetime import date, timedelta
import re as _re


# ---------------------------------------------------------------------------
# Easter algorithm (Anonymous Gregorian)
# ---------------------------------------------------------------------------

def calc_easter(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return date(year, month, day)


def _first_sunday_on_or_after(d: date) -> date:
    dow = d.isoweekday()  # 1=Mon … 7=Sun
    if dow == 7:
        return d
    return d + timedelta(7 - dow)


def advent1_for_year(advent_year: int) -> date:
    """First Sunday of Advent for the church year that BEGINS in advent_year."""
    return _first_sunday_on_or_after(date(advent_year, 11, 27))


def get_series(advent_year: int) -> str:
    """Return 'A', 'B', or 'C' for the three-year lectionary series."""
    # Verified: 2025→A, 2026→B, 2027→C, 2028→A …
    return ["A", "B", "C"][advent_year % 3]


def daily_readings(d: date) -> dict | None:
    """
    LSB Daily Lectionary readings (OT + NT) for any date.

    Fixed civil dates cover Nov 27–Mar 9 and May 18–Nov 26; the window from
    Ash Wednesday through Holy Trinity is keyed to the movable Easter cycle
    and takes precedence over fixed dates (per LSB rubric).
    """
    from liturgical_calendar.data.daily_lectionary import DAILY_FIXED, DAILY_MOVABLE
    easter = calc_easter(d.year)
    ash_wed = easter - timedelta(46)
    trinity = easter + timedelta(56)
    if ash_wed <= d <= trinity:
        return dict(DAILY_MOVABLE[(d - ash_wed).days])
    entry = DAILY_FIXED.get(f"{d.month:02d}-{d.day:02d}")
    return dict(entry) if entry else None


def get_proper(sunday: date) -> int:
    """
    Return the Proper number (3–29) for a Sunday in Ordinary Time.
    Proper 3 = Sunday closest to May 25; each subsequent proper is 7 days later.
    """
    year = sunday.year
    base = date(year, 5, 25)  # Proper 3 anchor
    delta = (sunday - base).days
    return max(3, min(29, 3 + round(delta / 7)))


# ---------------------------------------------------------------------------
# Main calendar class
# ---------------------------------------------------------------------------

class LiturgicalCalendar:
    """
    Computes all liturgically significant dates for a single church year.

    Parameters
    ----------
    advent_year : int
        The civil year in which Advent *begins* (e.g. 2025 for the 2025-2026
        church year).  Valid range: 1583–2299.
    """

    MIN_ADVENT_YEAR = 1583
    MAX_ADVENT_YEAR = 2299

    def __init__(self, advent_year: int):
        if not (self.MIN_ADVENT_YEAR <= advent_year <= self.MAX_ADVENT_YEAR):
            raise ValueError(
                f"advent_year must be {self.MIN_ADVENT_YEAR}–{self.MAX_ADVENT_YEAR}"
            )
        self.advent_year = advent_year
        self.civil_year = advent_year + 1
        self.series = get_series(advent_year)
        self._build()

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _build(self):
        y = self.advent_year
        cy = self.civil_year

        # --- Advent ---
        self.advent_1 = advent1_for_year(y)
        self.advent_2 = self.advent_1 + timedelta(7)
        self.advent_3 = self.advent_1 + timedelta(14)
        self.advent_4 = self.advent_1 + timedelta(21)

        # --- Christmas & New Year ---
        self.christmas     = date(y, 12, 25)
        self.holy_innocents = date(y, 12, 28)
        self.new_years_eve  = date(y, 12, 31)
        self.new_years_day  = date(cy, 1, 1)

        # Sundays between Christmas and Epiphany
        self._christmas_sundays = [
            d for d in _daterange(self.christmas + timedelta(1), date(cy, 1, 6))
            if d.isoweekday() == 7
        ]

        # --- Epiphany ---
        self.epiphany = date(cy, 1, 6)
        # Baptism of Our Lord = first Sunday AFTER Jan 6
        self.baptism_of_lord = _first_sunday_on_or_after(date(cy, 1, 7))

        # --- Easter & dependent dates ---
        self.easter = calc_easter(cy)
        self.ash_wednesday   = self.easter - timedelta(46)
        # Transfiguration (Three-Year) = Sunday immediately before Ash Wednesday
        # Ash Wed is always Wednesday; 3 days back = Sunday ✓
        self.transfiguration = self.ash_wednesday - timedelta(3)

        # --- Pre-Lent (One-Year series only) ---
        self.septuagesima  = self.easter - timedelta(63)
        self.sexagesima    = self.easter - timedelta(56)
        self.quinquagesima = self.easter - timedelta(49)

        # Transfiguration (One-Year) = Sunday before Septuagesima = Easter - 70 days
        self.transfiguration_1yr = self.septuagesima - timedelta(7)

        # Sundays after Epiphany:
        #   Three-Year: 2nd … last before Transfiguration (Sunday before Ash Wed)
        #   One-Year:   2nd … last before one-year Transfiguration (Sunday before Septuagesima)
        self._epiphany_sundays = list(
            _sunday_range(self.baptism_of_lord + timedelta(7), self.transfiguration)
        )
        self._epiphany_sundays_1yr = list(
            _sunday_range(self.baptism_of_lord + timedelta(7), self.transfiguration_1yr)
        )

        # --- Lent ---
        self.lent_1      = self.ash_wednesday + timedelta(4)   # first Sunday in Lent
        self.lent_2      = self.lent_1 + timedelta(7)
        self.lent_3      = self.lent_1 + timedelta(14)
        self.lent_4      = self.lent_1 + timedelta(21)
        self.lent_5      = self.lent_1 + timedelta(28)
        self.palm_sunday = self.easter - timedelta(7)
        self.maundy_thursday = self.easter - timedelta(3)
        self.good_friday     = self.easter - timedelta(2)

        # --- Easter Season ---
        self.easter_2    = self.easter + timedelta(7)
        self.easter_3    = self.easter + timedelta(14)
        self.easter_4    = self.easter + timedelta(21)
        self.easter_5    = self.easter + timedelta(28)
        self.easter_6    = self.easter + timedelta(35)
        self.ascension   = self.easter + timedelta(39)  # always Thursday
        self.easter_7    = self.easter + timedelta(42)
        self.pentecost   = self.easter + timedelta(49)

        # --- Season after Pentecost ---
        self.holy_trinity = self.pentecost + timedelta(7)
        self.next_advent_1 = advent1_for_year(cy)
        self.last_sunday   = self.next_advent_1 - timedelta(7)

        # Sundays after Pentecost (from 2nd Sunday after Pentecost onward)
        self._pentecost_sundays = list(
            _sunday_range(self.holy_trinity + timedelta(7), self.last_sunday)
        )

        # --- Fixed observances (date; actual observed Sunday may vary) ---
        self.reformation_day = date(cy, 10, 31)
        self.all_saints_day  = date(cy, 11, 1)
        self.thanksgiving    = _nth_thursday(cy, 11, 4)

        # Observed Sundays for moveable observances
        self.reformation_observed = _nearest_sunday(self.reformation_day)
        self.all_saints_observed  = _nearest_sunday(self.all_saints_day)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def date_to_slot(self, d: date, lectionary: str = 'three_year') -> str | None:
        """
        Given a date, return the liturgical slot key (e.g. 'advent_1',
        'proper_15', 'easter') or None if the date is outside this church year.

        lectionary: 'three_year' (default) or 'one_year'
        """
        if d < self.advent_1 or d >= self.next_advent_1:
            return None

        # Check fixed-date feasts first
        if d == self.christmas:         return "christmas_day"
        if d == self.holy_innocents:    return "holy_innocents"
        if d == self.new_years_eve:     return "new_years_eve"
        if d == self.new_years_day:     return "new_years_day"
        if d == self.epiphany:          return "epiphany"
        if d == self.ash_wednesday:     return "ash_wednesday"
        if d == self.maundy_thursday:   return "maundy_thursday"
        if d == self.good_friday:       return "good_friday"
        if d == self.ascension:         return "ascension"

        # Sundays
        if d.isoweekday() != 7:
            return None   # non-Sunday, non-feast: no slot

        if d == self.advent_1:          return "advent_1"
        if d == self.advent_2:          return "advent_2"
        if d == self.advent_3:          return "advent_3"
        if d == self.advent_4:          return "advent_4"

        if d in self._christmas_sundays:
            idx = self._christmas_sundays.index(d)
            return f"christmas_sunday_{idx + 1}"

        if d == self.baptism_of_lord:   return "baptism_of_lord"

        if lectionary == 'one_year':
            if d in self._epiphany_sundays_1yr:
                n = self._epiphany_sundays_1yr.index(d) + 2
                return f"epiphany_{n}"
            if d == self.transfiguration_1yr:  return "transfiguration"
            if d == self.septuagesima:         return "septuagesima"
            if d == self.sexagesima:           return "sexagesima"
            if d == self.quinquagesima:        return "quinquagesima"
        else:
            if d in self._epiphany_sundays:
                n = self._epiphany_sundays.index(d) + 2  # 2nd, 3rd, …
                return f"epiphany_{n}"
            if d == self.transfiguration:      return "transfiguration"

        if d == self.lent_1:            return "lent_1"
        if d == self.lent_2:            return "lent_2"
        if d == self.lent_3:            return "lent_3"
        if d == self.lent_4:            return "lent_4"
        if d == self.lent_5:            return "lent_5"
        if d == self.palm_sunday:       return "palm_sunday"
        if d == self.easter:            return "easter"
        if d == self.easter_2:          return "easter_2"
        if d == self.easter_3:          return "easter_3"
        if d == self.easter_4:          return "easter_4"
        if d == self.easter_5:          return "easter_5"
        if d == self.easter_6:          return "easter_6"
        if d == self.easter_7:          return "easter_7"
        if d == self.pentecost:         return "pentecost"
        if d == self.holy_trinity:      return "holy_trinity"
        if d == self.last_sunday:       return "last_sunday"

        # Reformation / All Saints (check observed Sunday)
        if d == self.reformation_observed:  return "reformation"
        if d == self.all_saints_observed:   return "all_saints"

        # St. Michael and All Angels (Sept 29 → observed Sunday)
        michael = _nearest_sunday(date(self.civil_year, 9, 29))
        if d == michael:                return "st_michael"

        # Thanksgiving (observed on the Thursday itself; no Sunday slot)
        # — handled separately in calendar output

        # Season after Pentecost
        if d in self._pentecost_sundays:
            if lectionary == 'one_year':
                n = (d - self.holy_trinity).days // 7
                return f"trinity_{n}"
            p = get_proper(d)
            return f"proper_{p}"

        return None  # unknown / unassigned

    def all_events(self, include_minor: bool = True, lectionary: str = 'three_year') -> list[dict]:
        """
        Return an ordered list of all liturgical events for this church year.

        Each dict has keys:
            date, slot, name, season, color, series, is_sunday, is_feast

        lectionary: 'three_year' (default) or 'one_year'
        """
        events = []

        def add(d: date, slot: str):
            info = slot_info(slot, self.series, d)
            if info is None:
                return
            if not include_minor and info.get("minor"):
                return
            # Merge one-year propers (collect + introit) for shared slots
            collect = info.get("collect")
            introit = info.get("introit")
            if lectionary == 'one_year' and not collect:
                from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS
                propers = ONE_YEAR_PROPERS.get(slot, {})
                collect = propers.get("collect")
                introit = propers.get("introit")
            events.append({
                "date":      d,
                "slot":      slot,
                "name":      info["name"],
                "season":    info["season"],
                "color":     info["color"],
                "series":    self.series,
                "is_sunday": d.isoweekday() == 7,
                "is_feast":  info.get("feast", False),
                "readings":  info.get("readings"),
                "proper":    info.get("proper"),
                "ordinal":   info.get("ordinal"),
                "minor":     info.get("minor", False),
                "collect":   collect,
                "introit":   introit,
            })

        # Walk the calendar in order
        add(self.advent_1, "advent_1")
        add(self.advent_2, "advent_2")
        add(self.advent_3, "advent_3")
        add(self.advent_4, "advent_4")

        # Christmas Eve (Dec 24 evening service)
        add(date(self.advent_year, 12, 24), "christmas_eve")
        add(self.christmas, "christmas_day")
        add(self.holy_innocents, "holy_innocents")

        for i, s in enumerate(self._christmas_sundays):
            add(s, f"christmas_sunday_{i+1}")

        add(self.new_years_eve, "new_years_eve")
        add(self.new_years_day, "new_years_day")
        add(self.epiphany, "epiphany")
        add(self.baptism_of_lord, "baptism_of_lord")

        if lectionary == 'one_year':
            for i, s in enumerate(self._epiphany_sundays_1yr):
                add(s, f"epiphany_{i+2}")
            add(self.transfiguration_1yr, "transfiguration")
            add(self.septuagesima, "septuagesima")
            add(self.sexagesima, "sexagesima")
            add(self.quinquagesima, "quinquagesima")
        else:
            for i, s in enumerate(self._epiphany_sundays):
                add(s, f"epiphany_{i+2}")
            add(self.transfiguration, "transfiguration")

        add(self.ash_wednesday, "ash_wednesday")
        add(self.lent_1, "lent_1")
        add(self.lent_2, "lent_2")
        add(self.lent_3, "lent_3")
        add(self.lent_4, "lent_4")
        add(self.lent_5, "lent_5")
        add(self.palm_sunday, "palm_sunday")
        add(self.maundy_thursday, "maundy_thursday")
        add(self.good_friday, "good_friday")
        add(self.easter, "easter")
        add(self.easter_2, "easter_2")
        add(self.easter_3, "easter_3")
        add(self.easter_4, "easter_4")
        add(self.easter_5, "easter_5")
        add(self.easter_6, "easter_6")
        add(self.ascension, "ascension")
        add(self.easter_7, "easter_7")
        add(self.pentecost, "pentecost")
        add(self.holy_trinity, "holy_trinity")

        # Season after Pentecost
        for s in self._pentecost_sundays:
            n_after = (s - self.holy_trinity).days // 7  # trinity_1 = 1st Sunday after Trinity
            if lectionary == 'one_year':
                slot = f"trinity_{n_after}"
                info = slot_info(slot, self.series, s)
                if info is None:
                    continue
                if not include_minor and info.get("minor"):
                    continue
                computed_name = self._trinity_ordinal_name(s)
                from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS
                _propers = ONE_YEAR_PROPERS.get(slot, {})
                events.append({
                    "date":      s,
                    "slot":      slot,
                    "name":      computed_name,
                    "season":    "Trinity",
                    "color":     info["color"],
                    "series":    self.series,
                    "is_sunday": True,
                    "is_feast":  False,
                    "readings":  info.get("readings"),
                    "ordinal":   n_after,
                    "minor":     False,
                    "collect":   _propers.get("collect"),
                    "introit":   _propers.get("introit"),
                })
            else:
                p = get_proper(s)
                slot = f"proper_{p}"
                info = slot_info(slot, self.series, s)
                if info:
                    info = dict(info)
                    info["ordinal"] = n_after
                if info is None:
                    continue
                if not include_minor and info.get("minor"):
                    continue
                computed_name = self._pentecost_ordinal_name(s)
                events.append({
                    "date":    s,
                    "slot":    slot,
                    "name":    computed_name,
                    "season":  info["season"],
                    "color":   info["color"],
                    "series":  self.series,
                    "is_sunday": True,
                    "is_feast":  False,
                    "readings":  info.get("readings"),
                    "proper":    p,
                    "ordinal":   n_after,
                    "minor":     False,
                })

            # Possibly overlay Reformation / All Saints / St. Michael
            if include_minor:
                if s == self.reformation_observed:
                    r_info = slot_info("reformation", self.series, s)
                    if r_info:
                        events[-1]["alt_name"] = r_info["name"]
                        events[-1]["alt_readings"] = r_info.get("readings")
                if s == self.all_saints_observed:
                    a_info = slot_info("all_saints", self.series, s)
                    if a_info:
                        events[-1]["alt_name"] = a_info["name"]
                        events[-1]["alt_readings"] = a_info.get("readings")

        add(self.last_sunday, "last_sunday")

        # Thanksgiving (Thursday)
        add(self.thanksgiving, "thanksgiving")

        events.sort(key=lambda e: e["date"])
        return events

    def lookup(self, d: date, lectionary: str = 'three_year') -> dict | None:
        """Return liturgical info for any date, or None if outside valid range.

        For Sundays/feasts: returns that day's info directly.
        For weekdays: returns the governing Sunday's info with is_weekday=True,
        plus minor_feast if a sanctoral observance falls on that date.

        lectionary: 'three_year' (default) or 'one_year'
        """
        ay = d.year if d >= advent1_for_year(d.year) else d.year - 1
        if d < date(self.MIN_ADVENT_YEAR, 11, 27) or d > date(self.MAX_ADVENT_YEAR + 1, 11, 26):
            return None
        cal = LiturgicalCalendar(ay) if ay != self.advent_year else self

        # Check for a sanctoral feast on this exact calendar date (by month/day)
        minor_feast_info = _sanctoral_feast_for_date(d.month, d.day)

        slot = cal.date_to_slot(d, lectionary=lectionary)

        if slot is not None:
            info = slot_info(slot, cal.series, d)
            # Compute human-readable ordinal name for season-after-Pentecost Sundays
            if slot.startswith("proper_") and d in cal._pentecost_sundays:
                info = dict(info)
                info["name"] = cal._pentecost_ordinal_name(d)
            elif slot.startswith("trinity_") and d in cal._pentecost_sundays:
                info = dict(info)
                info["name"] = cal._trinity_ordinal_name(d)
                info["season"] = "Trinity"
            # Merge one-year propers (collect + introit) for any slot when using one-year
            if lectionary == 'one_year' and not info.get("collect"):
                from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS
                propers = ONE_YEAR_PROPERS.get(slot, {})
                if propers:
                    info = dict(info)
                    info["collect"] = propers.get("collect")
                    info["introit"] = propers.get("introit")
            # If the slot IS a sanctoral feast, don't double-report it as minor_feast
            if minor_feast_info and minor_feast_info.get("name") == info.get("name"):
                minor_feast_info = None
            return {
                "date":         d,
                "slot":         slot,
                "church_year":  f"{ay}–{ay+1}",
                "series":       cal.series,
                "is_weekday":   False,
                "minor_feast":  minor_feast_info,
                **info,
            }

        # Weekday with no direct slot — find governing Sunday
        governing = None
        for delta in range(1, 8):
            prev = d - timedelta(delta)
            if prev < cal.advent_1:
                break
            prev_slot = cal.date_to_slot(prev, lectionary=lectionary)
            if prev_slot:
                gov_info = slot_info(prev_slot, cal.series, prev)
                if gov_info:
                    governing = {"date": prev, "slot": prev_slot, **gov_info}
                break

        if governing is None:
            return None

        gov_slot = governing["slot"]
        gov_date = governing["date"]
        # Compute human-readable name for season-after-Pentecost Sundays
        if gov_slot.startswith("proper_") and gov_date in cal._pentecost_sundays:
            governing["name"] = cal._pentecost_ordinal_name(gov_date)
        elif gov_slot.startswith("trinity_") and gov_date in cal._pentecost_sundays:
            governing["name"] = cal._trinity_ordinal_name(gov_date)
            governing["season"] = "Trinity"

        return {
            "date":          d,
            "slot":          gov_slot,
            "church_year":   f"{ay}–{ay+1}",
            "series":        cal.series,
            "is_weekday":    True,
            "governing_date": gov_date,
            "minor_feast":   minor_feast_info,
            **{k: v for k, v in governing.items() if k not in ("date", "slot")},
        }

    _PENTECOST_ORDINALS = [
        "", "First", "Second", "Third", "Fourth", "Fifth",
        "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
        "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth",
        "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth",
        "Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth",
        "Twenty-fifth", "Twenty-sixth", "Twenty-seventh",
    ]

    def _pentecost_ordinal_name(self, d: date) -> str:
        n = (d - self.holy_trinity).days // 7 + 1
        ord_word = self._PENTECOST_ORDINALS[n] if n < len(self._PENTECOST_ORDINALS) else str(n)
        return f"{ord_word} Sunday after Pentecost"

    def _trinity_ordinal_name(self, d: date) -> str:
        n = (d - self.holy_trinity).days // 7  # 1st Sunday after Trinity = 7 days after holy_trinity
        ord_word = self._PENTECOST_ORDINALS[n] if n < len(self._PENTECOST_ORDINALS) else str(n)
        return f"{ord_word} Sunday after Trinity"

    def file_label(self, d: date, lectionary: str = 'three_year') -> str:
        """
        Return a filename-safe label:
            2026-06-07 Second Sunday after Pentecost   (three-year)
            2026-06-07 Second Sunday after Trinity     (one-year)
        """
        slot = self.date_to_slot(d, lectionary=lectionary)
        if slot is None:
            return d.strftime("%Y-%m-%d")
        # Compute human-readable name for season-after-Pentecost Sundays
        if slot.startswith("proper_") and d in self._pentecost_sundays:
            name = self._pentecost_ordinal_name(d)
        elif slot.startswith("trinity_") and d in self._pentecost_sundays:
            name = self._trinity_ordinal_name(d)
        else:
            info = slot_info(slot, self.series, d)
            name = info["name"] if info else slot
        from liturgical_calendar.utils import safe_filename
        return safe_filename(f"{d.strftime('%Y-%m-%d')} {name}")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _daterange(start: date, end: date):
    d = start
    while d < end:
        yield d
        d += timedelta(1)


def _sunday_range(start: date, end: date):
    """Yield Sundays from start up to (but not including) end."""
    d = _first_sunday_on_or_after(start)
    while d < end:
        yield d
        d += timedelta(7)


def _nearest_sunday(d: date) -> date:
    """Return the Sunday nearest to date d (ties go forward)."""
    dow = d.isoweekday()  # 1=Mon … 7=Sun
    if dow == 7:
        return d
    back = dow            # days back to previous Sunday
    fwd  = 7 - dow        # days forward to next Sunday
    if back <= fwd:
        return d - timedelta(back)
    return d + timedelta(fwd)


def _nth_thursday(year: int, month: int, n: int) -> date:
    """Return the n-th Thursday of the given month/year."""
    d = date(year, month, 1)
    # isoweekday: Thu=4
    first_thu = d + timedelta((4 - d.isoweekday()) % 7)
    return first_thu + timedelta(7 * (n - 1))


# ---------------------------------------------------------------------------
# Sanctoral feast lookup by calendar date
# ---------------------------------------------------------------------------

_MONTH_ABBR = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
               'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

def _sanctoral_date_map():
    """Build {(month, day): slot_key} from SANCTORAL_SLOTS date_str fields."""
    from liturgical_calendar.data.sanctoral import SANCTORAL_SLOTS
    result = {}
    for key, info in SANCTORAL_SLOTS.items():
        ds = info.get("date_str", "")
        parts = ds.strip().split()
        if len(parts) == 2:
            m = _MONTH_ABBR.get(parts[0])
            try:
                day = int(parts[1])
            except ValueError:
                continue
            if m:
                result[(m, day)] = key
    return result

_SANCTORAL_MAP_CACHE = None

def _sanctoral_feast_for_date(month: int, day: int) -> dict | None:
    """Return sanctoral slot info for a given month/day, or None."""
    global _SANCTORAL_MAP_CACHE
    if _SANCTORAL_MAP_CACHE is None:
        _SANCTORAL_MAP_CACHE = _sanctoral_date_map()
    slot_key = _SANCTORAL_MAP_CACHE.get((month, day))
    if slot_key is None:
        return None
    from liturgical_calendar.data.sanctoral import SANCTORAL_SLOTS
    info = SANCTORAL_SLOTS.get(slot_key)
    if info:
        return {"slot": slot_key, **info}
    return None


# ---------------------------------------------------------------------------
# Slot info dispatcher — imported lazily to avoid circular imports
# ---------------------------------------------------------------------------

def slot_info(slot: str, series: str, d: date) -> dict | None:
    from liturgical_calendar.data.three_year import THREE_YEAR_SLOTS
    from liturgical_calendar.data.one_year   import ONE_YEAR_SLOTS
    from liturgical_calendar.data.sanctoral  import SANCTORAL_SLOTS

    # Sanctoral feasts take priority for specific date-tied keys
    if slot in SANCTORAL_SLOTS:
        return SANCTORAL_SLOTS[slot]

    if slot in THREE_YEAR_SLOTS:
        entry = THREE_YEAR_SLOTS[slot]
        result = {k: v for k, v in entry.items() if k not in ("A", "B", "C")}
        readings = entry.get(series) or entry.get("all")
        result["readings"] = readings
        return result

    if slot in ONE_YEAR_SLOTS:
        from liturgical_calendar.data.one_year_propers import ONE_YEAR_PROPERS
        entry = ONE_YEAR_SLOTS[slot]
        result = {k: v for k, v in entry.items() if k != "readings"}
        result["readings"] = entry.get("readings")
        propers = ONE_YEAR_PROPERS.get(slot, {})
        result["collect"] = propers.get("collect")
        result["introit"] = propers.get("introit")
        return result

    # Trinity Sundays beyond what is pre-keyed — generate dynamically
    if slot.startswith("trinity_"):
        n = int(slot.split("_")[1])
        ordinals = [
            "", "First", "Second", "Third", "Fourth", "Fifth",
            "Sixth", "Seventh", "Eighth", "Ninth", "Tenth",
            "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth",
            "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth",
            "Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth",
            "Twenty-fifth", "Twenty-sixth", "Twenty-seventh",
        ]
        name = f"{ordinals[n]} Sunday after Trinity" if n < len(ordinals) else f"Sunday {n} after Trinity"
        return {
            "name":     name,
            "season":   "Pentecost",
            "color":    "Green",
            "feast":    False,
            "readings": None,
        }

    # Epiphany Sundays beyond what is pre-keyed — generate dynamically
    if slot.startswith("epiphany_"):
        n = int(slot.split("_")[1])
        ordinals = [
            "", "First", "Second", "Third", "Fourth",
            "Fifth", "Sixth", "Seventh", "Eighth",
        ]
        name = f"{ordinals[n]} Sunday after the Epiphany" if n < len(ordinals) else f"Sunday {n} after the Epiphany"
        base_key = slot if slot in THREE_YEAR_SLOTS else f"epiphany_{min(n, 8)}"
        base = THREE_YEAR_SLOTS.get(base_key, {})
        result = {
            "name":   name,
            "season": "Epiphany",
            "color":  "Green",
            "feast":  False,
        }
        readings = base.get(series) or base.get("all")
        result["readings"] = readings
        return result

    # Christmas Sundays
    if slot.startswith("christmas_sunday_"):
        n = int(slot.split("_")[-1])
        names = ["", "First Sunday after Christmas", "Second Sunday after Christmas"]
        base = THREE_YEAR_SLOTS.get(slot, {})
        result = {
            "name":   names[n] if n < len(names) else f"Sunday after Christmas {n}",
            "season": "Christmas",
            "color":  "White",
            "feast":  False,
        }
        readings = base.get(series) or base.get("all")
        result["readings"] = readings
        return result

    return None
