import pytest
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

###------------###
### Test Setup ###
###------------###

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
        "name_last": "Owner"
    })
    channel_owner = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address2@email.com',
        "password": "onetwothree",
        "name_first": "User2",
        "name_last": "Member"
    })
    member = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address3@email.com',
        "password": "onetwothree",
        "name_first": "User3",
        "name_last": "NotMember"
    })
    not_member = json.loads(r.text)

    unregistered_user = {'token': not_member['token'] + "abcde", 'auth_user_id': not_member['auth_user_id'] + 1}

    return global_owner, channel_owner, member, not_member, unregistered_user

@pytest.fixture
def create_channel(register_users):
    _, channel_owner, _, _, _ = register_users

    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': channel_owner['token'],
        'name': 'Channel Public', 
        'is_public': True,
    })
    channel_public = json.loads(r.text)

    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': channel_owner['token'],
        'name': 'Channel Private', 
        'is_public': False,
    })
    channel_private = json.loads(r.text)

    nonexistent_channel = {'channel_id': 2}

    return channel_public, channel_private, nonexistent_channel

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_join Function Tests                                        ###
###-----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_channel_join_invalid_token(register_users, create_channel):
    _, _, _, _, unregistered_user = register_users
    channel_public, _, _ = create_channel
    
    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': unregistered_user['token'],
        'channel_id': channel_public['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_join_unauthorised_member_private(register_users, create_channel):
    _, _, _, user_not_member, _ = register_users
    _, channel_private, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_not_member['token'],
        'channel_id': channel_private['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_join_token_is_member(register_users, create_channel):
    _, user_owner, user_member, _, _ = register_users
    channel_public, channel_private, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_private['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_private['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_join_invalid_channel_id(register_users, create_channel):
    _,user_owner, _, _, _ = register_users
    _, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'], 
    })
    assert r.status_code == INPUT_ERROR

def test_channel_join_none_input(register_users, create_channel):
    _,_,_,user_not_member,_ = register_users
    _, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': None,
        'channel_id': None, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': None,
        'channel_id': nonexistent_channel['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_not_member['token'],
        'channel_id': None, 
    })
    assert r.status_code == INPUT_ERROR

###-----------------###
### Action Checking ###
###-----------------###

def test_channel_join_global_owner_public(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_join_global_owner_private(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    _, channel_private, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_private['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_private['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_join_member_public(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _,_ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_join_return_value(register_users, create_channel):
    _,_,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })
    output = json.loads(r.text)
    assert output == {}

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_addowner Function Tests                                    ###
###-----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###
def test_channel_addowner_invalid_token(register_users, create_channel):
    _,_,user_member,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': unregistered_user['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_addowner_token_not_member(register_users, create_channel):
    _,_,user_member,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_not_member1['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_addowner_token_not_owner(register_users, create_channel):
    _,_, user_member,user_not_member,_ = register_users
    channel_public, _, _  = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_not_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_addowner_invalid_channel_id(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    _, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_addowner_invalid_u_id(register_users, create_channel):
    _,user_owner,_,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': unregistered_user['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_addowner_already_owner(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_addowner_none_input(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': None,
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': None,
        'channel_id': nonexistent_channel['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': None, 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': None,
    })
    assert r.status_code == INPUT_ERROR

###-----------------###
### Action Checking ###
###-----------------###

def test_channel_addowner_member_owner_is_auth(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_addowner_member_global_owner_is_auth(register_users, create_channel):
    user_global_owner,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_addowner_not_member_owner_is_auth():
    pass

def test_channel_addowner_not_member_global_owner_is_auth():
    pass

def test_channel_addowner_return_value(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    output = json.loads(r.text)
    assert output == {}

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_removeowner Function Tests                                 ###
###-----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_channel_removeowner_invalid_token(register_users, create_channel):
    _,_,user_member,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': unregistered_user['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_removeowner_token_not_member(register_users, create_channel):
    _,_,user_member,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_not_member1['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_removeowner_token_not_owner(register_users, create_channel):
    _,_, user_member,user_not_member,_ = register_users
    channel_public, _, _  = create_channel

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_member['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_not_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_channel_removeowner_invalid_channel_id(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    _, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_removeowner_invalid_u_id(register_users, create_channel):
    _,user_owner,_,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': unregistered_user['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_removeowner_u_id_not_member(register_users, create_channel):
    _,user_owner,_,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_removeowner_u_id_not_owner(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_removeowner_u_id_only_owner(register_users, create_channel):
    _,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_owner['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_removeowner_none_input(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': None,
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': None,
        'channel_id': nonexistent_channel['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR
    
    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': None, 
        'u_id': user_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': None,
    })
    assert r.status_code == INPUT_ERROR

###-----------------###
### Action Checking ###
###-----------------###
def test_channel_removeowner_owner_is_auth(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_member['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_removeowner_global_owner_is_auth(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_owner['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_global_owner['token'],
        'channel_id': channel_public['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_removeowner_return_value(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    r = requests.post(config.url + 'channel/addowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/removeowner/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_public['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })
    output = json.loads(r.text)
    assert output == {}

