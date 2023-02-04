from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
import json


import logging
# from utils import  FeedBackUsernameStates
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


BASE_URL = 'http://127.0.0.1:8000/api/v1'


urls = f"{BASE_URL}/tests/"
responses = requests.get(url=urls).text
dataa = json.loads(responses)


class FeedBackUsernameStates(StatesGroup):
    name = State()

        
def test_name_one():
    url = f"{BASE_URL}/tests/"
    filtered_tests = requests.get(url=url).json()
    urls = f"{BASE_URL}/students/"
    filtered_students = requests.get(url=urls).json()
    
    for i in filtered_tests:
        for x in filtered_students:
            if i['group']['id'] == x['group']['id']:
                return  filtered_tests[-1]['name']             
            


    
def check_test(org_test_keys, test_keys):
    results = []
    for index, org_test_key  in enumerate(org_test_keys):
        if(len(test_keys) <= index ):
            pass
            # results.append(f"{index} javob kiritilmagan")
        elif(org_test_key == test_keys[index]):
            results.append(f" {test_keys[index]} ✅ ")
        else:
            results.append(f" {test_keys[index]} ❌ ")
    return results

  
def test_name_two(name):
    url = f"{BASE_URL}/tests/?group={name}"
    filtered_tests = requests.get(url=url).json()
    test2 = filtered_tests[-2]['name']
    
    return test2  


    