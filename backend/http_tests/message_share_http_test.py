'''
http test file for src/message_share_v1
'''
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

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

###--------------------------------------------------------------------------------------------------------###
### message_share_v1(token, og_message_id, message, channel_id, dm_id) return { shared_message_id } ###
###--------------------------------------------------------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_share_v1
def test_message_share_empty_token():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': '', 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function message_share_v1
def test_message_share_none_token():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': None, 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == ACCESS_ERROR


# invalid parameter string input token for function message_share_v1
def test_message_share_invalid_token_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': 123456789, 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function message_share_v1
def test_message_share_token_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': 'invalid_token', 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input og_message_id for function message_share_v1
def test_message_share_none_og_message_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': None, 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input og_message_id for function message_share_v1
def test_message_share_invalid_og_message_id_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': "invalid_og_message_id", 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# input of none existing og_message_id for function message_share_v1
def test_message_share_og_message_id_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': 123456789, 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input message for function message_share_v1
def test_message_share_none_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': None, 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input message for function message_share_v1
def test_message_share_invalid_message_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 123456789, 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter input message exceed 1000 characters for function message_share_v1
def test_message_share_exceed_length_limit_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': "a"*1001, 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input channel_id for function message_share_v1
def test_message_share_none_channel_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': None, 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input channel_id for function message_share_v1
def test_message_share_invalid_channel_id_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': "invalid_channel_id", 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# input of none existing channel_id for function message_share_v1
def test_message_share_channel_id_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': 123456789, 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input dm_id for function message_share_v1
def test_message_share_none_dm_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_two['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': 'message', 'channel_id': -1, 'dm_id': None})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input dm_id for function message_share_v1
def test_message_share_invalid_dm_type():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_two['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': 'message', 'channel_id': -1, 'dm_id': 'invalid_dm_id'})
    assert resp.status_code == INPUT_ERROR

# input of none existing dm_id for function message_share_v1
def test_message_share_dm_id_not_exist():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_two['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': 'message', 'channel_id': -1, 'dm_id': 123456789})
    assert resp.status_code == INPUT_ERROR

# input of non-channel_member trying to share og_message from channel for function message_share_v1
def test_message_share_non_channel_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_two['token'], 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == ACCESS_ERROR

# input of non-dm_member tring to share og_message from dm for function message_share_v1
def test_message_share_non_dm_member():
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
    resp = requests.post(url + 'message/share/v1', json = {'token': user_three['token'], 'og_message_id': dm_message['message_id'], 'message': 'message', 'channel_id': -1, 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

# input of invalid channel_id and dm_id for function message_share_v1
def test_message_share_invalid_channel_id_and_dm_id():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'message', 'channel_id': -1, 'dm_id': -1})
    assert resp.status_code == INPUT_ERROR

### ----output checking---- ###
# output testing, sharing message to a channel for function message_share_v1
def test_message_share_channel_message_output():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'hi', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    assert resp.status_code == 200

    get_message = requests.get(url + 'channel/messages/v2', params = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'start': 0})
    get_message = json.loads(get_message.text)
    assert 'message shared_message: hi' in [message['message'] for message in get_message['messages']]


# output testing, sharing message to a dm for function message_share_v1
def test_message_share_dm_message_output():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': 'hi', 'channel_id': -1, 'dm_id': dm['dm_id']})
    assert resp.status_code == 200

    get_message = requests.get(url + 'dm/messages/v1', params = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'start': 0})
    get_message = json.loads(get_message.text)
    assert 'message shared_message: hi' in [message['message'] for message in get_message['messages']]
