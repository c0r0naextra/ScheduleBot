import datetime

def today():
    today = datetime.datetime.now()
    return today



def f_monday(today):
    current = datetime.datetime.weekday(today)
    delta = datetime.timedelta(days=current)
    monday = today - delta
    return monday


def date(monday, day_of_week, today):                                 #returns date of day of week
    delta = datetime.timedelta(days=day_of_week)
    day = monday + delta
    if day < today:                                                   #if the day is over, it will be changed by the next week one
        day = day + datetime.timedelta(days=7)
    return day

def str_maker(date):                                    #Recieves a list containing day and month
    day = [date.day, date.month]
    interval = 0
    result = ''
    for i in range(2):
        if day[i] < 10:
            interval = '0' + str(day[i])
        else:
            interval = str(day[i])
        if i == 1:
            result = str(result) + '.' + interval
        else:
            result = str(result) + interval
    return result



def calendar():
    pass