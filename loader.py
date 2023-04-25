from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.contrib.middlewares.logging import LoggingMiddleware
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())
#bot = Bot(os.getenv('TOKEN'))
bot = Bot(TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())