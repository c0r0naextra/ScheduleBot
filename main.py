from aiogram.utils import executor
from keyboards import reg_keyboards
from loader import dp
from handlers import student


executor.start_polling(dp, skip_updates=True)
