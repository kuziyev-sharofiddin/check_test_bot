from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import BASE_URL
import requests
import json


def group_test_buttons(group):
    url = f"{BASE_URL}/test_keys/?group={group}"
    responses = requests.get(url=url).json()
    
    # print(responses)
    test1 = responses[-1]['test']['name']
    test2 = responses[-2]['test']['name']
    print(test1)
    return ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
            [
                KeyboardButton(text=f"{test1}"),
                KeyboardButton(text=f"{test2}")
            ]
        ]
    )
    
 
    
start_button = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Boshlash')
            

        ]
    ]
)
