'''
http test file for src/message_unreact_v1
'''
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR, OK

url = config.url
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

###-----------------------------------------------------------###
### message_unreact_v1(token, message_id, react_id) return {} ###
###-----------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_unreact_v1
def test_message_unreact_empty_token():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': '', 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function message_unreact_v1
def test_message_unreact_none_token():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': None, 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function message_unreact_v1
def test_message_unreact_invalid_token_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': 123456789, 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function message_unreact_v1
def test_message_unreact_token_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': 'invalid_token', 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input message_id for function message_unreact_v1
def test_message_unreact_none_message_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': None, 'react_id': 1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input message_id for function message_unreact_v1
def test_message_unreact_invalid_message_id_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': 'invalid_message_id', 'react_id': 1})
    assert resp.status_code == INPUT_ERROR

# input of none existing message_id for function message_unreact_v1
def test_message_unreact_message_id_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': 123456789, 'react_id': 1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input react_id for function message_unreact_v1
def test_message_unreact_none_react_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'react_id': None})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input react_id for function message_unreact_v1
def test_message_unreact_invalid_react_id_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'react_id': 'invalid_react_id'})
    assert resp.status_code == INPUT_ERROR

# input of none existing react_id for function message_unreact_v1
def test_message_unreact_react_id_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'react_id': 2})
    assert resp.status_code == INPUT_ERROR

# user trying to unreact channel message but not a channel member for function message_unreact_v1
def test_message_unreact_not_channel_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_two['token'], 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# user trying to unreact dm message but not a dm member for function message_unreact_v1
def test_message_unreact_not_dm_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_two['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_three['token'], 'message_id': dm_message['message_id'], 'react_id': 1})
    assert resp.status_code == ACCESS_ERROR

# user trying to unreact message that had not been reacted before for function message_unreact_v1
def test_message_unreact_not_reacted_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_two['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_two['token'], 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == INPUT_ERROR

### ----output checking---- ###
# user unreact to channel message with react exists for function message_unreact_v1
def test_message_unreact_channel_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_two['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    requests.post(url + 'message/react/v1', json = {'token': user_two['token'], 'message_id': message1['message_id'], 'react_id': 1})
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_two['token'], 'message_id': message1['message_id'], 'react_id': 1})
    assert resp.status_code == OK
    resp = json.loads(resp.text)
    assert resp == {}

# user unreact to dm message with react exists for function message_unreact_v1
def test_message_unreact_dm_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_two['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    requests.post(url + 'message/react/v1', json = {'token': user_two['token'], 'message_id': dm_message['message_id'], 'react_id': 1})
    resp = requests.post(url + 'message/unreact/v1', json = {'token': user_two['token'], 'message_id': dm_message['message_id'], 'react_id': 1})
    assert resp.status_code == OK
