import requests
import json
from src import config

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_users_all_output():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'john.apple@example.com', 
        'password': 'password1',
        'name_first': 'John',
        'name_last': 'Apple'
    })
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'pete.orange@outlook.com', 
        'password': 'password2',
        'name_first': 'Pete',
        'name_last': 'Orange'
    })
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'mary_jane@yahoo.com', 
        'password': 'password3',
        'name_first': 'Mary',
        'name_last': 'Jane'
    })
    r = requests.post(config.url + "auth/register/v2", json = {
        'email': 'dave.path@hotmail.com', 
        'password': 'password4',
        'name_first': 'Dave',
        'name_last': 'Path'
    })
    login = r.json()

    r = requests.get(config.url + "users/all/v1", params = {'token': login['token']})
    users = r.json()['users']
    assert users == [{
        'u_id': 0,
        'email': 'john.apple@example.com',
        'handle_str': 'johnapple',
        'name_first': 'John',
        'name_last': 'Apple'},
        {'u_id': 1,
        'email': 'pete.orange@outlook.com',
        'handle_str': 'peteorange',
        'name_first': 'Pete',
        'name_last': 'Orange'},
        {'u_id': 2,
        'email': 'mary_jane@yahoo.com',
        'handle_str': 'maryjane',
        'name_first': 'Mary',
        'name_last': 'Jane'},
        {'u_id': 3,
        'email': 'dave.path@hotmail.com',
        'handle_str': 'davepath',
        'name_first': 'Dave',
        'name_last': 'Path'}]
