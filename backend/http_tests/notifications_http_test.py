'''
http test file for notifications/get/v1
'''
import requests
import json
from src import config
from src.error import ACCESS_ERROR

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

###------------------------------------------------------###
### notifications_get_v1(token) return { notifications } ###
###------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function notifications_get_v1
def test_notifications_get_empty_token():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'notifications/get/v1', params = {'token': ''})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter None input token for function notifications_get_v1
def test_notifications_get_none_token():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'notifications/get/v1', params = {'token': None})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter string input token for function notifications_get_v1
def test_notifications_get_invalid_token_type():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'notifications/get/v1', params = {'token': 123456789})
    assert resp.status_code == ACCESS_ERROR

# input of none existing token for function notifications_get_v1
def test_notifications_get_token_not_exist():
    requests.delete(url + 'clear/v1')
    resp = requests.get(url + 'notifications/get/v1', params = {'token': 'invalid_token'})
    assert resp.status_code == ACCESS_ERROR

### ----output checking---- ###
# ------- tag ------- #
# channel send_message without tag
def test_notifications_get_send_message_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# channel send_message tag member
def test_notifications_get_send_message_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    m = f"@{user_three_detail['user']['handle_str']} message"
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': m})
    message1 = json.loads(message1.text)

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} tagged you in channelONE: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]

# channel edit_message without tag
def test_notifications_get_edit_message_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    requests.put(url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': 'edit message'})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# channel edit_message tag member
def test_notifications_get_edit_message_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    m = f"@{user_three_detail['user']['handle_str']} message"
    requests.put(url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': message1['message_id'], 'message': m})

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} tagged you in channelONE: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]

# channel share_message without tag
def test_notifications_get_share_message_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': 'hi', 'channel_id': channel1['channel_id'], 'dm_id': -1})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# channel share_message tag member
def test_notifications_get_share_message_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)
    m = f"@{user_three_detail['user']['handle_str']} message"
    requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': message1['message_id'], 'message': m, 'channel_id': channel1['channel_id'], 'dm_id': -1})

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    m = f"message shared_message: @{user_three_detail['user']['handle_str']} message"
    message = f"{user_one_detail['user']['handle_str']} tagged you in channelONE: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]

# dm send_message without tag
def test_notifications_get_send_dm_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# dm send_message tag member
def test_notifications_get_send_dm_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user_two_detail = requests.get(url + 'user/profile/v2', params = {'token': user_two['token'], 'u_id': user_two['auth_user_id']})
    user_two_detail = json.loads(user_two_detail.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    m = f"@{user_two_detail['user']['handle_str']} message"
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': m})
    dm_message = dm_message.json()

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_two['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} tagged you in userone, usertwo: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]

# dm edit_message without tag
def test_notifications_get_edit_dm_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    requests.put(url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': dm_message['message_id'], 'message': 'edit message'})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# dm edit_message tag member
def test_notifications_get_edit_dm_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user_two_detail = requests.get(url + 'user/profile/v2', params = {'token': user_two['token'], 'u_id': user_two['auth_user_id']})
    user_two_detail = json.loads(user_two_detail.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': "message"})
    dm_message = dm_message.json()
    m = f"@{user_two_detail['user']['handle_str']} message"
    requests.put(url + 'message/edit/v2', json = {'token': user_one['token'], 'message_id': dm_message['message_id'], 'message': m})

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_two['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} tagged you in userone, usertwo: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]

# dm share_message without tag
def test_notifications_get_share_dm_without_tag():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': 'message'})
    dm_message = dm_message.json()
    requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': 'hi', 'channel_id': -1, 'dm_id': dm['dm_id']})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# dm share_message tag member
def test_notifications_get_share_dm_tag_member():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user_two_detail = requests.get(url + 'user/profile/v2', params = {'token': user_two['token'], 'u_id': user_two['auth_user_id']})
    user_two_detail = json.loads(user_two_detail.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': "message"})
    dm_message = dm_message.json()
    m = f"@{user_two_detail['user']['handle_str']} message"
    requests.post(url + 'message/share/v1', json = {'token': user_one['token'], 'og_message_id': dm_message['message_id'], 'message': m, 'channel_id': -1, 'dm_id': dm['dm_id']})

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_two['token']})
    assert resp.status_code == 200
    m = f"message shared_message: @{user_two_detail['user']['handle_str']} message"
    message = f"{user_one_detail['user']['handle_str']} tagged you in userone, usertwo: {m[0:20]}"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]

# ------- invite ------- #
# channel_invite
def test_notifications_get_channel_invite():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/invite/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'u_id': user_three['auth_user_id']})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} added you to channelONE"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]

# dm_invite
def test_notifications_get_dm_invite():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user_one_detail = requests.get(url + 'user/profile/v2', params = {'token': user_one['token'], 'u_id': user_one['auth_user_id']})
    user_one_detail = json.loads(user_one_detail.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    requests.post(url + 'dm/invite/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'u_id': user_three['auth_user_id']})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    message = f"{user_one_detail['user']['handle_str']} added you to userone, usertwo"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]

# ------- react ------- #
# react to channel message
def test_notifications_get_react_channel_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    requests.post(url + 'message/react/v1', json = {'token': user_three['token'], 'message_id': message1['message_id'], 'react_id': 1})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    message = f"{user_three_detail['user']['handle_str']} reacted to your message in channelONE"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]

# react to dm message
def test_notifications_get_react_dm_message():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user_two_detail = requests.get(url + 'user/profile/v2', params = {'token': user_two['token'], 'u_id': user_two['auth_user_id']})
    user_two_detail = json.loads(user_two_detail.text)
    dm = requests.post(url + 'dm/create/v1', json = {'token': user_one['token'], 'u_ids': [user_two['auth_user_id']]})
    dm = json.loads(dm.text)
    dm_message = requests.post(url + 'message/senddm/v1', json = {'token': user_one['token'], 'dm_id': dm['dm_id'], 'message': "message"})
    dm_message = dm_message.json()

    requests.post(url + 'message/react/v1', json = {'token': user_two['token'], 'message_id': dm_message['message_id'], 'react_id': 1})
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    message = f"{user_two_detail['user']['handle_str']} reacted to your message in userone, usertwo"
    resp = json.loads(resp.text)
    assert resp['notifications'] == [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]

# ------- other output ------- #
def test_notifications_no_notification_output():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})

    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200
    resp = json.loads(resp.text)
    assert resp['notifications'] == []

# only output 20 most recent tag notifications
def test_notifications_tag_more_than_twenty():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    m = f"@{user_three_detail['user']['handle_str']} message"

    for _ in range(21):
        requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': m})
    
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert len(resp['notifications']) == 20

# only output 20 most recent invite notifications
def test_notifications_invite_more_than_twenty():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)

    for _ in range(21):
        requests.post(url + 'channel/invite/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'u_id': user_three['auth_user_id']})
        requests.post(url + 'channel/leave/v1', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_three['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert len(resp['notifications']) == 20

# only output 20 most recent react notifications
def test_notifications_react_more_than_twenty():
    requests.delete(url + 'clear/v1')
    user1 = requests.post(url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user3 = requests.post(url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    user_three_detail = requests.get(url + 'user/profile/v2', params = {'token': user_three['token'], 'u_id': user_three['auth_user_id']})
    user_three_detail = json.loads(user_three_detail.text)
    channel1 = requests.post(url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    channel1 = json.loads(channel1.text)
    requests.post(url + 'channel/join/v2', json = {'token': user_three['token'], 'channel_id': channel1['channel_id']})
    message1 = requests.post(url + 'message/send/v2', json = {'token': user_one['token'], 'channel_id': channel1['channel_id'], 'message': 'message'})
    message1 = json.loads(message1.text)

    for _ in range(21):
        requests.post(url + 'message/react/v1', json = {'token': user_three['token'], 'message_id': message1['message_id'], 'react_id': 1})
        requests.post(url + 'message/unreact/v1', json = {'token': user_three['token'], 'message_id': message1['message_id'], 'react_id': 1})
    
    resp = requests.get(url + 'notifications/get/v1', params = {'token': user_one['token']})
    assert resp.status_code == 200

    resp = json.loads(resp.text)
    assert len(resp['notifications']) == 20