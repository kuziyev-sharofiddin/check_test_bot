import logging
from utils import BASE_URL, add_to_group, add_to_student, create_test, delete_group, delete_group_student, NameTestStates, FeedBackGroupNameStates,FeedBackStudentStates,GroupDeleteStates
from buttons import start_button, group_buttons, choose_group_button,group_button, group_test_buttons, add_button, delete_button, again_start_button
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# API_TOKEN = '5655557359:AAEtzNsDSm94zQSXwisZzSJu3SUrtrED0Tw'

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
    "student_id_add":"student_id_add",
    "enter_name_id":"enter_name_id",
    "student_delete":"student_delete",
    "student_deletes":"student_deletes",
    "choose_group_students": "choose_group_students",
    "student_add":"student_add",
    "student_add_to_group":"student_add_to_group",
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

data = {}

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    data[message.from_user.id] = {
        "step": "",
        "state": { 
            "test_keys":"",
            "test_name":"",
            "delete_groups_students":[],
            "test_names":[],
            "student_id":"",
            'delete_group': [],
            'student_group': [],
            'group': [],
            'groups':"",
            'answer': [],
            'teacher': [],
        },
    }
    data[message.from_user.id]["step"] = steps["begin"]
    await message.reply(
        "Assalomu alaykum hurmatli o'qituvchi. Xush kelibsiz!\nMen sizga testdan nechtasini to'g'ri ishlaganingizni bilib beraman.\nQuyidagi tugmani bosing:",
        reply_markup=start_button
    )

@dp.message_handler(Text(startswith="Boshlash"),lambda message: data[message.from_user.id]["step"] == steps["begin"])
async def begin(message: types.Message):
        data[message.from_user.id]["step"] = steps["enter_name_id"]
        await message.answer("Iltimos loginingizni kiriting")
        
@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["enter_name_id"])
async def begin(message: types.Message):
    data[message.from_user.id]["step"] = steps["enter_name_id"]
    filtered_teacher = requests.get(url=f"{BASE_URL}/teachers/?user_id={message.text}")
    teacher = filtered_teacher.json()
    data[message.from_user.id]["state"]["teacher"] = teacher
    if teacher:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Iltimos ismingizni kiriting")
    else:
        data[message.from_user.id]["step"] = steps["begin"]
        await message.answer("Noto'g'ri login kiritdingiz.\nIltimos quyidagi tugmani bosing va boshqattan login kiriting", reply_markup=start_button)
    

   
@dp.message_handler(Text(startswith="Guruhni ko'rish"))
async def group_view(message: types.Message):
    data[message.from_user.id]["step"] = steps["choose_group"]
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))


@dp.message_handler(Text(startswith="O'quvchilar ro'yxatini ko'rish"))
async def group_view(message: types.Message):
    data[message.from_user.id]["step"] = steps["choose_group_students"]
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))
    
@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["choose_group_students"])
async def group_delete(message: types.Message):
    view_group_students = requests.get(url=f"{BASE_URL}/students/?group__name={message.text}").json()
    if view_group_students:
        view_students = f"<b>{message.text}</b> guruhdagi o'quvchilar ro'yxati:\n"
        for view_student in view_group_students:
            view_students += f"Ism:<b>{view_student['name']}</b> Login:<b>{view_student['user_id']}</b>\n"
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer(view_students, reply_markup=choose_group_button)
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Guruhda hali o'quvchilar mavjud emas! Iltimos avval o'quvchi qo'shing", reply_markup=choose_group_button)





    

@dp.message_handler(Text(startswith="Guruhni yoki o'quvchini qo'shish"))
async def group_or_student_add(message: types.Message):
    await message.answer("Quyidagilardan birin tanlang", reply_markup=add_button)
 

@dp.message_handler(Text(startswith="Guruhni yoki o'quvchini o'chirish"))
async def group_or_student_add(message: types.Message):
    await message.answer("Quyidagilardan birini tanlang", reply_markup=delete_button)


@dp.message_handler(Text(startswith="Guruhni o'chirish"))
async def student_add(message: types.Message):
    data[message.from_user.id]["step"] = steps["group_delete"]
    await message.answer("O'chirmoqchi bo'lgan guruhingizni tanlang", 
                        reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["group_delete"])
async def group_delete(message: types.Message):
    deleted_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data[message.from_user.id]["state"]["delete_group"] = deleted_group
    if deleted_group:
        grp_delete = delete_group(
            data[message.from_user.id]["state"]["delete_group"][0]['id']
        )
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer(f"<b>{message.text}</b>-guruh muvaffaqiyatli o'chirildi", reply_markup=choose_group_button)
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Amal oxiriga yetmadi", reply_markup=choose_group_button)
        
 


@dp.message_handler(Text(startswith="O'quvchini o'chirish"))
async def student_delete(message: types.Message):
    data[message.from_user.id]["step"] = steps["student_delete"]
    await message.answer("O'chirmoqchi bo'lgan o'quvchingizni guruhini tanlang", 
                        reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["student_delete"])
async def student_delete_id(message: types.Message):
    filtered_group_student = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data[message.from_user.id]["state"]["delete_groups_students"] = filtered_group_student
    data[message.from_user.id]["step"] = steps["student_deletes"]
    await message.answer("O'chirmoqchi bo'lgan o'quvchingizni ismini kiriting")


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["student_deletes"])
async def student_deletes_id(message: types.Message):
    student_deletes = data[message.from_user.id]["state"]["delete_groups_students"][0]['name']
    filtered_group_student = requests.get(url=f"{BASE_URL}/students/?name={message.text}&group__name={student_deletes}").json()
    if filtered_group_student:
        respond = delete_group_student(
            filtered_group_student[0]['id']
        )
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer(f"<b>{student_deletes}<b/> guruhdagi <b>{message.text}</b> ismli o'quvchi muvaffaqiyatli o'chirildi", reply_markup=choose_group_button)
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Bu guruhda bunday o'quvchi mavjud emas! Iltimos boshqa amalni bajarib ko'ring", reply_markup=choose_group_button)

@dp.message_handler(Text(startswith="Guruhni qo'shish"))
async def student_add(message: types.Message):
    data[message.from_user.id]["step"] = steps["group_add"]
    await message.answer("Iltimos guruhga nom bering")
    await FeedBackGroupNameStates.group_name.set()


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["group_add"], state=FeedBackGroupNameStates.group_name)
async def group_add_name(message: types.Message, state:FSMContext):
    group_name = add_to_group(
        message.text,
        data[message.from_user.id]["state"]["teacher"][0]['id'],
    )
    if group_name:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Guruh yaratildi", reply_markup=choose_group_button)
        await state.finish()
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Amal oxiriga yetmadi", reply_markup=choose_group_button)

    



@dp.message_handler(Text(startswith="O'quvchini qo'shish"))
async def students_add(message: types.Message):
    data[message.from_user.id]["step"] = steps["student_add_to_group"]
    await message.answer("Iltimos o'quvchi qo'shiladigan guruhni tanlang", reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["student_add_to_group"])
async def student_add(message: types.Message):
    filtered_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    data[message.from_user.id]["state"]["student_group"] = filtered_group
    data[message.from_user.id]["step"] = steps["student_id_add"]
    await message.answer("O'quvchini loginini kiriting")
    # await FeedBackStudentStates.student_name.set()

@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["student_id_add"])
async def student_id_add(message: types.Message):
    data[message.from_user.id]["state"]["student_id"] = message.text
    data[message.from_user.id]["step"] = steps["student_add"]
    await message.answer("O'quvchini ismini kiriting")
    await FeedBackStudentStates.student_name.set()


@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["student_add"], state=FeedBackStudentStates.student_name)
async def student_add_name(message: types.Message, state:FSMContext):
    student_name = add_to_student(
        data[message.from_user.id]["state"]["teacher"][0]['id'],
        data[message.from_user.id]["state"]["student_group"][0]['id'],
        message.text,
        data[message.from_user.id]["state"]["student_id"],
    )
    if student_name:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("O'quvchi guruhga kiritildi", reply_markup=choose_group_button)
        await state.finish()
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Amal oxiriga yetmadi", reply_markup=choose_group_button)



@dp.message_handler(Text(startswith="Guruhga test jo'natish"))
async def send_test(message: types.Message):
    data[message.from_user.id]["step"] = steps["test_name_enter"]
    await message.answer("Iltimos testni nomini kiriting")

@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["test_name_enter"])
async def choose_group(message: types.Message):
    filtered_tests = requests.get(url=f"{BASE_URL}/test_keys/?name={message.text}").json()
    if filtered_tests:
        data[message.from_user.id]["step"] == steps["test_name_enter"]
        await message.answer("Bu nomdan avval foydalanilgan.Iltimos testga boshqa nom bering:")
    else:
        data[message.from_user.id]["state"]["test_name"] = message.text
        data[message.from_user.id]["step"] = steps["test_name"]
        await message.answer("Iltimos testni kalitlarini kiriting:")
        await NameTestStates.test.set()
        

@dp.message_handler(Text(startswith="Guruhni natijalarini bilish"))
async def test_results(message: types.Message):
    data[message.from_user.id]["step"] = steps["group_name_result"] 
    guruh = data[message.from_user.id]["state"]["groups"]
    url = f"{BASE_URL}/test_keys/?group__name={guruh}"
    responses = requests.get(url=url).json()
    if responses:
        await message.answer("Quyidagilardan birini tanlang", 
                            reply_markup=group_test_buttons(data[message.from_user.id]["state"]["group"][0]['id']))
    else:
        data[message.from_user.id]["step"] = steps["choose_group"]
        await message.answer("Ushbu guruhga hali test qo'shilmadi.Iltimos boshqa guruhni tanlang",
                             reply_markup=group_buttons(data[message.from_user.id]["state"]["teacher"][0]['id']))


@dp.message_handler(Text(endswith="-Test"), lambda message: data[message.from_user.id]["step"] == steps["group_name_result"])
async def test_results(message: types.Message):
    filtered_tests = requests.get(url=f"{BASE_URL}/test_responses/?test__name={message.text}").json()
    gr = data[message.from_user.id]["state"]["groups"]
    if filtered_tests:
        result=f"{gr}-guruh {message.text} natijalari:\n"
        for test_result in filtered_tests:
            result += f"<b>{test_result['student']['name']}</b> <b>{len(test_result['answer_message'])}</b> ta testdan <b>{test_result['correct_response_count']}</b> topdi \n"
        await message.answer(result)
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Boshqa amalni ko'ring", reply_markup=choose_group_button)
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Hali natijalar mavjud emas!", reply_markup=choose_group_button)



@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["test_name"], state=NameTestStates.test)
async def create_tests(message: types.Message,  state:FSMContext):
    test_name = data[message.from_user.id]["state"]["test_name"]
    data[message.from_user.id]["state"]["test_keys"] = message.text
    result = create_test(
        test_name,
        data[message.from_user.id]["state"]["test_keys"],
        data[message.from_user.id]["state"]["teacher"][0]['id'],
        data[message.from_user.id]["state"]["group"][0]['id'],
    )
    if result:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Test yaratildi", reply_markup=choose_group_button)
        await state.finish()
    else:
        data[message.from_user.id]["step"] = steps["enter_name"]
        await message.answer("Amal oxiriga yetmadi", reply_markup=choose_group_button)





@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["choose_group"])
async def choose_group(message: types.Message):
    data[message.from_user.id]["state"]["groups"] = message.text
    filtered_group = requests.get(url=f"{BASE_URL}/groups/?name={message.text}").json()
    group = filtered_group
    data[message.from_user.id]["state"]["group"] = group
    await message.answer("Quyidagilardan birini tanlang", 
                        reply_markup=group_button)




@dp.message_handler(lambda message: data[message.from_user.id]["step"] == steps["enter_name"])
async def enter_name(message: types.Message):
    filtered_teacher = requests.get(url=f"{BASE_URL}/teachers/?first_name={message.text}")
    teacher = filtered_teacher.json()
    data[message.from_user.id]["state"]["teacher"] = teacher
    if teacher:
            await message.answer("Quyidagilardan birini tanlang", 
                             reply_markup=choose_group_button)
    else:
        data[message.from_user.id]["step"] == steps["enter_name_id"]
        await message.answer("Noto'g'ri ism kiritdingiz.\nIltimos quyidagi tugmani bosing va boshqattan ism kiriting")



if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)