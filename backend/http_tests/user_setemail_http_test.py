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
    requests.put(config.url + "user/profile/setemail/v2", json = {
        'token': login['token'],
        'email': 'new.email@example.com'
    })
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': 0
    })
    user_dict = r.json()
    user = user_dict['user']
    assert user['email'] == 'new.email@example.com'

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

    r = requests.put(config.url + "user/profile/setemail/v2", json = {
        'token': 'invalid_token',
        'email': 'new.email@example.com'
    })
    assert r.status_code == ACCESS_ERROR

def test_invalid_email():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.put(config.url + "user/profile/setemail/v2", json = {
        'token': login['token'],
        'email': 'invalidemail.com'
    })
    assert r.status_code == INPUT_ERROR

def test_email_in_use():
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
    r = requests.put(config.url + "user/profile/setemail/v2", json = {
        'token': login['token'],
        'email': 'mary_jane@yahoo.com'
    })
    assert r.status_code == INPUT_ERROR
