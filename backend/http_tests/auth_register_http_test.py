import requests
import json
from src import config
from src.error import INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_valid_new_user():
    requests.delete(config.url + "clear/v1")

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    user1 = r.json()

    assert user1['auth_user_id'] == 0

def test_3_valid_new_users():
    requests.delete(config.url + "clear/v1")

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "john.apple@example.com",
        "password": "password1",
        "name_first": "John",
        "name_last": "Apple"
    })
    user1 = r.json()

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "mary_jane@yahoo.com",
        "password": "password2",
        "name_first": "Mary",
        "name_last": "Jane"
    })
    user2 = r.json()

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": "dave.path@hotmail.com",
        "password": "password3",
        "name_first": "Dave",
        "name_last": "Path"
    })
    user3 = r.json()

    assert user1['auth_user_id'] == 0
    assert user2['auth_user_id'] == 1
    assert user3['auth_user_id'] == 2

###----------------###
### Error Checking ###
###----------------###

#Test for invalid emails

#Invalid formats
def test_format_no_at():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalidformat.com', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

def test_format_no_tld():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalidformat@example', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

#Invalid Characters
def test_invalid_divider():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalid~character@example.com', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_start():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': '-invalidstart@example.com', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_end():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalidend//@example.com', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

#Invalid TLD
def test_short_tld():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalid_tld@example.a', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

def test_long_tld():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'invalid_tld@example.abcd', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

#Other invalid cases    
def test_email_in_use():
    
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@outlook.com', 
        'password': 'password1',
        'name_first': 'Valid',
        'name_last': 'Email'
    })
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@outlook.com',
        'password': 'password1',
        'name_first': 'Used',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

def test_empty_email():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': '', 
        'password': 'password1',
        'name_first': 'Invalid',
        'name_last': 'Email'
    })
    assert r.status_code == INPUT_ERROR

#Tests for invalid passwords
def test_short_password():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'short.password@example.com', 
        'password': 'short',
        'name_first': 'Invalid',
        'name_last': 'Password'
    })
    assert r.status_code == INPUT_ERROR

def test_empty_password():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'empty.password@example.com', 
        'password': '',
        'name_first': 'Invalid',
        'name_last': 'Password'
    })
    assert r.status_code == INPUT_ERROR

#Tests for invalid name_first  
def test_empty_name_first():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': '',
        'name_last': 'Name'
    })
    assert r.status_code == INPUT_ERROR

def test_long_name_first():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': 51*'L',
        'name_last': 'Name'
    })
    assert r.status_code == INPUT_ERROR

#Tests for invalid name_last
def test_empty_name_last():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': 'Name',
        'name_last': ''
    })
    assert r.status_code == INPUT_ERROR

def test_long_name_last():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': 'Name',
        'name_last': 51*'L'
    })
    assert r.status_code == INPUT_ERROR

#Tests for both name_first and name_last
def test_empty_first_last():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': '',
        'name_last': ''
    })
    assert r.status_code == INPUT_ERROR

def test_long_first_last():
    
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'example@example.com', 
        'password': 'password1',
        'name_first': 51*'L',
        'name_last': 51*'L'
    })
    assert r.status_code == INPUT_ERROR