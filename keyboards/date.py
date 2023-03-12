import datetime


def date(week_day_id, week_flag):
    today = datetime.datetime.now()
    current = datetime.datetime.weekday(today)
    monday = today - datetime.timedelta(days=current)
    day = monday + datetime.timedelta(days=week_day_id-1)
    if week_flag == True:                            
        day = day + datetime.timedelta(days=7)
    day = [day.day, day.month]
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
    
    

    

def calendar(date):
    day = ''
    i = 0
    for number in date:
       day += number
       i += 1
       if i == 2:
           break
    day = int(day)
    
    month = ''
    for i in range(3,5):
        month += date[i]
    
    month = int(month) - 1
    months_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    for i in range(len(months_list)):
        if month == i:
            month = str(month)
            month = months_list[i]
            break

    date_str = ', ' + str(day) + ' ' + month
    return date_str
    

     


        





