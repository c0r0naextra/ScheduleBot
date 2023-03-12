from keyboards.date import calendar, date
import pymysql
from config import host, user, password, db_name
from aiogram.types import ReplyKeyboardMarkup
from db.functions import group_id_creator
from aiogram import types
import json



def create_connection(host, user, password, db_name):
    try:
        connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )    
        print('Connected successfully...')
        print('#' * 20)
    
    except Exception as ex:
        print("Connection refused")
        print(ex)
    return connection




def join_maker(connection, group_id, day_id):
    with connection.cursor() as cursor:   
        query = '''
        SELECT 
        lesson.lesson_time, 
        lesson.lesson_name, 
        calendar.week_day_name, 
        student_group.group_name 
        FROM 
        timetable
        INNER JOIN student_group on timetable.group_id = student_group.id
        INNER JOIN calendar on timetable.week_day_id = calendar.week_day
        INNER JOIN lesson on timetable.lesson_id = lesson.id
        WHERE student_group.id = (%s) and calendar.week_day = (%s)'''
    
        cursor.execute(query, (group_id, day_id))
        rows = cursor.fetchall()
    return rows

def group_id_creator(faculty, year, group):
        faculty_list = ['Лечебный', 'Медико-профилактический', 'Педиатрический', 'Стоматологический', 'Фармацевтический', 'Medical']
        if int(group) >= 1 and int(group) <= 9:
            group = '0' + group
        
        for i in range(len(faculty_list)):
            if faculty == faculty_list[i]:
                faculty_number = i + 1
    
        group_id = str(faculty_number) + year + group
        group_id = int(group_id)

        return group_id

    
    


def execute_read_query(connection, query):
     cursor = connection.cursor()

     with connection.cursor() as cursor:
         cursor.execute(query)
         result = cursor.fetchall()
     return result


def faculty_year_group_returner(faculty, year, group):
    list = [faculty, year, group]
    return list


async def schedule_kb(connection):
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    week_days = []
    
    query = "SELECT week_day_name FROM `calendar`"
    results = execute_read_query(connection, query)
    for result in results:
        week_days.append(result['week_day_name']) 
    
    markup.add(*week_days).insert('Назад')
    
    return markup



def week_day_id_maker(connection, day_of_week):
    week_days = []
    query = "SELECT week_day_name FROM `calendar`"
    results = execute_read_query(connection, query)
    for result in results:
        week_days.append(result['week_day_name'])
    i=0 
    for week_day in week_days:
        i+= 1
        if week_day == day_of_week:
            return i
        

def lecture(lecture_dict, date, row):
    lecture_dict = eval(row['lesson_name'])
    lesson_list = []
    for lesson_name, dates_list in lecture_dict.items():
        if date in dates_list:
            lesson_list.append(lesson_name)
    return lesson_list or ['-']
        


def send_message(connection, day_of_week, group_id, week_flag):
        
        week_day_id = week_day_id_maker(connection, day_of_week)
        current_date = date(week_day_id, week_flag)
            
        rows = join_maker(connection, group_id, week_day_id)
        schedule_text = '📆 '+ day_of_week + calendar(current_date)  + '\n\n'
        for row in rows:
            if '{' in row['lesson_name']:
                lecture_names = lecture(row['lesson_name'], current_date, row)
                if not lecture_names:
                    continue
                for lecture_name in lecture_names:    
                    string = row['lesson_time'] + '\n' + 'Л' + '\n' + lecture_name + '\n\n'
                    schedule_text += string
                    if len(lecture_names) == 2:
                        lecture_names = lecture_names.pop(0)
                    else:
                        break
                    continue    
            else:
                string = row['lesson_time'] + '\n' + row['lesson_name'] + '\n\n'
                schedule_text += string
        if schedule_text == '📆 '+ day_of_week + calendar(current_date)  + '\n\n': 
            schedule_text += 'Ваше расписание ещё не загружено!'
        return schedule_text

        






         
                
                
    