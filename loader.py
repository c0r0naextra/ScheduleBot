from aiogram import Bot, Dispatcher, executor
from config import TOKEN
import os
#from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv())

#bot = Bot(os.getenv('TOKEN'))
bot = Bot(TOKEN)
dp = Dispatcher(bot)