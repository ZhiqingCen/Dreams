import requests
import pytest
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR, OK

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def register_users():
    requests.delete(config.url + 'clear/v1')

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address0@email.com',
        "password": "onetwothree",
        "name_first": "User0",
        "name_last": "GlobalOwner"
    })
    global_owner = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address1@email.com',
        "password": "onetwothree",
        "name_first": "User1",
        "name_last": "GroupOwner"
    })
    group_owner = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address2@email.com',
        "password": "onetwothree",
        "name_first": "User2",
        "name_last": "GlobalMember"
    })
    global_member = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address3@email.com',
        "password": "onetwothree",
        "name_first": "User3",
        "name_last": "GroupMember"
    })
    group_member = json.loads(r.text)

    unregistered_user = {'token': 4, 'auth_user_id': 4}

    return global_owner, group_owner, global_member, group_member, unregistered_user

@pytest.fixture
def create_channel(register_users):
    global_owner, group_owner, _, group_member, _ = register_users

    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': group_owner['token'],
        'name': 'Channel Name', 
        'is_public': True,
    })
    channel = json.loads(r.text)

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': group_owner['token'],
        'channel_id': channel['channel_id'], 
        'u_id': group_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': group_owner['token'],
        'channel_id': channel['channel_id'], 
        'u_id': global_owner['auth_user_id'],
    })

    return channel

@pytest.fixture
def create_dm(register_users):
    global_owner, group_owner, _, group_member, _ = register_users
    
    r = requests.post(config.url + 'dm/create/v1', json = {
        'token': group_owner['token'],
        'u_ids': [global_owner['auth_user_id'], group_member['auth_user_id']],
    })
    dm = json.loads(r.text)

    return dm

###-----------------------------------------------------------------------------------------------------------###
###                                        admin_remove Function Tests                                        ###
###-----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_admin_remove_user_token_not_global_owner(register_users):
    _, group_owner, global_member, group_member, _ = register_users
    
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': group_owner['token'],
        'u_id': group_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_member['token'],
        'u_id': group_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_remove_user_token_invalid(register_users): 
    _, _, global_member, _, unregistered_user = register_users
    
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': unregistered_user['token'],
        'u_id': global_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': None,
        'u_id': global_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_remove_user_token_already_removed(register_users):
    global_owner, _, global_member_to_owner, group_member, _ = register_users
    global_owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member_to_owner['auth_user_id'],
        'permission_id': global_owner_permission_id,
    })

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member_to_owner['auth_user_id'],
    })

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_member_to_owner['token'],
        'u_id': group_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_remove_only_global_owner(register_users):
    global_owner, _, _, _, _ = register_users

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_owner['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_admin_remove_user_u_id_invalid(register_users):
    global_owner, _, _, _, unregistered_user = register_users

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': unregistered_user['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': None,
    })
    assert r.status_code == INPUT_ERROR

def test_admin_remove_user_u_id_already_removed(register_users):
    global_owner, _, global_member, _, _ = register_users

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
    })
    
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

###-----------------###
### Action Checking ###
###-----------------###

def test_admin_remove_user_global_member(register_users, create_channel, create_dm): 
    global_owner, _, _, global_member, _ = register_users
    channel = create_channel
    dm = create_dm

    #Send messages to dm and channel
    r = requests.post(config.url + 'message/send/v2', json = {
        'token': global_member['token'],
        'channel_id': channel['channel_id'],
        'message': "hi",
    })

    r = requests.post(config.url + 'message/senddm/v1', json = {
        'token': global_member['token'],
        'dm_id': dm['dm_id'],
        'message': "hello",
    })

    #Remove user
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
    })

    #Verify that name is removed user
    r = requests.get(config.url + 'user/profile/v2', params = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
    })
    removed_user = json.loads(r.text)['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == "Removed user"

    #Verify that messages they have sent are removed user
    r = requests.get(config.url + 'search/v2', params = {
        'token': global_owner['token'],
        'query_str': f"u_id={global_member['auth_user_id']}",
    })
    user_messages = json.loads(r.text)

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    r = requests.post(config.url + 'auth/login/v2', json = {
        'email': "address3@email.com",
        'password': "onetwothree",
    })
    assert r.status_code == INPUT_ERROR

    #Verify that they are no longer in channel or dm
    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert global_member['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': global_owner['token'],
        'dm_id': dm['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert global_member['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

def test_admin_remove_user_global_member_channel_owner(register_users, create_channel, create_dm): 
    global_owner, channel_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm

    #Send messages to dm and channel
    r = requests.post(config.url + 'message/send/v2', json = {
        'token': channel_owner['token'],
        'channel_id': channel['channel_id'],
        'message': "hi",
    })

    r = requests.post(config.url + 'message/senddm/v1', json = {
        'token': channel_owner['token'],
        'dm_id': dm['dm_id'],
        'message': "hello",
    })

    #Remove user
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': channel_owner['auth_user_id'],
    })

    #Verify that name is removed user
    r = requests.get(config.url + 'user/profile/v2', params = {
        'token': global_owner['token'],
        'u_id': channel_owner['auth_user_id'],
    })
    removed_user = json.loads(r.text)['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == "Removed user"

    #Verify that messages they have sent are removed user
    r = requests.get(config.url + 'search/v2', params = {
        'token': global_owner['token'],
        'query_str': f"u_id={channel_owner['auth_user_id']}",
    })
    user_messages = json.loads(r.text)

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    r = requests.post(config.url + 'auth/login/v2', json = {
        'email': "address1@email.com",
        'password': "onetwothree",
    })
    assert r.status_code == INPUT_ERROR

    #Verify that they are no longer in channel or dm
    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': global_owner['token'],
        'dm_id': dm['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

def test_admin_remove_user_global_owner(register_users, create_channel, create_dm): 
    global_owner, group_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm
    owner_permission_id = 1

    #Send messages to dm and channel
    r = requests.post(config.url + 'message/send/v2', json = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'],
        'message': "hi",
    })

    r = requests.post(config.url + 'message/senddm/v1', json = {
        'token': global_owner['token'],
        'dm_id': dm['dm_id'],
        'message': "hello",
    })

    #change user permissions of group_owner to owner
    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': group_owner['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    #Remove user
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': group_owner['token'],
        'u_id': global_owner['auth_user_id'],
    })

    #Verify that name is removed user
    r = requests.get(config.url + 'user/profile/v2', params = {
        'token': group_owner['token'],
        'u_id': global_owner['auth_user_id'],
    })
    removed_user = json.loads(r.text)['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == "Removed user"

    #Verify that messages they have sent are removed user
    r = requests.get(config.url + 'search/v2', params = {
        'token': group_owner['token'],
        'query_str': f"u_id={global_owner['auth_user_id']}",
    })
    user_messages = json.loads(r.text)

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    r = requests.post(config.url + 'auth/login/v2', json = {
        'email': "address0@email.com",
        'password': "onetwothree",
    })
    assert r.status_code == INPUT_ERROR

    #Verify that they are no longer in channel or dm
    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': group_owner['token'],
        'channel_id': channel['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': group_owner['token'],
        'dm_id': dm['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

def test_admin_remove_token_user(register_users, create_channel, create_dm): 
    global_owner, group_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm
    owner_permission_id = 1

    #Send messages to dm and channel
    r = requests.post(config.url + 'message/send/v2', json = {
        'token': global_owner['token'],
        'channel_id': channel['channel_id'],
        'message': "hi",
    })

    r = requests.post(config.url + 'message/senddm/v1', json = {
        'token': global_owner['token'],
        'dm_id': dm['dm_id'],
        'message': "hello",
    })

    #change user permissions of group_owner to owner
    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': group_owner['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    #Remove user
    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_owner['auth_user_id'],
    })

    #Verify that name is removed user
    r = requests.get(config.url + 'user/profile/v2', params = {
        'token': group_owner['token'],
        'u_id': global_owner['auth_user_id'],
    })
    removed_user = json.loads(r.text)['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == "Removed user"

    #Verify that messages they have sent are removed user
    r = requests.get(config.url + 'search/v2', params = {
        'token': group_owner['token'],
        'query_str': f"u_id={global_owner['auth_user_id']}",
    })
    user_messages = json.loads(r.text)

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    r = requests.post(config.url + 'auth/login/v2', json = {
        'email': "address0@email.com",
        'password': "onetwothree",
    })
    assert r.status_code == INPUT_ERROR

    #Verify that they are no longer in channel or dm
    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': group_owner['token'],
        'channel_id': channel['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': group_owner['token'],
        'dm_id': dm['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

###----------------------------------------------------------------------------------------------------------------------------###
###                                        admin_change_user_permissions Function Tests                                        ###
###----------------------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_admin_change_permissions_token_not_global_owner(register_users):
    _, group_owner, global_member, group_member, _ = register_users
    owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': group_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': group_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_change_permissions_token_invalid(register_users):
    _, _, global_member, _, unregistered_user = register_users
    owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': unregistered_user['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': None,
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_change_permissions_token_removed_user(register_users):
    global_owner, _, global_member_to_owner, group_member, _ = register_users
    owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member_to_owner['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member_to_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member_to_owner['token'],
        'u_id': group_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_change_permissions_u_id_invalid(register_users):
    global_owner, _, _, _, unregistered_user = register_users
    owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': unregistered_user['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': None,
        'permission_id': owner_permission_id,
    })
    assert r.status_code == INPUT_ERROR

def test_admin_change_permissions_u_id_only_global_owner(register_users):
    global_owner, _, _, _, _ = register_users
    member_permission_id = 2

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': member_permission_id,
    })
    assert r.status_code == INPUT_ERROR

def test_admin_change_permissions_u_id_removed_user(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1

    r = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    assert r.status_code == INPUT_ERROR

def test_admin_change_permissions_permission_id_invalid(register_users):
    global_owner, _, global_member, _, _ = register_users
    invalid_permission_id = 0

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': invalid_permission_id,
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': None,
    })
    assert r.status_code == INPUT_ERROR

###-----------------###
### Action Checking ###
###-----------------###

def test_admin_change_permissions_to_owner(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': member_permission_id,
    })
    assert r.status_code == OK

def test_admin_change_permissions_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': member_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': member_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_change_permissions_owner_to_owner(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })
    r.status_code == OK

def test_admin_change_permissions_member_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    member_permission_id = 2

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': member_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': member_permission_id,
    })
    assert r.status_code == ACCESS_ERROR

def test_admin_change_permissions_self_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_owner['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': owner_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': global_member['auth_user_id'],
        'permission_id': member_permission_id,
    })

    r = requests.post(config.url + 'admin/userpermission/change/v1', json = {
        'token': global_member['token'],
        'u_id': global_owner['auth_user_id'],
        'permission_id': member_permission_id,
    })
    assert r.status_code == ACCESS_ERROR