from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


BASE_URL = 'http://127.0.0.1:8000/api/v1'

class FeedBackTestNameStates(StatesGroup):
    name = State()
    test = State()



def create_test_name(groups, teachers, test_name):
    url = f"{BASE_URL}/tests/"

    if test_name and groups and teachers:
        post = requests.post(url=url, data = {
            "group": groups['id'],
            "teacher": teachers["id"],
            "name":test_name,
        })
        return "Iltimos testni kalitlarini kiriting"
    else:
        "Amal oxiriga yetmadi"

def create_test(groups, teachers, message):
    url = f"{BASE_URL}/tests/"

    if message and groups and teachers:
        post = requests.post(url=url, data = {
            "group": groups['id'],
            "teacher": teachers["id"],
            "message":message

        })
        return "Testni kalitlari bazaga jo'natildi"
    else:
        "Amal oxiriga yetmadi"