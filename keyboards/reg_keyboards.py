from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from aiogram.utils.callback_data import CallbackData



menu_cd = CallbackData('show_menu', 'level', 'faculty', 'year', 'group')

def make_cd(level, faculty='0', year='0', group='0'):
    return menu_cd.new(level=level, faculty=faculty, year=year, group=group)


# async def channel_sub_btn():
#     markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[InlineKeyboardButton(text='Ссылка на канал', url='https://t.me/+JuOvXXesnpw2NDZi')]])
#     return markup

async def default_kb():
    help_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Помощь')
    help_keyboard.add(button)
    return help_keyboard


async def faculty_kb():
    LEVEL = 0
    faculties = ['Лечебный', 'Медико-профилактический', 'Педиатрический', 'Стоматологический', 'Фармацевтический', 'Medical']
    markup = InlineKeyboardMarkup()


    for i in range(len(faculties)):
        button_text = faculties[i]
        callback_data = make_cd(level= LEVEL + 1, faculty=button_text)
        markup.add(InlineKeyboardMarkup(text=button_text, callback_data=callback_data))
    return markup



async def year_kb(faculty):
    LEVEL = 1
    
    markup = InlineKeyboardMarkup()
    
    if faculty == 'Medical':
        years = 5
    elif faculty == 'Стоматологический' or faculty == 'Фармацевтический':
        years = 5
    else:
        years = 6

    for i in range(1, years+1):
        button_text = i
        callback_data = make_cd(level=LEVEL + 1, faculty=faculty, year=button_text)
        markup.add(InlineKeyboardMarkup(text=button_text, callback_data=callback_data))
    return markup



async def change_to_schedule_kb():        
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Текущая неделя', 'Следующая неделя')
    return markup




