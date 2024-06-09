import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

###----------------###
### Error Checking ###
###----------------###

def test_email_not_registered():
    r = requests.post(config.url + "auth/passwordreset/request/v1", json = {
        'email': 'not_registered@email.com',
    })
    assert r.status_code == INPUT_ERROR

def test_empty():
    r = requests.post(config.url + "auth/passwordreset/request/v1", json = {
        'email': '',
    })
    assert r.status_code == INPUT_ERROR
