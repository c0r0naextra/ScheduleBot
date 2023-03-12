from aiogram.utils import executor
from keyboards import reg_keyboards
from loader import dp
from handlers import student


executor.start_polling(dp, skip_updates=True)



# лекции во втоник {'Микробилогия, вирусология (МБ)': '07.03 21.03 04.04 11.04 18.04 02.05 16.05 23.05 30.05', 'Медицинская информатика (Минф)': '14.03 28.03 25.04'}