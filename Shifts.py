Daysin = [4,4,2,6]
Daysoff = [1,2,3,6]
TDays = 16

#28th may

months = ["Jan","Feb","March","April","May","June",'July','August','September','October','November','December']
days = [   31 ,   28,    31,     30,    31,   30,     31,    31,       30,       31,        30,        31]


class Day():
    def __init__(self, date, inWork):
        #print(current_day, True, month_index )
        self.date = date
        self.inWork = inWork
        
        self.name = f"{self.date} is {self.inWork}"
   
    
days_box = []
month_index = 0
current_day = 7





def tomorrow(working):
    global days_box
    global month_index
    global current_day
    current_day + 1
    if month_index > 11:
        return
    if current_day >= days[month_index]:
        month_index += 1
        current_day =1
    else:
        current_day += 1
        
    new_date = f"{current_day}th of {months[month_index]}"
    return Day(new_date, working)



def shids():
    while month_index <= 11:
        month_box = []
        while(current_day <= days[month_index]):
             for i in range(len(Daysin)):
                 for j in range(Daysin[i]):
                    next_day = tomorrow("at work")
                    month_box.append(next_day)
                 for j in range(Daysoff[i]): 
                    next_day = tomorrow("off")
                    month_box.append(next_day)
        days_box.append(month_box)
    return days_box


    

choose = input("Choose?")
if choose != "":
    print(shids())
else:
    shids()
    chosen_day = int(input("What date ?")) - 1
    chosen_month = int(input("WHat month")) - 1
    
    print(shids()[chosen_months:])

