from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import BASE_URL
import requests
import json

def group_test_buttons(group):
    url = f"{BASE_URL}/test_keys/?teacher={group}"
    responses = requests.get(url=url).json()
    
    # print(responses)
    test1 = responses[-1]['test']['name']  
    test2 = responses[-2]['test']['name']
    return ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
            [
                KeyboardButton(text=f"{test1}"),
                KeyboardButton(text=f"{test2}")
            ]
        ]
    )

  
def group_buttons(teacher):
    url = f"{BASE_URL}/groups/?name=&teacher={teacher}"
    responses = requests.get(url=url).json()
    mk = ReplyKeyboardMarkup(resize_keyboard=True,)
    for n in responses:
        group = n['name']
        
        mk.insert(KeyboardButton(text=f"{group}"))
    return mk
    

start_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Boshlash')
        ]
    ]
)


choose_group_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Guruhni yoki o'quvchini qo'shish"),
            KeyboardButton(text="Guruhni yoki o'quvchini o'chirish"),
            KeyboardButton(text="Guruhni ko'rish")
        ]
    ]
)

add_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Guruhni qo'shish"),
            KeyboardButton(text="O'quvchini qo'shish"),
        ]
    ]
)


group_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Guruhga test jo'nati sh"),
            KeyboardButton(text="Guruhni natijalarini bilish"),
        ]
    ]
)