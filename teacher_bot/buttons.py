from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import BASE_URL
import requests
import json

  
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
            KeyboardButton(text="Guruhni qo'shish"),
            KeyboardButton(text="Guruhni o'chirish"),
            KeyboardButton(text="Guruhni ko'rish")
        ]
    ]
)



group_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Guruhga test jo'natish"),
            KeyboardButton(text="Guruhni natijalarini bilish"),
        ]
    ]
)