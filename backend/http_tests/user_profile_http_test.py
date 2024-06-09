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
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    login = r.json()
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': 0
    })
    profile = r.json()
    assert profile == {
        'user': {
            'u_id': 0,
            'email': 'john.apple@example.com',
            'name_first': 'John',
            'name_last': 'Apple',
            'handle_str': 'johnapple',
            'profile_img_url': 'imgurl/default.jpg'
        }
    }

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': 'invalid_token',
        'u_id': 0
    })
    assert r.status_code == ACCESS_ERROR

def test_invalid_u_id():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    login = r.json()
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': 999
    })
    assert r.status_code == INPUT_ERROR