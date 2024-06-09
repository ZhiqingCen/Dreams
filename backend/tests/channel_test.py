import pytest 
from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.common import invite_to_group, group_details

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_join Function Tests                                        ###
###-----------------------------------------------------------------------------------------------------------###

###------------###
### Test Setup ###
###------------###

@pytest.fixture
def register_users():
    clear_v1()
    user_global_owner = auth_register_v2("address0@email.com", "onetwothree", "User0", "GlobalOwner")
    user_owner = auth_register_v2("address1@email.com", "onetwothree", "User1", "Owner")
    user_member = auth_register_v2("address2@email.com", "onetwothree", "User2", "Member")
    user_not_member = auth_register_v2("address3@email.com", "onetwothree", "User3", "NotMember")
    unregistered_user = {'token': "not_a_token", 'auth_user_id': 4}
    return user_global_owner, user_owner, user_member, user_not_member, unregistered_user

@pytest.fixture
def create_channel(register_users):
    _,user_owner,_,_,_ = register_users
    channel_public = channels_create_v2(user_owner['token'], "Channel Public", True)
    channel_private = channels_create_v2(user_owner['token'], "Channel Private", False)
    nonexistent_channel = {'channel_id': 2}
    
    return channel_public, channel_private, nonexistent_channel

###----------------###
### Error Checking ###
###----------------###

def test_channel_join_invalid_token(register_users, create_channel):
    _, _, _, _, unregistered_user = register_users
    channel_public, _, _ = create_channel
    
    # token is not valid
    with pytest.raises(AccessError):
        channel_join_v2(unregistered_user['token'], channel_public['channel_id'])

def test_channel_join_unauthorised_member_private(register_users, create_channel):
    _, _, _, user_not_member, _ = register_users
    _, channel_private, _ = create_channel

    # channel is private + authorised user is not global owner
    with pytest.raises(AccessError):
        channel_join_v2(user_not_member['token'], channel_private['channel_id'])

def test_channel_join_token_is_member(register_users, create_channel):
    _, user_owner, user_member, _, _ = register_users
    channel_public, channel_private, _ = create_channel
    
    invite_to_group(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'], 'channel')
    invite_to_group(user_owner['token'], channel_private['channel_id'], user_member['auth_user_id'], 'channel')

    # token is part of channel
    with pytest.raises(AccessError):
        channel_join_v2(user_member['token'], channel_public['channel_id'])
    with pytest.raises(AccessError):    
        channel_join_v2(user_member['token'], channel_private['channel_id'])

def test_channel_join_invalid_channel_id(register_users, create_channel):
    _,user_owner, _, _, _ = register_users
    _, _, nonexistent_channel = create_channel
    
    # channel id is not valid
    with pytest.raises(InputError):
        channel_join_v2(user_owner['token'], nonexistent_channel['channel_id'])

def test_channel_join_none_input(register_users, create_channel):
    _,_,_,user_not_member,_ = register_users
    _, _, nonexistent_channel = create_channel

    with pytest.raises(AccessError):
        channel_join_v2(None, None)
    with pytest.raises(AccessError):    
        channel_join_v2(None, nonexistent_channel['channel_id'])

    with pytest.raises(InputError):
        channel_join_v2(user_not_member['token'], None)

###-----------------###
### Action Checking ###
###-----------------###

def test_channel_join_global_owner_public(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel
    
    channel_join_v2(user_global_owner['token'], channel_public['channel_id'])

    channel_content = group_details(user_owner['token'], channel_public['channel_id'], 'channel')
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_join_global_owner_private(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    _, channel_private, _ = create_channel
    
    channel_join_v2(user_global_owner['token'], channel_private['channel_id'])

    channel_content = group_details(user_owner['token'], channel_private['channel_id'], 'channel')
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_join_member_public(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _,_ = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    channel_content = group_details(user_owner['token'], channel_public['channel_id'], 'channel')
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_join_return_value(register_users, create_channel):
    _,_,user_member,_,_ = register_users
    channel_public, _, _ = create_channel
    
    assert channel_join_v2(user_member['token'],channel_public['channel_id']) == {} 

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_addowner Function Tests                                    ###
###-----------------------------------------------------------------------------------------------------------###

#Assumptions
#   - global owners cannot add/remove a user if they are not in the channel
# - if a u_id is not in the channel, add them

###----------------###
### Error Checking ###
###----------------###

# invalid token
def test_channel_addowner_invalid_token(register_users, create_channel):
    _,_,user_member,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_addowner_v1(unregistered_user['token'], channel_public['channel_id'], user_member['auth_user_id'])

# token not in the channel
def test_channel_addowner_token_not_member(register_users, create_channel):
    _,_,user_member,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_addowner_v1(user_not_member1['token'], channel_public['channel_id'], user_member['auth_user_id'])

# token not a channel owner or global owner
def test_channel_addowner_token_not_owner(register_users, create_channel):
    _,_, user_member,user_not_member,_ = register_users
    channel_public, _, _  = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_addowner_v1(user_member['token'], channel_public['channel_id'], user_not_member['auth_user_id'])

#channel_id is invalid
def test_channel_addowner_invalid_channel_id(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    _, _, nonexistent_channel = create_channel

    with pytest.raises(InputError):
        channel_addowner_v1(user_owner['token'], nonexistent_channel['channel_id'], user_member['auth_user_id'])

#u_id is invalid
def test_channel_addowner_invalid_u_id(register_users, create_channel):
    _,user_owner,_,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    with pytest.raises(InputError):
        channel_addowner_v1(user_owner['token'], channel_public['channel_id'], unregistered_user['auth_user_id'])

def test_channel_addowner_already_owner(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    with pytest.raises(InputError):
        channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

#none input
def test_channel_addowner_none_input(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, nonexistent_channel = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_addowner_v1(None, channel_public['channel_id'], user_member['auth_user_id'])
    with pytest.raises(AccessError):    
        channel_addowner_v1(None, nonexistent_channel['channel_id'], user_member['auth_user_id'])

    with pytest.raises(InputError):
        channel_addowner_v1(user_owner['token'], None, user_member['auth_user_id'])
    with pytest.raises(InputError):    
        channel_addowner_v1(user_owner['token'], channel_public['channel_id'], None)

###-----------------###
### Action Checking ###
###-----------------###

# user owner add owner
def test_channel_addowner_member_owner_is_auth(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    invite_to_group(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'], 'channel')

    channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    #Verify in channel owners
    channel_content = group_details(user_owner['token'], channel_public['channel_id'], 'channel')
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_addowner_member_global_owner_is_auth(register_users, create_channel):
    user_global_owner,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    invite_to_group(user_owner['token'], channel_public['channel_id'], user_global_owner['auth_user_id'], 'channel')

    invite_to_group(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'], 'channel')

    channel_addowner_v1(user_global_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    #Verify in channel owners
    channel_content = group_details(user_owner['token'], channel_public['channel_id'], 'channel')
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]

def test_channel_addowner_not_member_owner_is_auth():
    pass

def test_channel_addowner_not_member_global_owner_is_auth():
    pass

def test_channel_addowner_return_value(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    assert channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id']) == {} 

###-----------------------------------------------------------------------------------------------------------###
###                                        channel_removeowner Function Tests                                 ###
###-----------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

# invalid token
def test_channel_removeowner_invalid_token(register_users, create_channel):
    _,_,user_member,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_removeowner_v1(unregistered_user['token'], channel_public['channel_id'], user_member['auth_user_id'])

# token not in the channel
def test_channel_removeowner_token_not_member(register_users, create_channel):
    _,_,user_member,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_removeowner_v1(user_not_member1['token'], channel_public['channel_id'], user_member['auth_user_id'])

# token not a channel owner or global owner
def test_channel_removeowner_token_not_owner(register_users, create_channel):
    _,_, user_member,user_not_member,_ = register_users
    channel_public, _, _  = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_removeowner_v1(user_member['token'], channel_public['channel_id'], user_not_member['auth_user_id'])

#channel_id is invalid
def test_channel_removeowner_invalid_channel_id(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    _, _, nonexistent_channel = create_channel

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], nonexistent_channel['channel_id'], user_member['auth_user_id'])

#u_id is invalid
def test_channel_removeowner_invalid_u_id(register_users, create_channel):
    _,user_owner,_,_,unregistered_user = register_users
    channel_public, _, _ = create_channel

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], unregistered_user['auth_user_id'])

# u_id not in the channel
def test_channel_removeowner_u_id_not_member(register_users, create_channel):
    _,user_owner,_,user_not_member1,_ = register_users
    channel_public, _, _  = create_channel

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], user_not_member1['auth_user_id'])

#u_id is only owner
def test_channel_removeowner_u_id_only_owner(register_users, create_channel):
    _,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], user_owner['auth_user_id'])

def test_channel_removeowner_u_id_not_owner(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

#none input
def test_channel_removeowner_none_input(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, nonexistent_channel = create_channel

    channel_join_v2(user_member['token'], channel_public['channel_id'])

    with pytest.raises(AccessError):
        channel_removeowner_v1(None, channel_public['channel_id'], user_member['auth_user_id'])
    with pytest.raises(AccessError):    
        channel_removeowner_v1(None, nonexistent_channel['channel_id'], user_member['auth_user_id'])

    with pytest.raises(InputError):
        channel_removeowner_v1(user_owner['token'], None, user_member['auth_user_id'])
    with pytest.raises(InputError):    
        channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], None)

###-----------------###
### Action Checking ###
###-----------------###

def test_channel_removeowner_owner_is_auth(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    invite_to_group(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'], 'channel')

    channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    #Verify not a channel owner
    channel_content = group_details(user_owner['token'], channel_public['channel_id'], 'channel')
    assert user_member['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_removeowner_global_owner_is_auth(register_users, create_channel):
    user_global_owner,user_owner,_,_,_ = register_users
    channel_public, _, _ = create_channel

    invite_to_group(user_owner['token'], channel_public['channel_id'], user_global_owner['auth_user_id'], 'channel')

    channel_removeowner_v1(user_global_owner['token'], channel_public['channel_id'], user_owner['auth_user_id'])

    #Verify not a channel owner
    channel_content = group_details(user_global_owner['token'], channel_public['channel_id'], 'channel')
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]
    assert user_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_removeowner_return_value(register_users, create_channel):
    _,user_owner,user_member,_,_ = register_users
    channel_public, _, _ = create_channel

    channel_addowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id'])

    assert channel_removeowner_v1(user_owner['token'], channel_public['channel_id'], user_member['auth_user_id']) == {} 