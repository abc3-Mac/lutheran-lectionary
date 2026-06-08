from datetime import datetime, timedelta

def get_closest_sunday(date):
    days_to_sunday = (date.weekday() + 1) % 7
    return date - timedelta(days=days_to_sunday)

def days_between(date1, date2):
    return (date1 - date2).days

# Current date
today = datetime.now()
# For testing: today = datetime.strptime("2025-05-27 16:21:00", "%Y-%m-%d %H:%M:%S")

# Calculate liturgical year (Series A, B, or C)
year = today.year
advent_year = year - 1 if today.month < 12 else year
series_num = (advent_year - 1969) % 3
series = "A" if series_num == 0 else "B" if series_num == 1 else "C"

# Key dates for Series B (2024–2025)
advent_2024 = datetime(2024, 12, 1)
christmas_2024 = datetime(2024, 12, 25)
epiphany_2025 = datetime(2025, 1, 6)
lent_2025 = datetime(2025, 2, 12)
easter_2025 = datetime(2025, 3, 30)
pentecost_2025 = datetime(2025, 5, 18)
trinity_2025 = datetime(2025, 5, 25)
last_pentecost_2025 = datetime(2025, 11, 23)
advent_2025 = datetime(2025, 11, 30)

if today < advent_2024 or today >= advent_2025:
    print("Outside Series B (2024–2025). Check liturgical calendar.")
else:
    closest_sunday = get_closest_sunday(today)
    
    if advent_2024 <= today < christmas_2024:
        weeks_since_advent = days_between(closest_sunday, advent_2024) // 7
        advent_weeks = ["First Sunday in Advent", "Second Sunday in Advent", "Third Sunday in Advent", "Fourth Sunday in Advent"]
        if 0 <= weeks_since_advent < 4:
            print(f"{advent_weeks[weeks_since_advent]} (Series B)")
        else:
            print("Advent Season (Series B)")
    elif christmas_2024 <= today < epiphany_2025:
        christmas1 = datetime(2024, 12, 29)
        if closest_sunday.date() == christmas1.date():
            print("First Sunday after Christmas (Series B)")
        else:
            print("Christmas Season (Series B)")
    elif epiphany_2025 <= today < lent_2025:
        epiphany_sunday = datetime(2025, 1, 5)
        weeks_since_epiphany = days_between(closest_sunday, epiphany_sunday) // 7
        if weeks_since_epiphany == 0:
            print("First Sunday after Epiphany (Series B)")
        elif 0 < weeks_since_epiphany <= 5:
            print(f"Sunday after Epiphany {weeks_since_epiphany} (Series B)")
        else:
            print("Epiphany Season (Series B)")
    elif lent_2025 <= today < easter_2025:
        lent1 = datetime(2025, 2, 16)
        weeks_since_lent1 = days_between(closest_sunday, lent1) // 7
        lent_weeks = ["First Sunday in Lent", "Second Sunday in Lent", "Third Sunday in Lent", "Fourth Sunday in Lent", "Fifth Sunday in Lent"]
        if 0 <= weeks_since_lent1 < 5:
            print(f"{lent_weeks[weeks_since_lent1]} (Series B)")
        elif closest_sunday.date() == datetime(2025, 3, 23).date():
            print("Palm Sunday (Series B)")
        else:
            print("Lent Season (Series B)")
    elif easter_2025 <= today < pentecost_2025:
        weeks_since_easter = days_between(closest_sunday, easter_2025) // 7
        if weeks_since_easter == 0:
            print("Easter Sunday (Series B)")
        elif 0 < weeks_since_easter <= 6:
            print(f"Sunday after Easter {weeks_since_easter} (Series B)")
        else:
            print("Easter Season (Series B)")
    elif pentecost_2025 <= today <= last_pentecost_2025:
        weeks_since_pentecost = days_between(closest_sunday, pentecost_2025) // 7
        if weeks_since_pentecost == 0:
            print("Pentecost (Series B)")
        elif closest_sunday.date() == trinity_2025.date():
            print("Trinity Sunday (Series B)")
        elif 0 < weeks_since_pentecost <= 27:
            proper_number = weeks_since_pentecost + 3
            if closest_sunday.date() == last_pentecost_2025.date():
                print("Last Sunday after Pentecost (Series B)")
            else:
                print(f"Proper {proper_number} (Sunday after Pentecost, Series B)")
        else:
            print("Time after Pentecost (Series B)")
    else:
        print("Unknown liturgical week. Consult Lutheran Service Book.")


