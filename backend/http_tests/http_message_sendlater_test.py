import requests
import json
from src import config
from src.helper_func import extract_current_time
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

def register_users2(): 
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

def create_dm(user_one, member_ids):
    resp = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": member_ids
    })

    new_dm = resp.json()
    
    return new_dm

def extract_dm_message_data(user_one, new_dm):
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
        
    return message_output
 
def create_channel(user_one):
    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_one['token'],
        'name': 'Channel', 
        'is_public': False,
    })
    new_chan = json.loads(r.text)
    
    return new_chan

def extract_channel_message_data(user_one, new_chan):
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": new_chan['channel_id'],
        "start": 0
    })
    
    message_output =  resp.json()
 
    return message_output    

#############################################
#         Test message_sendlater            #
#############################################

def test_message_sendlater_dm():
    user_one, _, _ = register_users2()
    
    new_dm = create_dm(user_one, [])

    time_now = extract_current_time()
    
    sent_message = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm['dm_id'],
        "message": "hi",
        "time_sent": time_now + 1
    })
    assert isinstance(sent_message.json()['message_id'] , int)
        
    message_output = extract_dm_message_data(user_one, new_dm)
    
    # Confirm message is sent
    assert message_output['messages'][0]['message'] == "hi"

    # Confirm the message timestamp is correct
    assert message_output['messages'][0]['time_created'] >= time_now
    assert message_output['messages'][0]['time_created'] <= time_now + 2

def test_message_sendlater_channel():
    user_one, _, _ = register_users2()
    
    new_channel = create_channel(user_one)
    
    time_now = extract_current_time()
    
    sent_message = requests.post(config.url + "message/sendlater/v1", json = {
        "token": user_one["token"],
        "channel_id": new_channel['channel_id'],
        "message": "hi",
        "time_sent": time_now + 1
    })
    
    assert isinstance(sent_message.json()['message_id'] , int)
    
    message_output = extract_channel_message_data(user_one, new_channel)

    # Confirm message is sent
    assert message_output['messages'][0]['message'] == "hi"

    # Confirm the message timestamp is correct
    assert message_output['messages'][0]['time_created'] >= time_now
    assert message_output['messages'][0]['time_created'] <= time_now + 2

def test_message_sendlater_time_edgecase():
    user_one, _, _ = register_users2()
    
    new_dm = create_dm(user_one, [])
    
    time_now = extract_current_time()
    
    sent_message = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm['dm_id'],
        "message": "hi",
        "time_sent": time_now
    })
    assert isinstance(sent_message.json()['message_id'] , int)

def test_message_sendlater_invalid_time():
    user_one, _, _ = register_users2()
    
    new_dm = create_dm(user_one, [])
    
    time_now = extract_current_time()
    
    resp = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm['dm_id'],
        "message": "hi",
        "time_sent": time_now - 1
    })
    
    assert resp.status_code == INPUT_ERROR

def test_message_sendlater_invalid_group_id():
    user_one, _, _ = register_users2()
    
    time_now = extract_current_time()
    
    resp = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": 987654321,
        "message": "hi",
        "time_sent": time_now + 1
    })
    
    assert resp.status_code == INPUT_ERROR
       
def test_message_sendlater_too_long():
    MAX_MESSAGE_LEN = 1000
    user_one, _, _ = register_users2()
    
    new_dm = create_dm(user_one, [])
    
    time_now = extract_current_time()
    
    sent_message = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm['dm_id'],
        "message": "a" * MAX_MESSAGE_LEN,
        "time_sent": time_now + 1
    })
    assert isinstance(sent_message.json()['message_id'] , int)
    
    resp = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm['dm_id'],
        "message": "a" * (MAX_MESSAGE_LEN + 1),
        "time_sent": time_now + 1
    })
    assert resp.status_code == INPUT_ERROR

def test_message_sendlater_invalid_token():
    user_one, _, _ = register_users2()
    
    new_dm = create_dm(user_one, [])
    
    time_now = extract_current_time()
    
    resp = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": "invalid_token",
        "dm_id": new_dm['dm_id'],
        "message": "hi",
        "time_sent": time_now + 1
    })
    assert resp.status_code == ACCESS_ERROR

def test_message_sendlater_not_group_member():
    user_one, user_two, user_three = register_users2()
    
    new_dm = create_dm(user_one, [user_two['auth_user_id']])
    
    time_now = extract_current_time()
    
    resp = requests.post(config.url + "message/sendlaterdm/v1", json = {
        "token": user_three['token'],
        "dm_id": new_dm['dm_id'],
        "message": "hi",
        "time_sent": time_now + 1
    })
    assert resp.status_code == ACCESS_ERROR