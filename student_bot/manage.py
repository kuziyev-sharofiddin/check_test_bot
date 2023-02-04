import logging
from buttons import start_button,group_test_buttons
from utils import  FeedBackUsernameStates
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils import BASE_URL, check_test, test_name_one,test_name_two


API_TOKEN = '5973107652:AAG4ZnWOxcKk5fJA_47bstbP346EDB0nAYA'

import requests
import json


# print(test_name_one())

logging.basicConfig(level=logging.INFO)


steps = {
    "start": "start",
    "begin": "begin",
    "enter_name": "enter_name",
    "enter_login": "enter_login",
    "choose_test": "choose_test",
    "send_answer": "send_answer",
    "result_waiting": "result_waiting"
}

data = {
    "step": "",
    "state": []
}


bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    data["step"] = steps["begin"]
    await message.reply(
        """Assalomu alaykum hurmatli o'quvchi. Xush kelibsiz!
        Men sizga testdan nechtasini to'gri ishlaganingizni bilib beraman.
        Quyidagi tugmani bosing:""",
        reply_markup=start_button
    )


        
@dp.message_handler(Text(startswith="Boshlash"),lambda message: data["step"] == steps["begin"])
async def echos(message: types.Message):
    data["step"] = steps["enter_name"]
    await message.answer("Iltimos ismingizni kiriting")
    
 
@dp.message_handler(lambda message: data["step"] == steps["enter_name"])
async def echok(message: types.Message):
    filtered_students = requests.get(url=f"{BASE_URL}/students/?name={message.text}")
    student = filtered_students.json()
    if student:
        data["step"] = steps["enter_login"]
        await message.answer("Loginni kiriting:")
    else:
        data["step"] = steps["begin"]
        await message.answer("""Noto'g'ri ism kiritdingiz.\nIltimos quyidagi tugmani bosing.
                             va boshqattan ism kiriting""", reply_markup=start_button)



@dp.message_handler(lambda message: data["step"] == steps["enter_login"])
async def echok(message: types.Message):
    filtered_students = requests.get(url=f"{BASE_URL}/students/?login={message.text}")
    student = filtered_students.json()
    if student:
        data["step"] = steps["choose_test"]
        await message.answer("Quyidagilardan birini tanlang", 
                             reply_markup=group_test_buttons(student[0]['group']['id']))
    else:
        data["step"] = steps["begin"]
        await message.answer("""Noto'g'ri login kiritdingiz.Iltimos quyidagi tugmani bosing.
                            va boshqattan login kiriting""", reply_markup=start_button)
        
        

@dp.message_handler(Text(endswith="-Test"),lambda message: data["step"] == steps["choose_test"])
async def test(message: types.Message):
    filtered_tests = requests.get(url=f"{BASE_URL}/tests/?name={message.text}").json()
    test = str(filtered_tests[0]['message']).split(' ')
    print(test)

    data["step"] = steps["send_answer"]
    data["state"] = test
    
    await message.answer("Kalitlarni kiriting:")



@dp.message_handler(lambda message: data["step"] == steps["send_answer"])
async def test(message: types.Message):
    send_test = message.text.split(' ')
    
    results = check_test(data["state"], send_test)
    print(results)        
        
    
    resultStr = ""
    
    for res in results:
        resultStr += res  + '\n'
    
    data["step"] = steps["result_waiting"]
    await message.answer(resultStr)

# @dp.message_handler(Text(endswith=f"{test_name_one(student[0]['group']['id'])}"))
# async def test(message: types.Message):
#     await message.answer("Test kalitlarini kiriting:")
    
        

    


    

    
# async def feedback_name(message: types.Message, state:FSMContext):
#     await message.answer("Iltimos ismingizni kiriting:")
#     await FeedBackUsernameStates.name.set()

# @dp.message_handler(state=FeedBackUsernameStates.name)
# async def feedback_name_done(message: types.Message, state:FSMContext):
#     await message.answer(create_student_name(message.from_user.id, message.text))
#     await state.finish()



    
if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)