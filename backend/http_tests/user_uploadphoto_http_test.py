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
    requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': login['token'],
        'img_url': 'https://www.501commons.org/donate/Heart.jpg/image_preview',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 400,
    })
    r = requests.get(config.url + "user/profile/v2", params = {
        'token': login['token'],
        'u_id': 0
    })
    user_dict = r.json()
    user = user_dict['user']
    assert user['profile_img_url'] != 'imgurl/default.jpg'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token():
    requests.delete(config.url + "clear/v1")

    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    r = requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': 'invalid_token',
        'img_url': 'https://www.501commons.org/donate/Heart.jpg/image_preview',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 400,
    })
    assert r.status_code == ACCESS_ERROR
    
def test_not_jpg():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': login['token'],
        'img_url': 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png',
        'x_start': 0,
        'y_start': 0,
        'x_end': 200,
        'y_end': 400,
    })
    assert r.status_code == INPUT_ERROR
    
def test_invalid_crop1():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': login['token'],
        'img_url': 'https://www.501commons.org/donate/Heart.jpg/image_preview',
        'x_start': 0,
        'y_start': 0,
        'x_end': 600,
        'y_end': 500,
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_crop2():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': login['token'],
        'img_url': 'https://www.501commons.org/donate/Heart.jpg/image_preview',
        'x_start': -100,
        'y_start': 0,
        'x_end': 200,
        'y_end': 300,
    })
    assert r.status_code == INPUT_ERROR

def test_invalid_crop3():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    login = r.json()
    r = requests.post(config.url + "user/profile/uploadphoto/v1", json = {
        'token': login['token'],
        'img_url': 'https://www.501commons.org/donate/Heart.jpg/image_preview',
        'x_start': 200,
        'y_start': 200,
        'x_end': 100,
        'y_end': 100,
    })
    assert r.status_code == INPUT_ERROR