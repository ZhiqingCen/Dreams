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
    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': 'Darcy',
        'name_last': 'Bold'
    })
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': login['auth_user_id']
    })
    user_dict = r.json()
    user = user_dict['user']
    assert user['name_first'] == 'Darcy' and user['name_last'] == 'Bold'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token():
    requests.delete(config.url + "clear/v1")
    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': 'invalid_token',
        'name_first': 'Darcy',
        'name_last': 'Bold'
    })
    assert r.status_code == ACCESS_ERROR

def test_short_firstname():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()

    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': '',
        'name_last': 'tooshort'
    })
    assert r.status_code == INPUT_ERROR

def test_short_lastname():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()

    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': 'tooshort',
        'name_last': ''
    })
    assert r.status_code == INPUT_ERROR

def test_long_firstname():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()

    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': 51*'L',
        'name_last': 'toolong'
    })
    assert r.status_code == INPUT_ERROR

def test_long_lastname():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()

    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': 'toolong',
        'name_last': 51*'L'
    })
    assert r.status_code == INPUT_ERROR

def test_name_is_removed_user():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()

    r = requests.put(config.url + "user/profile/setname/v2", json = {
        'token': login['token'],
        'name_first': 'Removed',
        'name_last': 'user'
    })
    assert r.status_code == INPUT_ERROR