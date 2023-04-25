import logging
from config import host, user, password, db_name, CHANNEL_ID, WEBHOOK_URL
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from loader import dp, bot
from keyboards.reg_keyboards import faculty_kb, year_kb, menu_cd, change_to_schedule_kb, default_kb
from typing import Union
from db.database import create_connection, schedule_kb, send_message, group_id_creator, year_id_creator, group_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


global connection
connection = create_connection(host, user, password, db_name)


#Define states for the conversation
class SubscribeState(StatesGroup):
    waiting_for_subscription = State()


@dp.message_handler(commands=['start'])
async def menu(message : types.Message):
    global week_flag
    week_flag = False
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    if chat_member.status == "member" or chat_member.status == "creator":
        await faculty_list(message)
        return True
        # Allow the user to use the bot
        # ...
    else:
        # Ask the user to join the channel
        markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='Ссылка на канал', url='https://t.me/+JuOvXXesnpw2NDZi')]
            ])
        await message.reply("Для использования бота необходимо подписаться на канал", reply_markup=markup)
        # Set the custom state
        await SubscribeState.waiting_for_subscription.set()
        

@dp.callback_query_handler(state=SubscribeState.waiting_for_subscription)
async def process_subscribe_callback(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.from_user.id
    # Check if user has joined the channel
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=chat_id)
    if chat_member.status == "member" or chat_member.status == "creator":
        await bot.answer_callback_query(callback_query.id, text="Thank you for subscribing!")
        await state.finish()
        # Allow the user to use the bot
        # ...
    else:
        await bot.answer_callback_query(callback_query.id, text="Please subscribe to the channel first!")




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

    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)
    if chat_member.status == "member" or chat_member.status == "creator":
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
        return True
        # Allow the user to use the bot
        # ...
    else:
        # Ask the user to join the channel
        markup = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [InlineKeyboardButton(text='Ссылка на канал', url='https://t.me/+JuOvXXesnpw2NDZi')]
            ])
        await message.reply("Please subscribe to the channel first!", reply_markup=markup)
        # Set the custom state
        await SubscribeState.waiting_for_subscription.set()


        
    
# async def on_startup(dp):
#     await bot.set_webhook(WEBHOOK_URL)

# async def on_shutdown(dp):
#     await bot.delete_webhook()
#     connection.close()



   
        
    
    
    
    
        
    
    
    




    
                


    
    

        
    
    
    



    
    