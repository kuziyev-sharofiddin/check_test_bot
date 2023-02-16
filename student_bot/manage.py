import logging
from buttons import start_button,group_test_buttons
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils import BASE_URL, check_test,create_testresponse, FeedBackTestNameStates


API_TOKEN = '5973107652:AAG4ZnWOxcKk5fJA_47bstbP346EDB0nAYA'

import requests
import json




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
    "state": {
        'org_answer': [],
        'answer': "",
        'student': [],
    },
}

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    data["step"] = steps["begin"]
    await message.reply(
        "Assalomu alaykum hurmatli o'quvchi. Xush kelibsiz!\nMen sizga testdan nechtasini to'g'ri ishlaganingizni bilib beraman.\nQuyidagi tugmani bosing:",
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
    data["state"]["student"] = student
    if student:
        data["step"] = steps["choose_test"]
        await message.answer("Quyidagilardan birini tanlang", 
                             reply_markup=group_test_buttons(student[0]['group']['id']))
    else:
        data["step"] = steps["begin"]
        await message.answer("Noto'g'ri ism kiritdingiz.\nIltimos quyidagi tugmani bosing va boshqattan ism kiriting", reply_markup=start_button)


        
        

@dp.message_handler(Text(endswith="-Test"),lambda message: data["step"] == steps["choose_test"])
async def test(message: types.Message):

    filtered_tests = requests.get(url=f"{BASE_URL}/test_keys/?test__name={message.text}").json()
    test = filtered_tests[0]
    data["step"] = steps["send_answer"]
    data["state"]["org_answer"] = test
    await message.answer("Kalitlarni kiriting:")
    await FeedBackTestNameStates.name.set()



@dp.message_handler(lambda message: data["step"] == steps["send_answer"], state=FeedBackTestNameStates.name)
async def test(message: types.Message, state:FSMContext):
    answers = message.text.split(' ')
    org_answer = str(data["state"]['org_answer']['message']).split(' ')
    if len(answers)== len(org_answer):
        
        checkResult = check_test(org_answer,answers)
        results = checkResult[0]
        resultString = checkResult[1]  
        counts = checkResult[2]  
        correct_counts = len(counts)
        data["state"]['answer'] = results
        resultstr = ""

                
        for index, res in enumerate(results):
            if (index+1)%5 == 0:
                 resultstr += res + "\n"
            else:
                resultstr += res + " "
            
        data["step"] = steps["result_waiting"]
        await message.answer(resultstr)
        await message.answer(f"Siz {len(org_answer)} tadan {correct_counts} ta topdingiz")
        result = create_testresponse(
            data["state"]["student"][0]["id"],
            data["state"]["org_answer"]['test']["id"],
            resultString,
            correct_counts,
        )
        await message.answer(result)
        await state.finish()
    else:
        data["step"] = steps["send_answer"]
        await message.answer("Kalitlarni to'liq kiritmadingiz.Iltimos kalitlarni to'liq kiriting:")
        await FeedBackTestNameStates.name.set()
    
if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)