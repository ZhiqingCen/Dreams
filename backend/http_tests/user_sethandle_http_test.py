import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_basic_pass():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    requests.put(config.url + "user/profile/sethandle/v1", json = {
        'token': login['token'],
        'handle_str': 'newhandle'
    })
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': 0
    })
    user_dict = r.json()
    user = user_dict['user']
    assert user['handle_str'] == 'newhandle'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })

    r = requests.put(config.url + "user/profile/sethandle/v1", json = {
        'token': 'invalid_token',
        'handle_str': 'newhandle'
    })
    assert r.status_code == ACCESS_ERROR

def test_short_handle():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.put(config.url + "user/profile/sethandle/v1", json = {
        'token': login['token'],
        'handle_str': 'ts'
    })
    assert r.status_code == INPUT_ERROR

def test_long_handle():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.put(config.url + "user/profile/sethandle/v1", json = {
        'token': login['token'],
        'handle_str': 21*'L'
    })
    assert r.status_code == INPUT_ERROR

def test_handle_in_use():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'mary_jane@yahoo.com', 
        'password': 'password2',
        'name_first': 'Mary',
        'name_last': 'Jane'
    })
    r = requests.post(config.url + "auth/login/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
    })
    login = r.json()
    r = requests.put(config.url + "user/profile/sethandle/v1", json = {
        'token': login['token'],
        'handle_str': 'maryjane'
    })
    assert r.status_code == INPUT_ERROR
