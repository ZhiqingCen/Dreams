import requests
import json
from src import config
from src.error import INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_full_pass():

    requests.delete(config.url + "clear/v1")

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    user1 = r.json()

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "mary_jane@example.com",
        "password": "password2",
        "name_first": "Mary",
        "name_last": "Jane"
    })
    user2 = r.json()

    r = requests.post(config.url + "auth/login/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
    })
    login1 = r.json()

    r = requests.post(config.url + "auth/login/v2", json = {
        "email": "mary_jane@example.com",
        "password": "password2",
    })
    login2 = r.json()

    assert login1['auth_user_id'] == user1['auth_user_id']
    assert login2['auth_user_id'] == user2['auth_user_id']

###----------------###
### Error Checking ###
###----------------###

#Tests for invalid passwords
def test_wrong_password():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'wrongpassword'
    })
    assert r.status_code == INPUT_ERROR

def test_switched_passwords():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password2'
    })
    assert r.status_code == INPUT_ERROR

def test_empty_password():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'john.apple@example.com', 
        'password': ''
    })
    assert r.status_code == INPUT_ERROR

#Tests for invalid emails
def test_incorrect_email():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'dave.path@example.com', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_no_at_sign():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'invalidformat.com', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_divider_char():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'invalid~character@example.com', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_start_char():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': '-invalidstart@example.com', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_end_char():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'invalidend//@example.com', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_short_tld():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'invalid_tld@example.a', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_long_tld():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': 'invalid_tld@example.abcd', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR

def test_empty_email():
    r = requests.post(config.url + "auth/login/v2", json = {
        'email': '', 
        'password': 'password1'
    })
    assert r.status_code == INPUT_ERROR