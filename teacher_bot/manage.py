import logging
from utils import BASE_URL,FeedBackTestNameStates, create_test_name, add_to_group, add_to_student, create_test, delete_group, delete_group_student, NameTestStates, FeedBackGroupNameStates,FeedBackStudentStates,GroupDeleteStates
from buttons import start_button, group_buttons, choose_group_button,group_button, group_test_buttons, add_button, delete_button, again_start_button
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text



API_TOKEN = '6097484074:AAG3RZMCdeA8gPyV1jNdJXWjJ1_8cKE7TQg'

import requests
import json




logging.basicConfig(level=logging.INFO)


steps = {
    "start": "start",
    "begin": "begin",
    "enter_name": "enter_name",
    "group_add":"group_add",
    "group_delete":"group_delet",
    "student_delete":"student_delete",
    "student_deletes":"student_deletes",
    "student_add":"student_add",
    "student_add_to_group":"student_add_to_group",
    "group_delete":"group_delete",
    "group_view":"group_view",
    "enter_login": "enter_login",
    "choose": "choose",
    "choose_group": "choose_group",
    "send_answer": "send_answer",
    "group_name_result":"group_name_result",
    "result_test": "result_test",
    "test_name_enter": "test_name_enter",
    "test_name":"test_name",
}

data = {
    "step": "",
    "state": {
        "test_keys":"",
        "test_name":"",
        "delete_groups_students":[],
        "test_names":[],
        'delete_group': [],
        'student_group': [],
        'group': [],
        'groups':"",
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
    


   
@dp.message_handler(Text(startswith="Guruhni ko'rish"))
async def group_view(message: types.Message):
    data["step"] = steps["choose_group"]
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_buttons(data["state"]["teacher"][0]['id']))


@dp.message_handler(Text(startswith="Guruhni yoki o'quvchini qo'shish"))
async def group_or_student_add(message: types.Message):
    await message.answer("Quyidagilardan birin tanlang", reply_markup=add_button)
 

@dp.message_handler(Text(startswith="Guruhni yoki o'quvchini o'chirish"))
async def group_or_student_add(message: types.Message):
    await message.answer("Quyidagilardan birin tanlang", reply_markup=delete_button)


@dp.message_handler(Text(startswith="Guruhni o'chirish"))
async def student_add(message: types.Message):
    data["step"] = steps["group_delete"]
    await message.answer("O'chirmoqchi bo'lgan guruhingizni tanlang", 
                        reply_markup=group_buttons(data["state"]["teacher"][0]['id']))

@dp.message_handler(lambda message: data["step"] == steps["group_delete"])
async def student_add(message: types.Message):
    deleted_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data["state"]["delete_group"] = deleted_group
    grp_delete = delete_group(
        data["state"]["delete_group"][0]['id']
    )
    response_text = f"{message.text}-guruh muvaffaqiyatli o'chirildi" if grp_delete else "Amal oxiriga yetmadi"
    await message.answer(response_text)
 


@dp.message_handler(Text(startswith="O'quvchini o'chirish"))
async def student_delete(message: types.Message):
    data["step"] = steps["student_delete"]
    await message.answer("O'chirmoqchi bo'lgan o'quvchingizni guruhini tanlang", 
                        reply_markup=group_buttons(data["state"]["teacher"][0]['id']))


@dp.message_handler(lambda message: data["step"] == steps["student_delete"])
async def student_delete_id(message: types.Message):
    filtered_group_student = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data["state"]["delete_groups_students"] = filtered_group_student
    data["step"] = steps["student_deletes"]
    await message.answer("O'chirmoqchi bo'lgan o'quvchingizni ismini kiriting")

@dp.message_handler(lambda message: data["step"] == steps["student_deletes"])
async def student_deletes_id(message: types.Message):
    student_deletes = data["state"]["delete_groups_students"][0]['name']
    filtered_group_student = requests.get(url=f"{BASE_URL}/students/?name={message.text}&group__name={student_deletes}").json()
    respond = delete_group_student(
        filtered_group_student[0]['id']
    )
    respond_text = f"{student_deletes} guruhdagi {message.text} ismli o'quvchi muvaffaqiyatli o'chirildi" if respond else "Amal oxiriga yetmadi"
    await message.answer(respond_text)

@dp.message_handler(Text(startswith="Guruhni qo'shish"))
async def student_add(message: types.Message):
    data["step"] = steps["group_add"]
    await message.answer("Iltimos guruhga nom bering")
    await FeedBackGroupNameStates.group_name.set()


@dp.message_handler(lambda message: data["step"] == steps["group_add"], state=FeedBackGroupNameStates.group_name)
async def group_add_name(message: types.Message, state:FSMContext):
    group_name = add_to_group(
        message.text,
        data["state"]["teacher"][0]['id'],
    )
    response_text = "Guruh yaratildi" if group_name else "Amal oxiriga yetmadi"
    await message.answer(response_text)
    await state.finish()

@dp.message_handler(Text(startswith="O'quvchini qo'shish"))
async def student_add(message: types.Message):
    data["step"] = steps["student_add_to_group"]
    await message.answer("Iltimos o'quvchi qo'shiladigan guruhni tanlang", reply_markup=group_buttons(data["state"]["teacher"][0]['id']))


@dp.message_handler(lambda message: data["step"] == steps["student_add_to_group"])
async def student_add(message: types.Message):
    filtered_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data["state"]["student_group"] = filtered_group
    data["step"] = steps["student_add"]

    await message.answer("O'quvchini ismini kiriting")
    await FeedBackStudentStates.student_name.set()


@dp.message_handler(lambda message: data["step"] == steps["student_add"], state=FeedBackStudentStates.student_name)
async def student_add_name(message: types.Message, state:FSMContext):
    print(data["state"]["student_group"])
    student_name = add_to_student(
        data["state"]["teacher"][0]['id'],
        data["state"]["student_group"][0]['id'],
        message.text,
    )
    response_text = "O'quvchi guruhga kiritildi" if student_name else "Amal oxiriga yetmadi"
    await message.answer(response_text)
    await state.finish()


@dp.message_handler(Text(startswith="Guruhga test jo'natish"))
async def send_test(message: types.Message):
    data["step"] = steps["test_name_enter"]
    await message.answer("Iltimos testni nomini kiriting")
    await FeedBackTestNameStates.name.set()

@dp.message_handler(lambda message: data["step"] == steps["test_name_enter"],  state=FeedBackTestNameStates.name)
async def choose_group(message: types.Message, state:FSMContext):
    data["state"]["test_name"] = message.text
    data["step"] = steps["test_name"]
    test_name = create_test_name(
        data["state"]["test_name"],
    )
    response_text = "Test kalitlarini kiriting" if test_name else "Amal oxiriga yetmadi"

    await message.answer(response_text)
    await state.finish()
    await NameTestStates.test.set()

@dp.message_handler(Text(startswith="Guruhni natijalarini bilish"))
async def test_results(message: types.Message):
    data["step"] = steps["group_name_result"] 
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_test_buttons(data["state"]["group"][0]['id']))


@dp.message_handler(Text(endswith="-Test"), lambda message: data["step"] == steps["group_name_result"])
async def test_results(message: types.Message):
    filtered_tests = requests.get(url=f"{BASE_URL}/test_responses/?test__name={message.text}").json()
    gr = data["state"]["groups"]
    result=f"{gr}-guruh {message.text} natijalari:\n"
    for test_result in filtered_tests:
        result += f"{test_result['student']['name']} {len(test_result['answer_message'])} ta testdan {test_result['correct_response_count']} topdi \n"
    await message.answer(result, reply_markup=choose_group_button)
    await message.answer("Boshqa amalni ko'ring", reply_markup=choose_group_button)



@dp.message_handler(lambda message: data["step"] == steps["test_name"], state=NameTestStates.test)
async def create_tests(message: types.Message,  state:FSMContext):
    test_name = data["state"]["test_name"]
    filtered_tests = requests.get(url=f"{BASE_URL}/tests/?name={test_name}").json()
    data["state"]["test_keys"] = message.text
    await message.answer(message.text)

    result = create_test(
        filtered_tests[0]['id'],
        data["state"]["test_keys"],
        data["state"]["teacher"][0]['id'],
        data["state"]["group"][0]['id'],
    )
    response_text = "Test yaratildi" if result else "Amal oxiriga yetmadi"
    await message.answer(response_text)
    await state.finish()




@dp.message_handler(lambda message: data["step"] == steps["choose_group"])
async def choose_group(message: types.Message):
    data["state"]["groups"] = message.text
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
    if teacher:
            await message.answer("Quyidagilardan birini tanlang", 
                             reply_markup=choose_group_button)
    else:
        data["step"] = steps["begin"]
        await message.answer("Noto'g'ri ism kiritdingiz.\nIltimos quyidagi tugmani bosing va boshqattan ism kiriting", reply_markup=start_button)

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)