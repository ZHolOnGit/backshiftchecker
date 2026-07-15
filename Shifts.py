from enum import Enum
from datetime import date, timedelta
from itertools import islice, cycle

# Anchor date: the first day of the rota cycle
ANCHOR_DATE = date(2026, 1, 6)

class ShiftType(Enum):
    DAYS = "DAYS"
    BACKSHIFT = "BACKSHIFT"
    OFF = "OFF"

ROTA = [
    ShiftType.DAYS, ShiftType.DAYS, ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF,
    ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS, ShiftType.BACKSHIFT, ShiftType.OFF,
    ShiftType.OFF, ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF, ShiftType.OFF,
    ShiftType.OFF, ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS,
    ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF, ShiftType.OFF,
    ShiftType.OFF, ShiftType.OFF, ShiftType.OFF, ShiftType.OFF
]

ROTA_LENGTH = len(ROTA)  # 28


class Day:
    def __init__(self, date, shift_type, weekday):
        self.date = date
        self.inWork = shift_type
        self.weekDay = weekday

    def __str__(self):
        nice_date = format_custom_date(self.date)
        if self.inWork == ShiftType.DAYS:
            return f"{nice_date} is a DAY IN (7-5)"
        elif self.inWork == ShiftType.BACKSHIFT:
            return f"{nice_date} is a BACKSHIFT (boo) (10-8)"
        else:
            return f"{nice_date} is a DAY OFF"


def format_custom_date(d):
    """Return a human-readable date string e.g. 'Wednesday the 7th of January'."""
    if 11 <= d.day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(d.day % 10, "th")
    return d.strftime(f"%A the {d.day}{suffix} of %B")


def _cycle_from_offset(offset):
    """Return a cycle iterator starting at the correct rota position."""
    shifted = ROTA[offset:] + ROTA[:offset]
    return cycle(shifted)


def shids(years=None):
    """
    Generate Day objects for every calendar day across the given years.

    Args:
        years: list of ints, e.g. [2026, 2027, 2028]. Defaults to [2026, 2027, 2028].

    Returns:
        list of Day objects covering Jan 1 – Dec 31 for each year, in order.
    """
    if years is None:
        years = [2026, 2027, 2028]

    days_box = []
    for year in years:
        start = date(year, 1, 1)
        end = date(year, 12, 31)

        # Calculate which position in the rota Jan 1 of this year falls on
        offset = (start - ANCHOR_DATE).days % ROTA_LENGTH
        rota_iter = _cycle_from_offset(offset)

        current = start
        while current <= end:
            shift = next(rota_iter)
            days_box.append(Day(current, shift, current.strftime("%A")))
            current += timedelta(days=1)

    return days_box


def next_month():
    """Return the next 30 days from today."""
    days_box = shids()
    today = date.today()
    for i, day in enumerate(days_box):
        if day.date == today:
            return days_box[i:i + 30]
    return []


def next_days_off():
    """Return days off within the next 30 days."""
    return [day for day in next_month() if day.inWork == ShiftType.OFF]


if __name__ == "__main__":
    all_days = shids([2026, 2027, 2028])

    # Summary per year
    for year in [2026, 2027, 2028]:
        year_days = [d for d in all_days if d.date.year == year]
        print(f"{year}: {len(year_days)} days  (leap year: {date(year, 12, 31).timetuple().tm_yday == 366})")

    # Verify anchor date
    jan7 = next(d for d in all_days if d.date == date(2026, 1, 7))
    print(f"\nAnchor check — {jan7}")

    # Show first and last day of each year
    for year in [2026, 2027, 2028]:
        year_days = [d for d in all_days if d.date.year == year]
        print(f"\n{year} first: {year_days[0]}")
        print(f"{year} last:  {year_days[-1]}")

    # Verify continuity across year boundary (Dec 31 2026 → Jan 1 2027)
    dec31 = next(d for d in all_days if d.date == date(2026, 12, 31))
    jan1  = next(d for d in all_days if d.date == date(2027, 1, 1))
    dec31_idx = (date(2026, 12, 31) - ANCHOR_DATE).days % ROTA_LENGTH
    jan1_idx  = (date(2027, 1, 1)  - ANCHOR_DATE).days % ROTA_LENGTH
    print(f"\nContinuity check:")
    print(f"  Dec 31 2026 rota pos {dec31_idx}: {dec31}")
    print(f"  Jan 01 2027 rota pos {jan1_idx}: {jan1}")
    assert (dec31_idx + 1) % ROTA_LENGTH == jan1_idx, "Cycle continuity broken!"
    print("  Continuity OK")

    # Verify leap day exists in 2028
    leap_day = next((d for d in all_days if d.date == date(2028, 2, 29)), None)
    assert leap_day is not None, "Leap day missing!"
    print(f"\nLeap day check — {leap_day}  OK")

    # Verify 2028 has 366 days
    days_2028 = [d for d in all_days if d.date.year == 2028]
    assert len(days_2028) == 366, f"Expected 366 days in 2028, got {len(days_2028)}"
    print("2028 day count: 366  OK")
