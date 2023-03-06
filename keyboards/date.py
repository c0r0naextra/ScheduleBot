import datetime


def date(day_of_week):
    today = datetime.datetime.now()
    current = datetime.datetime.weekday(today)
    #delta = datetime.timedelta(days=current)
    monday = today - datetime.timedelta(days=current)
    day = monday + datetime.timedelta(days=day_of_week)
    if day < today:                            
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
    
    

    

# def str_maker(date):                                    #Recieves a list containing day and month
#     day = [date.day, date.month]
#     interval = 0
#     result = ''
#     for i in range(2):
#         if day[i] < 10:
#             interval = '0' + str(day[i])
#         else:
#             interval = str(day[i])
#         if i == 1:
#             result = str(result) + '.' + interval
#         else:
#             result = str(result) + interval
#     return result



