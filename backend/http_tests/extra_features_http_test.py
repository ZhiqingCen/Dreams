'''
http test file for src/extra_features
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

###---------------------------------------------------###
### channel_rename(token, name, channel_id) return {} ###
###---------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function group_rename
def test_group_rename_empty_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': '', 'name': 'new_channel', 'channel_id': channel1['channel_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function group_rename
def test_group_rename_none_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': None, 'name': 'new_channel', 'channel_id': channel1['channel_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function group_rename
def test_group_rename_invalid_token_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': 123456789, 'name': 'new_channel', 'channel_id': channel1['channel_id']})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function group_rename
def test_group_rename_token_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': 'invalid_token', 'name': 'new_channel', 'channel_id': channel1['channel_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input name for function group_rename
def test_group_rename_none_name():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': None, 'channel_id': channel1['channel_id']})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input name for function group_rename
def test_group_rename_invalid_name_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 123456789, 'channel_id': channel1['channel_id']})
    assert resp.status_code == INPUT_ERROR

# input of name exceed 20 characters for function group_rename
def test_group_rename_name_too_long():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 'a'*21, 'channel_id': channel1['channel_id']})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input group_id for function group_rename
def test_group_rename_none_group_id():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 'new_name', 'channel_id': None})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input group_id for function group_rename
def test_group_rename_invalid_group_id_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 'new_name', 'channel_id': 'invalid_channel_id'})
    assert resp.status_code == INPUT_ERROR

# input of none existing group_id for function group_rename
def test_group_rename_group_id_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 'new_name', 'channel_id': 123456789})
    assert resp.status_code == INPUT_ERROR

# non channel owner trying to rename channel for function group_rename
def test_group_rename_non_channel_owner():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_three['token'], 'name': 'new_name', 'channel_id': channel1['channel_id']})
    assert resp.status_code == ACCESS_ERROR

### ----output checking---- ###
# channel owner trying to rename channel for function group_rename
def test_group_rename_change_channel_name():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    resp = requests.post(config.url + 'channel/rename/v1', json = {'token': user_one['token'], 'name': 'new_name', 'channel_id': channel1['channel_id']})
    assert resp.status_code == OK

    get_data = requests.get(config.url + 'channel/details/v2', params = {'token': user_one['token'], 'channel_id': channel1['channel_id']})
    get_data = json.loads(get_data.text)
    assert get_data['name'] == 'new_name'


###---------------------------------------------------###
### dm_rename(token, name, channel_id) return {} ###
###---------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function group_rename
def test_dm_rename_empty_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': '', 'name': 'new_dm', 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function group_rename
def test_dm_rename_none_token():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': None, 'name': 'new_dm', 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function group_rename
def test_dm_rename_invalid_token_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': 123456789, 'name': 'new_dm', 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function group_rename
def test_dm_rename_token_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': 'invalid_token', 'name': 'new_cdm', 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input name for function group_rename
def test_dm_rename_none_name():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': None, 'dm_id': dm['dm_id']})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input name for function group_rename
def test_dm_rename_invalid_name_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 123456789, 'dm_id': dm['dm_id']})
    assert resp.status_code == INPUT_ERROR

# input of name exceed 20 characters for function group_rename
def test_dm_rename_name_too_long():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 'a'*21, 'dm_id': dm['dm_id']})
    assert resp.status_code == INPUT_ERROR

# invalid parameter None input group_id for function group_rename
def test_dm_rename_none_group_id():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 'new_dm', 'dm_id': None})
    assert resp.status_code == INPUT_ERROR

# invalid parameter string input group_id for function group_rename
def test_dm_rename_invalid_group_id_type():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 'new_dm', 'dm_id': 'invalid_channel_id'})
    assert resp.status_code == INPUT_ERROR

# input of none existing group_id for function group_rename
def test_dm_rename_group_id_not_exist():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 'new_dm', 'dm_id': 123456789})
    assert resp.status_code == INPUT_ERROR

# non dm owner trying to rename dm for function group_rename
def test_group_rename_non_dm_owner():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_two['token'], 'name': 'new_dm', 'dm_id': dm['dm_id']})
    assert resp.status_code == ACCESS_ERROR

### ----output checking---- ###
# dm owner trying to rename dm for function group_rename
def test_group_rename_change_dm_name():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    resp = requests.post(config.url + 'dm/rename/v1', json = {'token': user_one['token'], 'name': 'new_name', 'dm_id': dm['dm_id']})
    assert resp.status_code == OK

    get_data = requests.get(config.url + 'dm/details/v1', params = {'token': user_one['token'], 'dm_id': dm['dm_id']})
    get_data = json.loads(get_data.text)
    assert get_data['name'] == 'new_name'