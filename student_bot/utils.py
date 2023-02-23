from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


BASE_URL = 'http://188.225.31.249:7999/api/v1'


urls = f"{BASE_URL}/tests/"
responses = requests.get(url=urls).text



class FeedBackTestNameStates(StatesGroup):
    name = State()

    
def check_test(org_test_keys, test_keys):
    results = []
    resultString = ""
    correct_count = ""
    for index, org_test_key  in enumerate(org_test_keys):
        if(len(test_keys) <= index ):
            pass
            # results.append(f"{index} javob kiritilmagan")
        elif(org_test_key == test_keys[index]):
            results.append(f" {test_keys[index]} ✅ ")
            resultString += "1"
            correct_count += "1"
            # correct.append(f"{test_keys[index]}")

        else:
            results.append(f" {test_keys[index]} ❌ ")
            resultString += "0"
            
    return [results, resultString, correct_count]
     

def create_testresponse(student, tests, answer_message, correct):
    url = f"{BASE_URL}/test_response_create/"
    print(answer_message)
    if answer_message and tests and student and correct:
        post = requests.post(url=url, data = {
            "answer_message":answer_message,
            "correct_response_count": correct,
            "student": student,
            "test": tests
        })
        return "Ishtirokingiz uchun tashakkur.\nNatijangiz ustozga jo'natildi"
    else:
        "Amal oxiriga yetmadi"


    