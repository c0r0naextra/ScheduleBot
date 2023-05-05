import sys
sys.path.append('/ScheduleBot/data')
from data.config import TOKEN
from aiogram import Bot, Dispatcher
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())
# bot = Bot(os.getenv('TOKEN'))
bot = Bot(TOKEN)
dp = Dispatcher(bot)
