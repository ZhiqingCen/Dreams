import time
import pytest
import requests
import json
from src import config
from http_tests.channel_http_test import register_users
from src.helper_func import extract_current_time
from src.error import ACCESS_ERROR, INPUT_ERROR

###--------------------------------------------------------------------------------------------------------------###
###                                           standup_start Http Tests                                           ###
###--------------------------------------------------------------------------------------------------------------###

###-------------###
### Test Set Up ###
###-------------###
ONE_SECOND = 1 #seconds
NOT_AN_INT = 1.5 #seconds
VALID_MESSAGE = "AERO: Message"
LONGEST_VALID_MESSAGE = 'a' * 1000
MESSAGE_TOO_LONG = 'a' * 1001

@pytest.fixture
@pytest.mark.usefixtures("register_users")
def create_channel(register_users):
    global_owner, channel_owner, member,_,_ = register_users
    
    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': channel_owner['token'],
        'name': 'Channel', 
        'is_public': True,
    })
    channel = json.loads(r.text)
    
    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': channel_owner['token'],
        'channel_id': channel['channel_id'], 
        'u_id': global_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': channel_owner['token'],
        'channel_id': channel['channel_id'], 
        'u_id': member['auth_user_id'],
    })

    nonexistent_channel = {'channel_id': channel['channel_id'] + 1}
    
    return channel, nonexistent_channel

def wait_for_threads_to_finish():
    time.sleep(1)


###----------------###
### Error Checking ###
###----------------###
def test_standup_start_invalid_token(register_users, create_channel):
    _, _, _, _, unregistered_user = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': unregistered_user['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    assert r.status_code == ACCESS_ERROR

def test_standup_start_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': not_member['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    assert r.status_code == ACCESS_ERROR

def test_standup_start_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': nonexistent_channel['channel_id'], 
        'length': ONE_SECOND,
    })
    assert r.status_code == INPUT_ERROR

def test_standup_start_invalid_length(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': NOT_AN_INT,
    })
    assert r.status_code == INPUT_ERROR

def test_standup_start_startup_already_active(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    assert r.status_code == INPUT_ERROR

    wait_for_threads_to_finish()

def test_standup_start_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': None,
        'channel_id': None, 
        'length': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': None,
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': None, 
        'length': ONE_SECOND,
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': None,
    })
    assert r.status_code == INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_standup_start_owner_begins(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    time_start = extract_current_time()
    expected_time_finish = time_start + 1

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
    })
    
    channel_activity = json.loads(r.text)['is_active']

    assert channel_activity == True
    
    assert returned_time_finish > time_start
    assert returned_time_finish <= expected_time_finish + 1

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": owner["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False

def test_standup_start_global_owner_begins(register_users, create_channel):
    global_owner,_,_,_,_ = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    time_start = extract_current_time()
    expected_time_finish = time_start + 1

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'], 
    })
    
    channel_activity = json.loads(r.text)['is_active']

    assert channel_activity == True
    
    assert returned_time_finish > time_start
    assert returned_time_finish <= expected_time_finish + 1

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": global_owner["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == global_owner['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False

def test_standup_start_member_begins(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    time_start = extract_current_time()
    expected_time_finish = time_start + 1

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
    })
    
    channel_activity = json.loads(r.text)['is_active']

    assert channel_activity == True
    
    assert returned_time_finish > time_start
    assert returned_time_finish <= expected_time_finish + 1

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": member["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == member['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False

###--------------------------------------------------------------------------------------------------------------###
###                                           standup_active Http Tests                                          ###
###--------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_standup_active_invalid_token(register_users, create_channel):
    _,_,_,_,unregistered_user = register_users
    channel, _ = create_channel
    
    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': unregistered_user['token'],
        'channel_id': channel['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

def test_standup_active_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': not_member['token'],
        'channel_id': channel['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

def test_standup_active_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': member['token'],
        'channel_id': nonexistent_channel['channel_id'], 
    })
    assert r.status_code == INPUT_ERROR

def test_standup_active_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': None,
        'channel_id': None, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': None,
        'channel_id': channel['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': member['token'],
        'channel_id': None, 
    })
    assert r.status_code == INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_standup_active_is_active(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
    })
    channel_activity = json.loads(r.text)

    assert channel_activity['is_active'] == True

    assert channel_activity['time_finish'] == returned_time_finish

    wait_for_threads_to_finish()

def test_standup_active_not_active(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel

    r = requests.get(config.url + 'standup/active/v1', params = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
    })
    channel_activity = json.loads(r.text)

    assert channel_activity['is_active'] == False

    assert channel_activity['time_finish'] == None

###--------------------------------------------------------------------------------------------------------------###
###                                           standup_send Http Tests                                            ###
###--------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_standup_send_invalid_token(register_users, create_channel):
    _,_,_,_,unregistered_user = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': unregistered_user['token'],
        'channel_id': channel['channel_id'], 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == ACCESS_ERROR

def test_standup_send_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': not_member['token'],
        'channel_id': channel['channel_id'], 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == ACCESS_ERROR
    
def test_standup_send_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': nonexistent_channel['channel_id'], 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == INPUT_ERROR

def test_standup_send_startup_not_active(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == INPUT_ERROR

def test_standup_send_group_message_too_long(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel
    
    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': MESSAGE_TOO_LONG,
    })
    assert r.status_code == INPUT_ERROR

    wait_for_threads_to_finish()

def test_standup_send_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': None,
        'channel_id': None, 
        'message': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': None,
        'channel_id': channel['channel_id'], 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': None, 
        'message': VALID_MESSAGE,
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': None,
    })
    assert r.status_code == INPUT_ERROR

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_standup_send_one_message(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': "Hello!",
    })

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": owner["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: Hello!'
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False

def test_standup_send_message_upper_limit(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': LONGEST_VALID_MESSAGE,
    })

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": owner["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: ' + LONGEST_VALID_MESSAGE
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False

def test_standup_send_multiple_messages(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    r = requests.post(config.url + 'standup/start/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'length': ONE_SECOND,
    })
    returned_time_finish = json.loads(r.text)['time_finish']

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': member['token'],
        'channel_id': channel['channel_id'], 
        'message': "Hello there",
    })

    r = requests.post(config.url + 'standup/send/v1', json = {
        'token': owner['token'],
        'channel_id': channel['channel_id'], 
        'message': "General Kenobi",
    })

    wait_for_threads_to_finish()

    r = requests.get(config.url + "channel/messages/v2", params = {
        "token": owner["token"],
        "channel_id": channel['channel_id'],
        "start": 0,
    })
    most_recent_message = json.loads(r.text)['messages'][0]

    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: Hello there\nuser1owner: General Kenobi'
    assert most_recent_message['time_created'] == returned_time_finish
    assert most_recent_message['is_pinned'] == False