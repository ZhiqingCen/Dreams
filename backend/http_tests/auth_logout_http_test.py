import requests
import json
from src import config
from src.error import ACCESS_ERROR, OK

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_pass():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'adam.orange@gmail.com', 
        'password': 'password1',
        'name_first': 'Adam',
        'name_last': 'Orange'
    })
    user1 = r.json()

    r = requests.post(config.url + "auth/logout/v1", json = {
        'token': user1['token']
    })
    result = r.json()
    assert result['is_success'] == True

def test_logout_successfully():
    '''
    Create a user and have them create a dm then logout. Check that the logout
    was successful by checking that the user's token is no longer valid.
    '''

    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'adam.orange@gmail.com', 
        'password': 'password1',
        'name_first': 'Adam',
        'name_last': 'Orange'
    })
    user1 = json.loads(r.text)

    # Have user1 create a DM by passing in their token
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    })    
    
    # Confirm the creation of the DM was successful
    assert r.status_code == OK
    
    # Logout the user
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1['token']
    })
    
    # Check that the user token can no longer be used to create DM by confirming an
    # AccessError is raised
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    }) 
    
    assert r.status_code == ACCESS_ERROR

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token():
    requests.delete(config.url + "clear/v1")
    r = requests.post(config.url + "auth/logout/v1", json = {
        'token': 'invalid_token'
    })
    result = r.json()
    assert result['is_success'] == False

def test_removed_user():
    requests.delete(config.url + "clear/v1")

    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'adam.orange@gmail.com', 
        'password': 'password1',
        'name_first': 'Adam',
        'name_last': 'Orange'
    })
    user1 = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.doe@gmail.com', 
        'password': 'password2',
        'name_first': 'John',
        'name_last': 'Doe'
    })
    user2 = json.loads(r.text)

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user1['token'],
        'u_id': user2['auth_user_id'],
    })
    
    r = requests.post(config.url + "auth/logout/v1", json = {
        'token': user2['token']
    })
    result = r.json()
    assert result['is_success'] == False
