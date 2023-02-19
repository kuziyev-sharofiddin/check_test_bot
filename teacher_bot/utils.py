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

class NameTestStates(StatesGroup):
    test = State()

class FeedBackGroupNameStates(StatesGroup):
    group_name =State()

class FeedBackStudentStates(StatesGroup):
    student_name =State()

class GroupDeleteStates(StatesGroup):
    name =State()
def create_test_name(test_names):
    url = f"{BASE_URL}/tests/"

    if test_names:
        test = requests.post(url=url, data = {
            "name":test_names,
        })
        return test
    else:
        return None

def create_test(test, message,  teachers, groups):
    url = f"{BASE_URL}/test_key_create/"

    if test and message and  teachers and groups:        
        test = requests.post(url=url, data = {
            "test":test,
            "message":message,
            "teacher": teachers,
            "group": groups,
        })
        return test

    else:
        return None
    
def add_to_group(text, teacher):
    url = f"{BASE_URL}/group_create/"
    if text and teacher:
        add_group = requests.post(url=url, data = {
            "name":text,
            "teacher":teacher,
        })
        return add_group
    
def add_to_student(teacher, group, name):
    url = f"{BASE_URL}/student_create/"
    if teacher and group and name:
        add_student = requests.post(url=url, data = {
            "teacher": teacher,
            "group": group,
            "name": name,
        })
        return add_student
    
def delete_group(id):
    url=f"{BASE_URL}/group/{id}/"
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    group_delete = requests.delete(url=url, headers=headers)
    return group_delete

def delete_group_student(id):
    url=f"{BASE_URL}/student/{id}/"
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    group_delete_students = requests.delete(url=url, headers=headers)
    return group_delete_students