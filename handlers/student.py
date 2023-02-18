import json
from aiogram import types, Dispatcher
from loader import dp, bot
#from keyboards.main_menu import schedule_buttons, start_menu_kb
from keyboards.date import str_maker, date, f_monday, today
from db.lessons import lesson, lecture, string_f
from keyboards.registration import faculty_kb, year_kb, menu_cd, group_kb, change_to_schedule_kb, schedule_kb
from typing import Union







@dp.message_handler(commands=['start'])
async def menu(message : types.Message):
    await faculty_list(message)
    #markup = await start_menu_kb()
    #await bot.send_message(message.chat.id, "Привет! Я помогу узнать расписание)", reply_markup=markup)

async def faculty_list(message : Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await faculty_kb()
    global user_id
    global first_name
    global username

    user_id = message.from_user.id
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
    
    


    markup = await change_to_schedule_kb(faculty, year, group)
    user_list = [user_id, username, faculty, year, group]

    user_dict = {
        'user_id': f'{user_id}',
        'username': f'{first_name}',
        'faculty': f'{faculty}',
        'year': f'{year}',
        'group': f'{group}',
    }
    print('dict:', user_dict)
   
   
    # json.dump(user_dict, open('users.json', 'w'))


    # with open('users.json') as f:
    #     a = json.load(f)

    # print('json', a) 


    #Внести пользователя в базу данных

    # data = json.loads(lectures)
    # with open("schedule.json", "w") as f:
    # json.dump(data, f, indent=3)

 

    print(type(message))

    await message.message.edit_text("Готово!")
    await bot.send_message(message.from_user.id, "Меню:", reply_markup=markup)

    
    
    




    #print(user_list)


    # user_id = query.message.from_user.id
    # user_name = query.message.from_user.username
    # print(user_id, user_name)

# async def user_data(query: types.CallbackQuery, faculty, year, group, **kwargs):
#     data = await query.data
#     print(data)



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
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    week_days_eng = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    if message.text == 'Посмотреть расписание':
        markup = await schedule_kb()
        await bot.send_message(message.from_user.id, "Привет!", reply_markup=markup)
        for day in week_days:
            if day == message.text:
                await bot.send_message(message.chat.id, string_f(lesson(week_days_eng[week_days.index(day)], lecture(dates[week_days.index(day)]))))

    
    

    # levels = {
    #    "Посмотреть расписание": schedule_buttons,
    #    "Назад": start_menu_kb,
    # }
    # week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    # week_days_eng = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


    # def creating_dates():
    #     dates = []
    #     today_day = today()

    #     for i in range(len(week_days)):                                           #Creating buttons
    #         dates.append(str_maker(date(f_monday(today_day), i, today_day)))
    #     return dates



    # if message.text == "Посмотреть расписание":
    #     text = "Расписание"
    # else:
    #     text = "Назад"

    


    # if message.text == "Посмотреть расписание" or message.text == "Назад":
    #     current_level_function = levels[message.text]
    #     markup = await current_level_function()
    #     await bot.send_message(message.chat.id, text, reply_markup=markup)
    # else:
    #     dates = creating_dates()
    #     for day in week_days:
    #         if day == message.text:
    #             await bot.send_message(message.chat.id, string_f(lesson(week_days_eng[week_days.index(day)], lecture(dates[week_days.index(day)]))))

        
    