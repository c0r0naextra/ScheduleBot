from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram import types
#from keyboards.main_menu import schedule_buttons, start_menu_kb



menu_cd = CallbackData('show_menu', 'level', 'faculty', 'year', 'group')

def make_cd(level, faculty='0', year='0', group='0'):
    return menu_cd.new(level=level, faculty=faculty, year=year, group=group)



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
        years = 3
    elif faculty == 'Стоматологический' or faculty == 'Фармацевтический':
        years = 5
    else:
        years = 6

    for i in range(1, years+1):
        button_text = i
        callback_data = make_cd(level=LEVEL + 1, faculty=faculty, year=button_text)
        markup.add(InlineKeyboardMarkup(text=button_text, callback_data=callback_data))

    markup.row(InlineKeyboardButton(text='Назад', callback_data=make_cd(level=LEVEL - 1)))

    return markup


async def group_kb(faculty, year):
    LEVEL = 2
    markup = InlineKeyboardMarkup()

    groups = 34

    for group in range(groups):
        button_text = group
        callback_data = make_cd(level=LEVEL+1, faculty=faculty, year=year, group=button_text)
        markup.insert(InlineKeyboardMarkup(text=button_text, callback_data=callback_data))

    markup.row(InlineKeyboardButton(text='Назад', callback_data=make_cd(level=LEVEL - 1)))

    return markup



async def change_to_schedule_kb(faculty, year, group):        #when registration is over
    LEVEL = 3

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    check_button = KeyboardButton('Посмотреть расписание')
    markup.add(check_button)

    #markup.row(InlineKeyboardButton(text='Назад', callback_data=make_cd(level=LEVEL - 1)))

    return markup




async def schedule_kb():
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    
    markup.add(*week_days).insert('Назад')
    
    return markup
