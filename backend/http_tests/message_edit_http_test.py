'''
http test file for src/message_edit_v2
'''
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

one = {
    'email': 'address@email1.com',
    'password': 'UserOne111',
    'name_first': 'User',
    'name_last': 'One',
}
two = {
    'email': 'address@email2.com',
    'password': 'UserTwo222',
    'name_first': 'User',
    'name_last': 'Two',
}

three = {
    'email': 'address@email3.com',
    'password': 'UserThree333',
    'name_first': 'User',
    'name_last': 'Three',
}

# # create channels for testing
# d
###--------------------------------------------------------------###
### message_edit_v2(token, message_id, message) return {} ###
###--------------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_edit_v2
def test_message_edit_empty_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    resp = requests.put(config.url + 'message/edit/v2', json = {'token': '', 'message_id': message1['message_id'], 'message': 'new message'})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function message_edit_v2
def test_message_edit_none_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': None, 'message_id': message1['message_id'], 'message': 'new message'})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function message_edit_v2
def test_message_edit_invalid_token_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': 123456789, 'message_id': message1['message_id'], 'message': 'new message'})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function message_edit_v2
def test_message_edit_token_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': "invalid_token!@#123", 'message_id': message1['message_id'], 'message': 'new message'})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input message_id for function message_edit_v2
def test_message_edit_none_message_id():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': None, 'message': 'new message'})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input message_id for function message_edit_v2
def test_message_edit_invalid_message_id_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': "invalid_message_id", 'message': 'new message'})
    assert resp.status_code == INPUT_ERROR

# input of none existing message_id for function message_edit_v2
def test_message_edit_message_id_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': 123456789, 'message': 'new message'})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input message for function message_edit_v2
def test_message_edit_none_message():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': None})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input message for function message_edit_v2
def test_message_edit_invalid_message_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': 123456789})
    assert resp.status_code == INPUT_ERROR

# invalid parameter input message exceed 1000 characters for function message_edit_v2
def test_message_edit_exceed_length_limit_message():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    long_message = "a"*1001
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': long_message})
    assert resp.status_code == INPUT_ERROR

### ----output checking---- ###

# check message_edit_v2 output, input empty dm message
def test_message_edit_empty_dm_message():
    '''
    Test that if a message is edited in a dm to become an empty string, 
    the message is deleted.
    '''
    requests.delete(config.url + 'clear/v1')
    
    # Register users, create a DM and send a message in that DM.
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(config.url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    
    # Create dm and send a message in that DM
    dm = requests.post(config.url + 'dm/create/v1', json = {"token": user_one['token'], "u_ids": [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    r = requests.post(config.url + 'message/senddm/v1', json = {"token": user_one['token'], "dm_id": dm['dm_id'], "message": 'message'})
    dm_message = r.json()
    
    # Check that the message exists
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": dm['dm_id'],
        "start": 0
    })
    message_output =  resp.json()
    assert "message" in [message['message'] for message in message_output['messages']] 
    
    # Edit the message to have no contents
    requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': dm_message['message_id'], 'message': 'edit message'})
    
    # Check that the message no longer exists
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": dm['dm_id'],
        "start": 0
    })
    message_output =  resp.json()
    assert not "message" in [message['message'] for message in message_output['messages']] 


def test_message_edit_dm_message():
    '''
    Test that a messages sent in a dm can be edited.
    '''
    # Register user_one and user_two
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(config.url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    
    # Create dm and send a message in that DM
    dm = requests.post(config.url + 'dm/create/v1', json = {"token": user_one['token'], "u_ids": [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    r = requests.post(config.url + 'message/senddm/v1', json = {"token": user_one['token'], "dm_id": dm['dm_id'], "message": 'message'})
    dm_message = r.json()
    
    # Check that the message exists
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": dm['dm_id'],
        "start": 0
    })
    message_output =  resp.json()
    
    assert "message" in [message['message'] for message in message_output['messages']] 
    
    # Edit the message
    requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': dm_message['message_id'], 'message': 'edit message'})
    
    # Check that the edited message exists
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": dm['dm_id'],
        "start": 0
    })
    message_output =  resp.json()
    assert "edit message" in [message['message'] for message in message_output['messages']] 



def test_message_edit_empty_channel_message():
    '''
    Test that if a message is edited in a channel to become an empty string, 
    the message is deleted.
    '''
    requests.delete(config.url + 'clear/v1')
    
    # Register user and add create a channel then send a message in that channel
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    
    # Check that the message exists
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": channel1['channel_id'],
        "start": 0
    })
    message_output =  resp.json()
    assert "message" in [message['message'] for message in message_output['messages']] 
    
    
    # Edit the message to have no contents
    requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': ''})
    
    # Check that the message no longer exists
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": channel1['channel_id'],
        "start": 0
    })
    message_output =  resp.json()
    assert not "message" in [message['message'] for message in message_output['messages']] 


def test_message_edit_channel_message():
    '''
    Test that a user can edit the message sent in a channel.
    '''
    requests.delete(config.url + 'clear/v1')
    
    # Register user_one
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
        
    # Have user_one create a channel and send a message to that channel
    channel1 = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(config.url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    # Have user_one edit the message
    resp = requests.put(config.url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': 'edit message'})
    
    # Extract the messages from channel1
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": channel1['channel_id'],
        "start": 0
    })
    
    message_output =  resp.json()
    
    # check that the edited message is in channel messages.
    assert "edit message" in [message['message'] for message in message_output['messages']]  
    
    
    
