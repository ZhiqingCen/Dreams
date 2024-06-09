'''
http test file for src/users_stats_v1
'''
from src.helper_func import extract_current_time
import requests
import json
from src import config
from src.error import ACCESS_ERROR, OK

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

###-----------------------------------------------------------###
### users_stats_v1(token) return {'dreams_stats': user_stats} ###
###-----------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function users_stats_v1
def test_users_stats_empty_token():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'users/stats/v1', params = {'token': ''})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function users_stats_v1
def test_users_stats_none_token():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'users/stats/v1', params = {'token': None})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function users_stats_v1
def test_users_stats_invalid_token_type():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'users/stats/v1', params = {'token': 123456789})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function users_stats_v1
def test_users_stats_token_not_exist():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'users/stats/v1', params = {'token': 'invalid_token'})
    assert resp.status_code == ACCESS_ERROR

### ----output checking---- ###
# user not in any channels, dms for function users_stats_v1
def test_users_stats_user_not_in_channels_dms():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.get(url + 'users/stats/v1', params = {'token': user_one['token']})
    assert resp.status_code == OK
    
    resp = json.loads(resp.text)
    assert resp['dreams_stats']['utilization_rate'] == 0

# all users joined channels/dms for function users_stats_v1
def test_users_stats_all_users_joined_channels_dms():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)

    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()

    timestamp = extract_current_time()

    resp = requests.get(url + 'users/stats/v1', params = {'token': user_one['token']})
    assert resp.status_code == OK

    resp = json.loads(resp.text)
    assert resp['dreams_stats'] == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': timestamp,}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': timestamp,}],
        'messages_exist': [{'num_messages_exist': 2, 'time_stamp': timestamp,}],
        'utilization_rate': 1.0,
    }

# half users joined channels/dms for function users_stats_v1
def test_users_stats_half_users_joined_channels_dms():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    requests.post(url + 'auth/register/v2', json = two)

    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    timestamp = extract_current_time()

    resp = requests.get(url + 'users/stats/v1', params = {'token': user_one['token']})
    assert resp.status_code == OK

    resp = json.loads(resp.text)
    assert resp["dreams_stats"] == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': timestamp,}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': timestamp,}],
        'messages_exist': [{'num_messages_exist': 1, 'time_stamp': timestamp,}],
        'utilization_rate': 0.5,
    }