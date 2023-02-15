import logging
from utils import BASE_URL,FeedBackTestNameStates,create_test_name,create_test
from buttons import start_button,group_buttons, choose_group_button,group_button
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
# from utils import BASE_URL, check_test,create_testresponse, FeedBackTestNameStates


API_TOKEN = '6097484074:AAG3RZMCdeA8gPyV1jNdJXWjJ1_8cKE7TQg'

import requests
import json




logging.basicConfig(level=logging.INFO)


steps = {
    "start": "start",
    "begin": "begin",
    "enter_name": "enter_name",
    "group_add":"group_add",
    "group_delete":"group_delete",
    "group_view":"group_view",
    "enter_login": "enter_login",
    "choose": "choose",
    "choose_group": "choose_group",
    "send_answer": "send_answer",
    "result_test": "result_test",
    "test_name_enter": "test_name_enter",
    "test_name":"test_name",
}

data = {
    "step": "",
    "state": {
        "test_keys":"",
        "test_name":"",
        'group': [],
        'answer': [],
        'teacher': [],
    },
}

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    data["step"] = steps["begin"]
    await message.reply(
        "Assalomu alaykum hurmatli o'qituvchi. Xush kelibsiz!\nMen sizga testdan nechtasini to'g'ri ishlaganingizni bilib beraman.\nQuyidagi tugmani bosing:",
        reply_markup=start_button
    )


        
@dp.message_handler(Text(startswith="Boshlash"),lambda message: data["step"] == steps["begin"])
async def begin(message: types.Message):
    data["step"] = steps["enter_name"]
    await message.answer("Iltimos ismingizni kiriting")
    

   
@dp.message_handler(Text(startswith="Guruhni ko'rish"), lambda message: data["step"] == steps["group_view"])
async def group_view(message: types.Message):
    data["step"] = steps["choose_group"]
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_buttons(data["state"]["teacher"][0]['id']))


@dp.message_handler(Text(startswith="Guruhga test jo'natish"))
async def send_test(message: types.Message):
    data["step"] = steps["test_name_enter"]
    await message.answer("Iltimos testni nomini kiriting")
    await FeedBackTestNameStates.name.set()


@dp.message_handler(Text(startswith="Guruhni natijalarini bilish"))
async def test_results(message: types.Message):
    await message.answer("Natija")



@dp.message_handler(lambda message: data["step"] == steps["test_name_enter"],  state=FeedBackTestNameStates.name)
async def choose_group(message: types.Message, state:FSMContext):
    data["state"]["test_name"] = message.text
    data["step"] = steps["test_name"]
    result = create_test_name(
        data["state"]["group"][0],
        data["state"]["teacher"][0],
        data["state"]["test_name"],
    )
    await message.answer(result)
    await state.finish()
    await FeedBackTestNameStates.test.set()

@dp.message_handler(lambda message: data["step"] == steps["test_name"], state=FeedBackTestNameStates.test)
async def choose_group(message: types.Message,  state:FSMContext):
    print(message.text)
    await message.answer(message.text)
    data["state"]["test_keys"] = message.text
    result = create_test(
        data["state"]["group"][0],
        data["state"]["teacher"][0],
        data["state"]["test_keys"],
    )
    await message.answer(result)
    await state.finish()



@dp.message_handler(lambda message: data["step"] == steps["choose_group"])
async def choose_group(message: types.Message):
    filtered_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    group = filtered_group
    data["state"]["group"] = group
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_button)




@dp.message_handler(lambda message: data["step"] == steps["enter_name"])
async def enter_name(message: types.Message):
    filtered_teacher = requests.get(url=f"{BASE_URL}/teachers/?first_name={message.text}")
    teacher = filtered_teacher.json()
    data["state"]["teacher"] = teacher
    # print( data["state"]["teacher"])
    if teacher:
        data["step"] = steps["group_add"]
        data["step"] = steps["group_delete"]
        data["step"] = steps["group_view"]
        await message.answer("Quyidagilardan birini tanlang", 
                             reply_markup=choose_group_button)
    else:
        data["step"] = steps["begin"]
        await message.answer("Noto'g'ri ism kiritdingiz.\nIltimos quyidagi tugmani bosing va boshqattan ism kiriting", reply_markup=start_button)

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)