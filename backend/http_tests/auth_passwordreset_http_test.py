import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

###----------------###
### Error Checking ###
###----------------###

def test_invalid_reset_code():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    r = requests.post(config.url + "auth/passwordreset/request/v1", json = {
        'email': 'john.apple@example.com',
    })
    r = requests.post(config.url + "auth/passwordreset/reset/v1", json = {
        'reset_code': 'invalid_code', 
        'new_password': 'validpassword',
    })
    assert r.status_code == INPUT_ERROR

def test_password_too_short():
    r = requests.post(config.url + "auth/passwordreset/reset/v1", json = {
        'reset_code': 'valid_code', 
        'new_password': 'short',
    })
    assert r.status_code == INPUT_ERROR