#import pymysql
from config import host, user, password, db_name
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from loader import dp, bot
#from keyboards.main_menu import schedule_buttons, start_menu_kb
from keyboards.date import date
#from db.lessons import lesson, lecture, string_f
from keyboards.reg_keyboards import faculty_kb, year_kb, menu_cd, group_kb, change_to_schedule_kb
from db.functions import group_id_creator
from typing import Union
from db.database import check_student, create_connection, execute_read_query, join_maker



global connection
connection = create_connection(host, user, password, db_name)




@dp.message_handler(commands=['start'])
async def menu(message : types.Message):
    await faculty_list(message)
    #markup = await start_menu_kb()
    #await bot.send_message(message.chat.id, "Привет! Я помогу узнать расписание)", reply_markup=markup)



async def faculty_list(message : Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await faculty_kb()
    global tg_id
    global first_name
    global username

    tg_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    if isinstance(message, types.Message):
        await bot.send_message(message.from_user.id, "Привет! Сначала зарегистрируйся!", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):                                 #Получает callback, если нажата кнопка назад
        call = message
        await call.message.edit_reply_markup(reply_markup=markup)




async def year_list(query: types.CallbackQuery, faculty, **kwargs):
    markup = await year_kb(faculty)
    await query.message.edit_reply_markup(markup)


async def group_list(query: types.CallbackQuery, faculty, year, **kwargs):
    markup = await group_kb(faculty, year)
    await query.message.edit_reply_markup(markup)



async def schedule_menu(message : Union[types.Message, types.CallbackQuery], faculty, year, group, **kwargs):

    global group_id
    group_id = group_id_creator(faculty, year, group)
    
    markup = await change_to_schedule_kb(faculty, year, group)

    #group_id = check_student(connection, tg_id, group_id, first_name)


    await message.message.edit_text("Готово!")
    await bot.send_message(message.from_user.id, "Меню:", reply_markup=markup)

    
    
    



    


@dp.callback_query_handler(menu_cd.filter())
async def navigate(query : types.CallbackQuery, callback_data: dict):
    await query.answer()
    current_level = callback_data.get('level')
    faculty = callback_data.get('faculty')
    year = callback_data.get('year')
    group = callback_data.get('group')

    print(current_level, faculty, year, group)


    levels = {
        "0": faculty_list,
        "1": year_list,
        "2": group_list,
        "3": schedule_menu
    }

    current_level_function = levels[current_level]


    await current_level_function(query, faculty=faculty, year=year, group=group) #Функция вызывает нужное меню(через вызов нужной функции)




@dp.message_handler(content_types=['text'])
async def message(message : types.Message):
    schedule_text = ''
####################################################################
    async def schedule_kb():
    
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        
        week_days = []
    
        query = "SELECT week_day_name FROM `calendar`"
        results = execute_read_query(connection, query)
        for result in results:
            week_days.append(result['week_day_name']) 
        
        markup.add(*week_days).insert('Назад')
        
        return markup
#########################################################################
    def week_day_id_maker(day_of_week):
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
######################################################################
    def lecture(lecture_dict, date):
        lecture_dict = eval(row['lesson_name'])
        keys_list = lecture_dict.keys()
        for key in keys_list:
            if date in lecture_dict[key]:
                return key
        else:
            return '-'
        
######################################################################
    markup = await schedule_kb()
    



    if message.text == 'Посмотреть расписание':
        await bot.send_message(message.from_user.id, "Привет!", reply_markup=markup)
    elif message.text in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']:
        week_day_id = week_day_id_maker(message.text)
        current_date = date(week_day_id-1)
        
        rows = join_maker(connection, group_id , week_day_id)
        schedule_text = '📅 '+ message.text + ' ' + current_date  + '\n\n'
        for row in rows:
            if '{' in row['lesson_name']:
                string = row['lesson_time'] + '\n' + 'Лекция' + '\n' + lecture(row['lesson_name'], current_date) + '\n\n'
                schedule_text += string      
                
            else:
                string = row['lesson_time'] + '\n' + row['lesson_name'] + '\n\n'
                schedule_text += string
                
        await bot.send_message(message.from_user.id, schedule_text)

                
                    


                
            





   
        
    
    
    
    
        
    
    
    




    
                


    
    

        
    
    
    



    # week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    # week_days_eng = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    # if message.text == 'Посмотреть расписание':
    #     print('yes')
        # markup = await schedule_kb()
        # await bot.send_message(message.from_user.id, "Привет!", reply_markup=markup)
        # for day in week_days:
        #     if day == message.text:
        #         await bot.send_message(message.chat.id, string_f(lesson(week_days_eng[week_days.index(day)], lecture(dates[week_days.index(day)]))))

    
    

    # levels = {
    #    c: schedule_kb,
    #    "Назад": change_to_schedule_kb,
    # }
    # week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    # week_days_eng = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


    



    # if message.text == "Посмотреть расписание":
    #     text = "Расписание"
    # else:
    #     text = "Назад"

    


    # if message.text == "Посмотреть расписание" or message.text == "Назад":
    #     current_level_function = levels[message.text]
    #     markup = await current_level_function(faculty, year, group)
    #     await bot.send_message(message.chat.id, text, reply_markup=markup)
    # else:
    #     dates = creating_dates()
    #     for day in week_days:
    #         if day == message.text:
    #             await bot.send_message(message.chat.id, string_f(lesson(week_days_eng[week_days.index(day)], lecture(dates[week_days.index(day)]))))

        
    