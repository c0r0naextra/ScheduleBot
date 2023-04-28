from config import host, user, password, db_name, CHANNEL_ID
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, bot
from keyboards.date import calendar, date
from keyboards.reg_keyboards import faculty_kb, year_kb, menu_cd, change_to_schedule_kb, default_kb, channel_sub_btn
from typing import Union
from db.database import create_connection, join_maker, schedule_kb, send_message, week_day_id_maker, group_id_creator, year_id_creator, group_kb, faculty_year_group_returner



global connection
connection = create_connection(host, user, password, db_name)


# def check_subscription(chat_member):
#     print(chat_member)
#     if chat_member['status'] != 'left':
#         return True
#     else: 
#         return False


@dp.message_handler(commands=['start'])
async def menu(message : types.Message):
    # if check_subscription(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
    global week_flag
    week_flag = False
    await faculty_list(message)
    # else:
    #     markup = await channel_sub_btn()
    #     await bot.send_message(message.from_user.id, "Для использования бота необходимо подписаться на канал", reply_markup=markup)


async def faculty_list(message : types.Message, **kwargs):
    markup = await faculty_kb()
    help_keyboard = await default_kb()
    global tg_id
    global first_name
    global username

    tg_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    await bot.send_message(message.from_user.id, "Приветствую!", reply_markup=help_keyboard)
    await bot.send_message(message.from_user.id, "Для начала пройди регистрацию (факультет, курс, группа)", reply_markup=markup)


async def year_list(query: types.CallbackQuery, faculty, **kwargs):
    markup = await year_kb(faculty)
    await query.message.edit_reply_markup(markup)


async def group_list(query: types.CallbackQuery, faculty, year, **kwargs):
    year_id = year_id_creator(faculty, year)
    markup = await group_kb(year_id, faculty, year, connection)
    await query.message.edit_reply_markup(markup)



async def schedule_menu(message : Union[types.Message, types.CallbackQuery], faculty, year, group, **kwargs):
    global group_id
    group_id = group_id_creator(faculty, year, group)
    markup = await change_to_schedule_kb()

    await message.message.edit_text("Готово!")
    await bot.send_message(message.from_user.id, "Меню:", reply_markup=markup)



@dp.callback_query_handler(menu_cd.filter())
async def navigate(query : types.CallbackQuery, callback_data: dict):
    await query.answer()
    current_level = callback_data.get('level')
    faculty = callback_data.get('faculty')
    year = callback_data.get('year')
    group = callback_data.get('group')

    levels = {
        "0": faculty_list,
        "1": year_list,
        "2": group_list,
        "3": schedule_menu
    }

    current_level_function = levels[current_level]
    await current_level_function(query, faculty=faculty, year=year, group=group) 


@dp.message_handler(content_types=['text'])
async def message(message : types.Message):
    markup = await schedule_kb(connection)
    keyboard = await change_to_schedule_kb()
    
    # if check_subscription(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
    help_text = "Это бот для получения расписания. Введите /start, чтобы начать."
    if message.text == 'Помощь':
        await bot.send_message(message.from_user.id, help_text)
    
    global week_flag
    if message.text == 'Текущая неделя':
        await bot.send_message(message.from_user.id, "Выбери день недели:", reply_markup=markup)
    elif message.text == 'Следующая неделя':
        week_flag = True
        await bot.send_message(message.from_user.id, "Выбери день недели:", reply_markup=markup)
    elif message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        schedule_text = send_message(connection, message.text, group_id, week_flag)
        await bot.send_message(message.from_user.id, schedule_text)
    elif message.text == 'Назад':
        week_flag = False
        await bot.send_message(message.from_user.id, 'Меню:', reply_markup=keyboard)
    # else:
    #     markup = await channel_sub_btn()
    #     await bot.send_message(message.from_user.id, "Для использования бота необходимо подписаться на канал", reply_markup=markup)



#




    
        



