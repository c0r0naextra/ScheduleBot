from aiogram.utils import executor
from keyboards import reg_keyboards
from loader import dp
from handlers import student
import os
from config import WEBHOOK_PATH, WEBHOOK_URL, host, WEBAPP_PORT


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=student.on_startup,
    #     on_shutdown=student.on_shutdown,
    #     skip_updates=True,
    #     host=host,
    #     port=WEBAPP_PORT,
    # )
    