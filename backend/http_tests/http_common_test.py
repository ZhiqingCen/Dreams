import pytest
import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

##--------------------------------------------------------------------------------------------------------------###
###                                        invite_to_group Function Tests                                        ###
###--------------------------------------------------------------------------------------------------------------###

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
        "name_last": "NotMember1"
    })
    not_member1 = json.loads(r.text)

    r = requests.post(config.url + "auth/register/v2", json = {
        "email": 'address4@email.com',
        "password": "onetwothree",
        "name_first": "User4",
        "name_last": "NotMember2"
    })
    not_member2 = json.loads(r.text)

    unregistered_user = {'token': 5, 'auth_user_id': 5}

    return global_owner, channel_owner, member, not_member1, not_member2, unregistered_user

@pytest.fixture
def create_channel(register_users):
    _, channel_owner, _, _, _, _ = register_users

    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': channel_owner['token'],
        'name': 'Channel 1', 
        'is_public': True,
    })
    channel_public = json.loads(r.text)

    nonexistent_channel = {'channel_id': 2}

    return channel_public, nonexistent_channel

@pytest.fixture
def create_dm(register_users):
    _, dm_owner, dm_member, _, _, _ = register_users

    r = requests.post(config.url + 'dm/create/v1', json = {
        'token': dm_owner['token'],
        'u_ids': [dm_member['auth_user_id']], 
    })
    dm = json.loads(r.text)

    nonexistent_dm = {'dm_id': 2}

    return dm, nonexistent_dm

###--------------------------###
### Error Checking - Channel ###
###--------------------------###
def test_channel_invite_invalid_token(register_users, create_channel):
    _, _, _, user_not_member1, user_not_member2, unregistered_user = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_not_member1['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member2['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': unregistered_user['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member2['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR
    
def test_channel_invite_invalid_group_id(register_users, create_channel):
    _,user_owner, _, user_not_member1, _, _ = register_users
    _, nonexistent_channel = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_invite_invalid_u_id(register_users, create_channel):
    _,user_owner, _, user_channel_member, _, unregistered_user = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': unregistered_user['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_channel_member['token'],
        'channel_id': channel_one['channel_id'], 
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_channel_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_channel_invite_none_input(register_users, create_channel):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel 

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': None,
        'channel_id': None, 
        'u_id': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': None,
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': None, 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': None,
    })
    assert r.status_code == INPUT_ERROR

###---------------------###
### Error Checking - Dm ###
###---------------------###

def test_dm_invite_invalid_token(register_users, create_dm):
    _, _, _, user_not_member1, user_not_member2, unregistered_user = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_not_member1['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_not_member2['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': unregistered_user['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_dm_invite_invalid_group_id(register_users, create_dm):
    _,user_owner, _, user_not_member1, _, _ = register_users
    _, nonexistent_dm = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': nonexistent_dm['dm_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_dm_invite_invalid_u_id(register_users, create_dm):
    _,user_owner, user_dm_member, _, _, unregistered_user = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': unregistered_user['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_dm_member['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

def test_dm_invite_none_input(register_users, create_dm):
    _,user_owner, _, user_not_member1, _, _ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': None,
        'dm_id': None, 
        'u_id': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': None,
        'dm_id': dm_one['dm_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': None, 
        'u_id': user_not_member1['auth_user_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': None,
    })
    assert r.status_code == INPUT_ERROR

###----------------------------------###
### Output/Action Checking - Channel ###
###----------------------------------###
def test_channel_invite_auth_is_owner(register_users, create_channel):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel
    
    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_not_member1['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_invite_global_owner(register_users, create_channel):
    user_global_owner, user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_invite_auth_is_member(register_users, create_channel):
    _,user_owner, _, user_member, user_not_member, _ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_member['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    channel_content = json.loads(r.text)
    assert user_not_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_invite_second_channel(register_users, create_channel):
    _,user_owner, _, user_member, _, _ = register_users
    channel_one, _ = create_channel
    
    r = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_owner['token'],
        'name': 'Channel 2', 
        'is_public': True,
    })
    channel_two = json.loads(r.text)

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    channel_content1 = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content1['all_members']]

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_two['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_two['channel_id'],
    })
    channel_content2 = json.loads(r.text)
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content2['all_members']]
    
def test_invite_to_group_return_type(register_users, create_channel):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })
    output = json.loads(r.text)
    assert output == {}

###-----------------------------###
### Output/Action Checking - Dm ###
###-----------------------------###
def test_dm_invite_auth_is_owner(register_users, create_dm):
    _,user_owner, _, user_not_member1, _, _ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_not_member1['auth_user_id'],
    })

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert user_not_member1['auth_user_id'] in [member['u_id'] for member in dm_content['members']]

def test_dm_invite_auth_is_member(register_users, create_dm):
    _,user_owner, _, user_member, user_not_member, _ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_member['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_not_member['auth_user_id'],
    })

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    dm_content = json.loads(r.text)
    assert user_not_member['auth_user_id'] in [member['u_id'] for member in dm_content['members']]

def test_dm_invite_second_dm(register_users, create_dm):
    _,user_owner, user_member1, user_member2, _, _ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/create/v1', json = {
        'token': user_owner['token'],
        'u_ids': [user_member2['auth_user_id']],
    })
    dm_two = json.loads(r.text)

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    dm_content1 = json.loads(r.text)
    assert user_member1['auth_user_id'] in [member['u_id'] for member in dm_content1['members']]

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_two['dm_id'], 
        'u_id': user_member1['auth_user_id'],
    })

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_two['dm_id'],
    })
    dm_content2 = json.loads(r.text)
    assert user_member1['auth_user_id'] in [member['u_id'] for member in dm_content2['members']]
    
###------------------------------------------------------------------------------------------------------------###
###                                        group_details Function Tests                                        ###
###------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_group_details_invalid_token(register_users, create_channel, create_dm):
    _, _, _, _, _, unregistered_user = register_users
    channel_one, _ = create_channel
    dm_one, _ = create_dm

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': unregistered_user['token'],
        'channel_id': channel_one['channel_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': unregistered_user['token'],
        'dm_id': dm_one['dm_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_group_details_token_not_member(register_users, create_channel, create_dm):
    _, _, _, _, user_not_member, _ = register_users
    channel_one, _ = create_channel
    dm_one, _ = create_dm

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_not_member['token'],
        'channel_id': channel_one['channel_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_not_member['token'],
        'dm_id': dm_one['dm_id'],
    })
    assert r.status_code == ACCESS_ERROR

def test_group_details_invalid_group_id(register_users, create_channel, create_dm):
    _,user_owner, _, _, _, _ = register_users
    _, nonexistent_channel = create_channel
    _, nonexistent_dm = create_dm

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'],
    })
    assert r.status_code == INPUT_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': nonexistent_dm['dm_id'],
    })
    assert r.status_code == INPUT_ERROR
    
def test_group_details_none_input(register_users, create_channel, create_dm):
    _,user_owner,_,_,_,_ = register_users
    _, nonexistent_channel = create_channel
    _, nonexistent_dm = create_dm

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': None,
        'channel_id': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': None,
        'dm_id': None,
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': None,
        'channel_id': nonexistent_channel['channel_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': None,
        'dm_id': nonexistent_dm['dm_id'],
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': None,
    })
    assert r.status_code == INPUT_ERROR

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': None,
    })
    assert r.status_code == INPUT_ERROR

###---------------------------###
### Output Checking - Channel ###
###---------------------------###

def test_channel_details_global_owner_is_auth(register_users, create_channel):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_global_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_global_owner['auth_user_id'], 'name_first': 'User0', 'name_last': 'GlobalOwner',}, {'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_global_owner['auth_user_id'], 'name_first': 'User0', 'name_last': 'GlobalOwner',}, {'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
    }

def test_channel_details_owner_is_only_member(register_users, create_channel):
    _, user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
    }

def test_channel_details_owner_is_auth(register_users, create_channel):
    _, user_owner, user_member, _, _, _ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',},
                         {'u_id': user_member['auth_user_id'], 'name_first': 'User2', 'name_last': 'Member',},   
        ],
    }

def test_channel_details_member_is_auth(register_users, create_channel):
    _,user_owner,user_member,_,_,_ = register_users
    channel_one, _ = create_channel 

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_member['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',},
                         {'u_id': user_member['auth_user_id'], 'name_first': 'User2', 'name_last': 'Member',},   
        ],
    } 

###----------------------###
### Output Checking - Dm ###
###----------------------###

def test_dm_details_owner_is_only_member(register_users):
    _, user_owner, _, _, _, _ = register_users

    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_owner["token"],
        "u_ids": [],
    })
    dm_one = json.loads(r.text)

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "user1owner", 
        'members': [{'u_id': user_owner['auth_user_id'], 'email': 'address1@email.com','name_first': 'User1', 'name_last': 'Owner','handle_str': 'user1owner',},]
    }

def test_dm_details_owner_is_auth(register_users, create_dm):
    _, user_owner, user_member, _, _, _ = register_users
    dm_one, _ = create_dm

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "user1owner, user2member", 
        'members' : [{'u_id': user_owner['auth_user_id'], 'email': 'address1@email.com','name_first': 'User1', 'name_last': 'Owner','handle_str': 'user1owner',},
                     {'u_id': user_member['auth_user_id'], 'email': 'address2@email.com', 'name_first': 'User2', 'name_last': 'Member','handle_str': 'user2member',},   
        ],
    }

def test_dm_details_member_is_auth(register_users, create_dm):
    _,user_owner,user_member,_,_,_ = register_users
    dm_one, _ = create_dm

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_member['token'],
        'dm_id': dm_one['dm_id'],
    })
    details = json.loads(r.text)
    assert details == {
        'name': "user1owner, user2member", 
        'members' : [{'u_id': user_owner['auth_user_id'], 'email': 'address1@email.com','name_first': 'User1', 'name_last': 'Owner','handle_str': 'user1owner',},
                     {'u_id': user_member['auth_user_id'], 'email': 'address2@email.com', 'name_first': 'User2', 'name_last': 'Member','handle_str': 'user2member',},   
        ],
    }

###----------------------------------------------------------------------------------------------------------###
###                                        leave_group Function Tests                                        ###
###----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

def test_leave_group_invalid_token(register_users, create_channel, create_dm):
    _, _, _, _, user_not_member, unregistered_user = register_users
    channel_one, _ = create_channel
    dm_one, _ = create_dm

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': unregistered_user['token'],
        'channel_id': channel_one['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_not_member['token'],
        'channel_id': channel_one['channel_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': unregistered_user['token'],
        'dm_id': dm_one['dm_id'], 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_not_member['token'],
        'dm_id': dm_one['dm_id'], 
    })
    assert r.status_code == ACCESS_ERROR
 
def test_leave_group_invalid_group_id(register_users, create_channel, create_dm):
    _,user_owner, _, _, _, _ = register_users
    _, nonexistent_channel = create_channel
    _, nonexistent_dm = create_dm

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_owner['token'],
        'channel_id': nonexistent_channel['channel_id'], 
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_owner['token'],
        'dm_id': nonexistent_dm['dm_id'], 
    })
    assert r.status_code == INPUT_ERROR
    
def test_leave_group_none_input(register_users, create_channel, create_dm):
    _,user_owner,_,_,_,_ = register_users
    _, nonexistent_channel = create_channel
    _, nonexistent_dm = create_dm

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': None,
        'channel_id': None, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': None,
        'channel_id': nonexistent_channel, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': None,
        'dm_id': None, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': None,
        'dm_id': nonexistent_dm, 
    })
    assert r.status_code == ACCESS_ERROR

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_owner['token'],
        'channel_id': None, 
    })
    assert r.status_code == INPUT_ERROR

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_owner['token'],
        'dm_id': None, 
    })
    assert r.status_code == INPUT_ERROR

###---------------------------###
### Action Checking - Channel ###
###---------------------------###

def test_leave_group_channel_member(register_users, create_channel):
    _,user_owner,_,user_member,_,_ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_member['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_member['token'],
        'channel_id': channel_one['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert user_member['auth_user_id'] not in [member['u_id'] for member in details['all_members']]

def test_leave_group_channel_global_owner(register_users, create_channel):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/invite/v2', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_one['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in details['all_members']]
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in details['owner_members']]

def test_leave_group_channel_owner(register_users, create_channel):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
    })

    r = requests.post(config.url + 'channel/join/v2', json = {
        'token': user_global_owner['token'],
        'channel_id': channel_one['channel_id'], 
    })

    r = requests.get(config.url + 'channel/details/v2', params = {
        'token': user_global_owner['token'],
        'channel_id': channel_one['channel_id'],
    })
    details = json.loads(r.text)
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in details['all_members']]
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in details['owner_members']]

def test_leave_group_channel_return_type(register_users, create_channel):
    _,user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel

    r = requests.post(config.url + 'channel/leave/v1', json = {
        'token': user_owner['token'],
        'channel_id': channel_one['channel_id'], 
    })
    output = json.loads(r.text)
    assert output == {}

###----------------------###
### Action Checking - Dm ###
###----------------------###

def test_leave_group_dm_member(register_users, create_dm):
    _,user_owner, user_member,_,_,_ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_member['token'],
        'dm_id': dm_one['dm_id'], 
    })

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    details = json.loads(r.text)
    assert user_member['auth_user_id'] not in [member['u_id'] for member in details['members']]

def test_leave_group_dm_global_owner(register_users, create_dm):
    user_global_owner,user_owner,_,_,_,_ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/invite/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
        'u_id': user_global_owner['auth_user_id'],
    })

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_global_owner['token'],
        'dm_id': dm_one['dm_id'], 
    })

    r = requests.get(config.url + 'dm/details/v1', params = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'],
    })
    details = json.loads(r.text)
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in details['members']]

def test_leave_group_dm_owner(register_users, create_dm):
    _,user_owner,_,_,_,_ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
    })
    
    r = requests.get(config.url + 'dm/list/v1', params = {
        'token': user_owner['token'],
    })
    dm_list = json.loads(r.text)['dms']
    assert not dm_list

def test_leave_group_dm_return_type(register_users, create_dm):
    _,user_owner, _, _, _, _ = register_users
    dm_one, _ = create_dm

    r = requests.post(config.url + 'dm/leave/v1', json = {
        'token': user_owner['token'],
        'dm_id': dm_one['dm_id'], 
    })
    output = json.loads(r.text)
    assert output == {}

###----------------------------------------------------------------------------------------------------------###
###                                        send_group_message Function Tests                                       ###
###----------------------------------------------------------------------------------------------------------###

###-------------###
### Test Set Up ###
###-------------###

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

@pytest.fixture
def register_users2(): 
    '''
    Register users using auth/register/v2 and return the outputs, a dictionaries 
    containing keys 'token' and 'auth_user_id'
    '''
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


# ------------------------------- #
# -- message/senddm/v1 testing -- #
# ------------------------------- #   

def test_send_group_message_dm(register_users2):
    '''
    Check the output of message/senddm/v1 by creating a group and sending a 
    message in that group. Check the message has been sucessfully sent using
    dm/messages/v1
    '''
    user_one, user_two, user_three = register_users2
    
    # Create a dm and send a message in that dm
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()
    
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
    
    # Check output of message/senddm/v1
    assert "message_id" in resp.json()
    
    # Extract messages and check sent message exists in the database
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
    
    assert "hi" in [message['message'] for message in message_output['messages']]
 
   
def test_send_group_message_channel(register_users2):
    '''
    Create a channel and send a message in that channel, then check that a member
    of the channel can view the message sent.
    '''
    user_one, _, _ = register_users2
    
    # Create a channel and send a message in that channel
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_one["token"],
        "name": "Channel",
        "is_public": False
    })
    new_chan = r.json()
    
    requests.post(config.url + "message/send/v2", json = {
        "token": user_one["token"],
        "channel_id": new_chan['channel_id'],
        "message": "hi"
    })
    
    # Extract the messages from new_chan
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": new_chan['channel_id'],
        "start": 0
    })
    
    message_output =  resp.json()
    
    # check that new message is in channel messages.
    assert "hi" in [message['message'] for message in message_output['messages']]     
        
def test_send_group_message_invalid_dm_id(register_users2):
    '''
    Test access errors by checking that a user who enters an invalid DM ID or an
    DM ID of a group they arent a member of recieves an AccessError when they 
    attempt to send a message to that DM.
    '''
    user_one, user_two, user_three = register_users2
    
    # Create a DM containing user_one and user_two.
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    # Have user_three attempt to send a message to the DM they are not a member of.
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_three["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
    # Confirm AccessError raised
    assert resp.status_code == ACCESS_ERROR   
    
    # Check and INPUT_ERROR is raised when an invalid DM ID is given.
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": 987654321,
        "message": "hi"
    })
    assert resp.status_code == ACCESS_ERROR
    
def test_send_group_message_message_too_long(register_users2):
    '''
    Send a message in a dm which is the max length and check the message has 
    been sent. Then try to send a message which is greater than max length and 
    check that an input error is given.
    '''
    MAX_LEN = 1000

    user_one, user_two, _ = register_users2
    
    # Create a dm, then send a max length message in that dm.
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "a" * MAX_LEN
    })

    # Extract the message sent
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    
    message_output = resp.json()
    
    # Check message has been sent
    assert "a" * 1000 in [message['message'] for message in message_output['messages']]

    # Check message not sent if greater than max length
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "a" * (MAX_LEN + 1)
    })
    
    assert resp.status_code == INPUT_ERROR
  
def test_send_group_message_message_empty(register_users2):
    '''
    Check that an input error is raised when an empty message is sent
    '''
    user_one, user_two, _ = register_users2
   
    # Create dm and send empty message in that dm
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": ""
    })
    
    # Confirm that an input error is raised.
    assert resp.status_code == INPUT_ERROR

# ------------------------------------- #
# channels/list/v2 & dm/list/v1 testing #
# ------------------------------------- #  

## Testing list_groups output ##
def test_list_groups_dms(register_users2):
    user_one, user_two, user_three = register_users2
   
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three['auth_user_id']]
    })
    new_dm1 = r.json()
    
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_two["token"],
        "u_ids": [user_one["auth_user_id"]]
    })
    new_dm2 = r.json()
    
    requests.post(config.url + "dm/create/v1", json = {
        "token": user_two["token"],
        "u_ids": [user_three["auth_user_id"]]
    })
   
    r = requests.get(config.url + "dm/list/v1", params = {
        "token": user_one["token"]
    })
    
    dm_list = r.json()
    
    # Test owner and members of dm can view correct dm list and that dms users who
    # are not members of the dm cannot see those dms.
    assert dm_list == {'dms': [
        {'name': new_dm1['dm_name'], 'dm_id': new_dm1['dm_id']},
        {'name': new_dm2['dm_name'], 'dm_id': new_dm2['dm_id']}
    ]}
 
def test_list_groups_channels(register_users2):
    user_one, user_two, _ = register_users2
    
    # Create a channel and send a message in that channel
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_one["token"],
        "name": "Channel1",
        "is_public": True
    })
    new_chan1 = r.json()
    
    requests.post(config.url + "channels/create/v2", json = {
        "token": user_two["token"],
        "name": "Channel2",
        "is_public": True
    })
    
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_two["token"],
        "name": "Channel3",
        "is_public": False
    })
    new_chan3 = r.json()
    
    requests.post(config.url + "channel/invite/v2", json = {
        "token": user_two["token"],
        "channel_id": new_chan3['channel_id'],
        "u_id": user_one['auth_user_id']
    })
    
    # Test owner and members of channel can view correct dm list and that dms users who
    # are not members of the channel cannot see those channels.
    r = requests.get(config.url + "channels/list/v2", params = {
        "token": user_one["token"]
    })
    channel_list = r.json()

    assert channel_list == {'channels': [
        {'name': "Channel1", 'channel_id': new_chan1['channel_id']},
        {'name': "Channel3", 'channel_id': new_chan3['channel_id']}
    ]}
 
## Testing when token user is not a member of any groups
def test_list_groups_empty(register_users2):
    user_one, _, _ = register_users2
    
    r = requests.get(config.url + "channels/list/v2", params = {
        "token": user_one["token"]
    })
   
    assert r.json() == {"channels": []}
    
    r = requests.get(config.url + "dm/list/v1", params = {
        "token": user_one["token"]
    })
    assert r.json() == {"dms": []}
 
## Testing list_groups AccessError ##
def test_list_groups_invalid_token(register_users2):
    _, _, _ = register_users2
    
    r = requests.get(config.url + "dm/list/v1", params = {
        "token": "invalid_token"
    })
    assert r.status_code == ACCESS_ERROR
    
    r = requests.get(config.url + "channels/list/v2", params = {
        "token": "invalid_token"
    })
    assert r.status_code == ACCESS_ERROR

# -------------------------------------------- #
# dm/messages/v1 & channel/messages/v2 testing #
# -------------------------------------------- #  

def test_extract_messages_output_check(register_users2):
    user_one, user_two, user_three = register_users2
   
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three['auth_user_id']]
    })
    new_dm = r.json()
    
    resp = requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
    
    # Check output 
    assert "message_id" in resp.json()
   
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
   
    assert "hi" in [message['message'] for message in message_output['messages']]
    assert "message_id" in message_output['messages'][0]
    assert "u_id" in message_output['messages'][0]
    assert "message" in message_output['messages'][0]
    assert "time_created" in message_output['messages'][0]
    assert "is_pinned" in message_output['messages'][0]
    assert message_output["start"] == 0
    assert message_output["end"] == -1
 
def test_extract_messages_channels(register_users2):
    user_one, user_two, _ = register_users2
    
    # Create a channel and send a message in that channel
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_one["token"],
        "name": "Channel1",
        "is_public": True
    })
    new_chan1 = r.json()
    
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_two["token"],
        "name": "Channel2",
        "is_public": True
    })
    new_chan2 = r.json()
    
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_two["token"],
        "name": "Channel3",
        "is_public": False
    })
    new_chan3 = r.json()
    
    requests.post(config.url + "channel/invite/v2", json = {
        "token": user_two["token"],
        "channel_id": new_chan3['channel_id'],
        "u_id": user_one['auth_user_id']
    })
    
    requests.post(config.url + "channel/invite/v2", json = {
        "token": user_one["token"],
        "channel_id": new_chan1['channel_id'],
        "u_id": user_two['auth_user_id']
    })
    
    # Send messages in different channels
    requests.post(config.url + "message/send/v2", json = {
        "token": user_two["token"],
        "channel_id": new_chan1['channel_id'],
        "message": "hi"
    })
    
    requests.post(config.url + "message/send/v2", json = {
        "token": user_two["token"],
        "channel_id": new_chan2['channel_id'],
        "message": "hey"
    })
    
    requests.post(config.url + "message/send/v2", json = {
        "token": user_two["token"],
        "channel_id": new_chan3['channel_id'],
        "message": "hello"
    })
 
    # Extract the messages from respective channels
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": new_chan1['channel_id'],
        "start": 0
    })
    message_output =  resp.json()
    
    resp = requests.get(config.url + "channel/messages/v2", params = {
        "token": user_one["token"],
        "channel_id": new_chan3['channel_id'],
        "start": 0
    })
    message_output2 =  resp.json()
 
    assert "hi" in [message['message'] for message in message_output['messages']]
    assert "hello" in [message['message'] for message in message_output2['messages']]
    assert not "hey" in [message['message'] for message in message_output['messages']]
    assert not "hey" in [message['message'] for message in message_output2['messages']]
   
def test_extract_messages_empty(register_users2):
    user_one, user_two, user_three = register_users2
    
    # Create a dm
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()

    # Extract messages and check no messages exists in the database
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
   
    assert message_output == {"messages": [], "start" : 0, "end": -1}
    
def test_extract_messages_indexing(register_users2):
    user_one, user_two, user_three = register_users2
    
    # Create a dm
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()
   
    for _ in range(50):
        requests.post(config.url + "message/senddm/v1", json = {
            "token": user_one["token"],
            "dm_id": new_dm["dm_id"],
            "message": "hi"
        })
    
    # Extract messages and check output
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
   
    assert message_output["start"] == 0
    assert message_output["end"] == -1
    
    requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
   
    # Extract messages and check output
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 0
    })
    message_output = resp.json()
   
    assert message_output["start"] == 0
    assert message_output["end"] == 50
   
    # Extract messages and check output
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "start": 1
    })
    message_output = resp.json()
       
    assert message_output["start"] == 1
    assert message_output["end"] == -1
   

def test_extract_messages_invalid_dm_id(register_users2):
    user_one, user_two, user_three = register_users2
    
    # Create a dm and send a message in that dm
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()
    
    requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    }) 
    
    # Check that and INPUT_ERROR is raised when an invalid DM ID is given
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one["token"],
        "dm_id": 987654321,
        "start": 0
    })
    
    assert resp.status_code == INPUT_ERROR
   
def test_extract_messages_invalid_token(register_users2):
    user_one, user_two, user_three = register_users2
   
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()
   
    # Check that and ACCESS_ERROR is raised when an invalid token is given
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": "invalid_token",
        "dm_id": new_dm['dm_id'],
        "start": 0
    })
    
    assert resp.status_code == ACCESS_ERROR
 
def test_extract_messages_invalid_indexing(register_users2):
    user_one, user_two, user_three = register_users2
   
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json()
    
    # Check that and INPUT_ERROR is raised when an invalid index is given
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_one['token'],
        "dm_id": new_dm['dm_id'],
        "start": 1
    })
    
    assert resp.status_code == INPUT_ERROR
   
def test_extract_messages_unauthorised_user(register_users2):
    user_one, user_two, user_three = register_users2
   
    # Create group without user_three as a member
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    # Have user_three try to access message data from group they aren't part of.
    resp = requests.get(config.url + "dm/messages/v1", params = {
        "token": user_three['token'],
        "dm_id": new_dm['dm_id'],
        "start": 0
    })

    assert resp.status_code == ACCESS_ERROR  