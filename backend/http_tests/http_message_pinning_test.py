import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

user1 = {   
    "password": "qwertyuiop",
    "email": "address1@email.com", 
    "name_first": "U1", 
    "name_last": "One", 
    "handle_str": "u1one"
}
user2 = {   
    "password": "asdfghjkl",
    "email": "address2@email.com", 
    "name_first": "U2", 
    "name_last": "Two", 
    "handle_str": "u2two"
}
user3 = {   
    "password": "mnbvcxz",
    "email": "address3@email.com", 
    "name_first": "U3", 
    "name_last": "Three", 
    "handle_str": "u3three"
}                   

def register_users(): 

    requests.delete(config.url + "clear/v1")
    resp = requests.post(config.url + "auth/register/v2", json = {
        "email": user1["email"],
        "password": user1["password"],
        "name_first": user1["name_first"],
        "name_last": user1["name_last"]
    })
    user_one = json.loads(resp.text)
    
    resp = requests.post(config.url + "auth/register/v2", json = {
        "email": user2["email"],
        "password": user2["password"],
        "name_first": user2["name_first"],
        "name_last": user2["name_last"]
    })
    user_two = json.loads(resp.text)
    
    resp = requests.post(config.url + "auth/register/v2", json = {
        "email": user3["email"],
        "password": user3["password"],
        "name_first": user3["name_first"],
        "name_last": user3["name_last"]
    })
    user_three = json.loads(resp.text)
    
    return user_one, user_two, user_three

def send_group_message_in_dm(user_one, member_ids):
    resp = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": member_ids
    })

    new_dm = resp.json()
    
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
    
    message_id = resp.json()['message_id']
    
    return message_id, new_dm

def extract_dm_message_data(user_one, new_dm):
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
        
    return message_output
 
def send_group_message_in_channel(user_one):
    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_one['token'],
        'name': 'Channel', 
        'is_public': False,
    })
    new_chan = json.loads(r.text)
    
    resp = requests.post(config.url + "message/send/v2", json = {
        "token": user_one["token"],
        "channel_id": new_chan['channel_id'],
        "message": "hi"
    })
    
    message_id = resp.json()['message_id']
    
    return message_id, new_chan

def extract_channel_message_data(user_one, new_chan):
    # Extract the messages from new_chan
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": new_chan['channel_id'],
        "start": 0
    })
    
    message_output =  resp.json()
 
    return message_output    
    
#################################################
#              Test message_pin                 #
#################################################
    
def test_message_pin_dm():
    user_one, _, _ = register_users()
    message_id, new_dm = send_group_message_in_dm(user_one, [])
    message_output = extract_dm_message_data(user_one, new_dm)
    
    assert not message_output['messages'][0]['is_pinned']
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    assert resp.json() == {}
    
    message_output = extract_dm_message_data(user_one, new_dm)
    
    assert message_output['messages'][0]['is_pinned']
    

def test_message_pin_channel():    
    user_one, _, _ = register_users()
    
    message_id, new_chan = send_group_message_in_channel(user_one)
    
    message_output = extract_channel_message_data(user_one, new_chan)

    assert not message_output['messages'][0]['is_pinned']
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    assert resp.json() == {}
    
    message_output = extract_channel_message_data(user_one, new_chan)
    
    assert message_output['messages'][0]['is_pinned']


def test_message_pin_invalid_message_id():
    user_one, _, _ = register_users()
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": 987654321,
    })
    
    assert resp.status_code == INPUT_ERROR
   

def test_message_pin_already_pinned():
    user_one, _, _ = register_users()
    
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == INPUT_ERROR 
        
def test_message_pin_user_not_member():
    user_one, user_two, _ = register_users()
    
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_two["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR


def test_message_pin_user_not_owner():
    user_one, user_two, _ = register_users()
    
    message_id, _ = send_group_message_in_dm(user_one, [user_two['auth_user_id']])
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": user_two["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR


def test_message_pin_invalid_token():
    user_one, _, _ = register_users()
    
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    resp = requests.post(config.url + "message/pin/v1", json = {
        "token": "invalid_token",
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR     

#################################################
#             Test message_unpin                #
#################################################

def test_message_unpin_dm():
    user_one, _, _ = register_users()
    message_id, new_dm = send_group_message_in_dm(user_one, [])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    message_output = extract_dm_message_data(user_one, new_dm)
    
    assert message_output['messages'][0]['is_pinned']
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    assert resp.json() == {}
    
    message_output = extract_dm_message_data(user_one, new_dm)
    
    assert not message_output['messages'][0]['is_pinned']


def test_message_unpin_channel():    
    user_one, _, _ = register_users()
    
    message_id, new_chan = send_group_message_in_channel(user_one)
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
       
    message_output = extract_channel_message_data(user_one, new_chan)

    assert message_output['messages'][0]['is_pinned']
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    assert resp.json() == {}
    
    message_output = extract_channel_message_data(user_one, new_chan)
    
    assert not message_output['messages'][0]['is_pinned']
    

def test_message_unpin_invalid_message_id():
    user_one, _, _ = register_users()
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })

    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_one["token"],
        "message_id": 987654321,
    })
    
    assert resp.status_code == INPUT_ERROR   

def test_message_unpin_already_unpinned():
    user_one, _, _ = register_users()
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == INPUT_ERROR

        
def test_message_unpin_user_not_member():
    user_one, user_two, _ = register_users()
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_two["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR

def test_message_unpin_user_not_owner():
    user_one, user_two, _ = register_users()
    message_id, _ = send_group_message_in_dm(user_one, [user_two['auth_user_id']])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": user_two["token"],
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR    

def test_message_unpin_invalid_token():
    user_one, _, _ = register_users()
    message_id, _ = send_group_message_in_dm(user_one, [])
    
    requests.post(config.url + "message/pin/v1", json = {
        "token": user_one["token"],
        "message_id": message_id,
    })
    
    resp = requests.post(config.url + "message/unpin/v1", json = {
        "token": "invalid_token",
        "message_id": message_id,
    })
    
    assert resp.status_code == ACCESS_ERROR    
    
