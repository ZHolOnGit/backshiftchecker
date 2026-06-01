from enum import Enum
from datetime import date, datetime, timedelta
from itertools import cycle

Daysin = [4,4,2,6]
Daysoff = [1,2,3,6]
TDays = 16

#rota = ["D", "D", "B", "B", "O", "D", "D", "D", "B", "O", "O", "B", "B", "O", "O", "O", "D", "D", "D", "D", "B", "B", "O", "O", "O", "O", "O", "O"] 

#28th may
#Calculates backshifts and regular days
#Starts from the current day
#Has the day of the week attached (doomsday?)
#on a flask app in a s3 bucket (lol)

#D = days (7-5)
#B = Backshift (10-8)
#O = Off work

months = ["Jan","Feb","March","April","May","June",'July','August','September','October','November','December']
days = [   31 ,   28,    31,     30,    31,   30,     31,    31,       30,       31,        30,        31 ]

class ShiftType(Enum):
    DAYS = 1
    BACKSHIFT = 2
    OFF = 3

rota = [
    ShiftType.DAYS, ShiftType.DAYS, ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF,
    ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS, ShiftType.BACKSHIFT, ShiftType.OFF,
    ShiftType.OFF, ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF, ShiftType.OFF,
    ShiftType.OFF, ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS, ShiftType.DAYS,
    ShiftType.BACKSHIFT, ShiftType.BACKSHIFT, ShiftType.OFF, ShiftType.OFF,
    ShiftType.OFF, ShiftType.OFF, ShiftType.OFF, ShiftType.OFF
]


class Day():
    def __init__(self, date, inWork, weekDay):
        #print(current_day, True, month_index )
        self.date = date
        self.inWork = inWork
        self.weekDay = weekDay
        
        self.name = f"{self.date} is {self.inWork}"
        
    def __str__(self):
        #Have the start of the string calculated with proper date formatting (th nd, st etc)
        nice_date = format_custom_date(self.date)
        if self.inWork == ShiftType.DAYS:
            return f"{nice_date} is a DAY IN (7-5)"
        elif self.inWork == ShiftType.BACKSHIFT:
            return f"{nice_date} is a BACKSHIFT (boo) (10-8)"
        else:
            return f"{nice_date} is a DAY OFF"

def format_custom_date(d):
    # 1. Determine the ordinal suffix for the day
    if 11 <= d.day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(d.day % 10, "th")

    # 2. Build the string using strftime for weekday (%A) and month (%B)
    return d.strftime(f"%A the {d.day}{suffix} of %B")

#The start of the cycle
month_index = 0
current_day = 7


def shids():
    days_box = []
    current_day = date(2026,1,7)
    for item in cycle(rota):
        days_box.append(Day(current_day, item, current_day.strftime("%A")))
        current_day = current_day + timedelta(days=1)
        if current_day.year == 2027:
            break
    return days_box

def next_month():
    days_box = shids()
    for i in range(len(days_box)):
        if days_box[i].date == date.today():
            return days_box[i:i+30]

def next_days_off():
    days_off = []
    for day in next_month():
        if day.inWork == ShiftType.OFF:
            days_off.append(day)
    return days_off

for day in next_days_off():
    print(day)

























    
