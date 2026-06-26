"""The Almanac — calendar and lunar utilities (Roadmap F).

Pure-Python, dependency-free computational tools that bring back the
calculations from the user's 1997 Calendar Explorer:

  - moon      : astronomical Moon phases (Meeus), full/new/quarter moons,
                blue moons and other rarities.
  - computus  : date of Easter, Western (Gregorian) and Eastern (Orthodox).
  - convert   : Julian <-> Gregorian calendar and Julian Day Number.

Everything here is offline and deterministic so it can be unit-tested and
cross-checked against authoritative sources (USNO for the Moon, known Easter
tables for the computus), per the project's data-verification rule.
"""
