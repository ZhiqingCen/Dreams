from src.channels import channels_create_v2
from src.channel import channel_join_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import AccessError, InputError
from src.common import invite_to_group, group_details, leave_group, list_groups, extract_messages_from_group, send_group_message
from src.dm import dm_create_v1
import pytest

###--------------------------------------------------------------------------------------------------------------###
###                                        invite_to_group Function Tests                                        ###
###--------------------------------------------------------------------------------------------------------------###

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def register_users():
    clear_v1()
    user_global_owner = auth_register_v2("address0@email.com", "onetwothree", "User0", "GlobalOwner")
    user_owner = auth_register_v2("address1@email.com", "onetwothree", "User1", "Owner")
    user_dm_member = auth_register_v2("address2@email.com", "onetwothree", "User2", "Member")
    user_not_member1 = auth_register_v2("address3@email.com", "onetwothree", "User3", "NotMember1")
    user_not_member2 = auth_register_v2("address4@email.com", "onetwothree", "User4", "NotMember2")
    unregistered_user = {'token': 5, 'auth_user_id': 5}

    return user_global_owner, user_owner, user_dm_member, user_not_member1, user_not_member2, unregistered_user

@pytest.fixture
def create_channel_with_user_owner(register_users):
    _,user_owner,_,_,_,_ = register_users
    channel_one = channels_create_v2(user_owner['token'], "Channel 1", True)
    nonexistent_channel = {'channel_id': 2}
    
    return channel_one, nonexistent_channel

@pytest.fixture
def create_dm_with_user_owner(register_users):
    _,user_owner,user_dm_member,_,_,_ = register_users
    dm_one = dm_create_v1(user_owner['token'], [user_dm_member['auth_user_id']])
    nonexistent_dm = {'dm_id': 2}
    
    return dm_one, nonexistent_dm

###--------------------------###
### Error Checking - Channel ###
###--------------------------###

def test_channel_invite_invalid_token(register_users, create_channel_with_user_owner):
    _, _, _, user_not_member1, user_not_member2, unregistered_user = register_users
    channel_one, _ = create_channel_with_user_owner
    
    # checks token is in channel first
    # checks if token isnt a registered user 
    with pytest.raises(AccessError):
        invite_to_group(user_not_member1['token'], channel_one['channel_id'], user_not_member2['auth_user_id'], 'channel')
    with pytest.raises(AccessError):
        invite_to_group(unregistered_user['token'], channel_one['channel_id'], user_not_member1['auth_user_id'], 'channel')

def test_channel_invite_invalid_group_id(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    _, nonexistent_channel = create_channel_with_user_owner
    
    # check valid channel id
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], nonexistent_channel['channel_id'], user_not_member1['auth_user_id'], 'channel')

def test_channel_invite_invalid_u_id(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_channel_member, _, unregistered_user = register_users
    channel_one, _ = create_channel_with_user_owner
    
    # check u_id is valid
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], channel_one['channel_id'], unregistered_user['auth_user_id'], 'channel')

    # error if u_id is already in the channel
    channel_join_v2(user_channel_member['token'], channel_one['channel_id'])
    
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], channel_one['channel_id'], user_channel_member['auth_user_id'], 'channel')

def test_channel_invite_none_input(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner

    with pytest.raises(AccessError):
        invite_to_group(None, None, None, 'channel')
    with pytest.raises(AccessError):
        invite_to_group(None, channel_one['channel_id'], user_not_member1['auth_user_id'], 'channel')
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], None, user_not_member1['auth_user_id'], 'channel')
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], channel_one['channel_id'], None, 'channel')

###---------------------###
### Error Checking - Dm ###
###---------------------###

def test_dm_invite_invalid_token(register_users, create_dm_with_user_owner):
    _, _, _, user_not_member1, user_not_member2, unregistered_user = register_users
    dm_one, _ = create_dm_with_user_owner
    
    # checks token is in dm first
    # checks if token isnt a registered user 
    with pytest.raises(AccessError):
        invite_to_group(user_not_member1['token'], dm_one['dm_id'], user_not_member2['auth_user_id'], 'dm')
    with pytest.raises(AccessError):
        invite_to_group(unregistered_user['token'], dm_one['dm_id'], user_not_member1['auth_user_id'], 'dm')

def test_dm_invite_invalid_group_id(register_users, create_dm_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    _, nonexistent_dm = create_dm_with_user_owner
    
    # check valid dm id
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], nonexistent_dm['dm_id'], user_not_member1['auth_user_id'], 'dm')

def test_dm_invite_invalid_u_id(register_users, create_dm_with_user_owner):
    _,user_owner, user_dm_member, _, _, unregistered_user = register_users
    dm_one, _ = create_dm_with_user_owner
    
    # check u_id is valid
    # error if u_id is already in the dm
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], dm_one['dm_id'], unregistered_user['auth_user_id'], 'dm')
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], dm_one['dm_id'], user_dm_member['auth_user_id'], 'dm')

def test_dm_invite_none_input(register_users, create_dm_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    dm_one, _ = create_dm_with_user_owner

    with pytest.raises(AccessError):
        invite_to_group(None, None, None, 'dm')
    with pytest.raises(AccessError):
        invite_to_group(None, dm_one['dm_id'], user_not_member1['auth_user_id'], 'dm')
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], None, user_not_member1['auth_user_id'], 'dm')
    with pytest.raises(InputError):
        invite_to_group(user_owner['token'], dm_one['dm_id'], None, 'dm')

###----------------------------------###
### Output/Action Checking - Channel ###
###----------------------------------###
def test_channel_invite_auth_is_owner(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    
    invite_to_group(user_owner['token'], channel_one['channel_id'], user_not_member1['auth_user_id'], 'channel')
    
    #check user_not_member1 is part of channel 1
    channel_content = group_details(user_owner['token'], channel_one['channel_id'], 'channel')
    assert user_not_member1['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_invite_global_owner(register_users, create_channel_with_user_owner):
    user_global_owner, user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner

    invite_to_group(user_owner['token'], channel_one['channel_id'], user_global_owner['auth_user_id'], 'channel')
    
    #check user_global_owner has owner permissions and is in the channel
    channel_content = group_details(user_owner['token'], channel_one['channel_id'], 'channel')
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['owner_members']]
    assert user_global_owner['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_invite_auth_is_member(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_member, user_not_member, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    invite_to_group(user_owner['token'], channel_one['channel_id'], user_member['auth_user_id'], 'channel')

    invite_to_group(user_member['token'], channel_one['channel_id'], user_not_member['auth_user_id'], 'channel')
    
    #check user_not_member is part of channel 1
    channel_content = group_details(user_member['token'], channel_one['channel_id'], 'channel')
    assert user_not_member['auth_user_id'] in [member['u_id'] for member in channel_content['all_members']]

def test_channel_invite_second_channel(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_member, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    channel_two = channels_create_v2(user_owner['token'], "Channel 2", True)
    
    invite_to_group(user_owner['token'], channel_one['channel_id'], user_member['auth_user_id'], 'channel')
    
    #check user_member is part of channel 1
    channel_content1 = group_details(user_owner['token'], channel_one['channel_id'], 'channel')
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content1['all_members']]

    invite_to_group(user_owner['token'], channel_two['channel_id'], user_member['auth_user_id'], 'channel')

    #check user_member is part of channel 2
    channel_content2 = group_details(user_owner['token'], channel_two['channel_id'], 'channel')
    assert user_member['auth_user_id'] in [member['u_id'] for member in channel_content2['all_members']]

def test_invite_to_group_return_type(register_users, create_channel_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    
    assert invite_to_group(user_owner['token'], channel_one['channel_id'], user_not_member1['auth_user_id'], 'channel') == {}

###-----------------------------###
### Output/Action Checking - Dm ###
###-----------------------------###
def test_dm_invite_auth_is_owner(register_users, create_dm_with_user_owner):
    _,user_owner, _, user_not_member1, _, _ = register_users
    dm_one, _ = create_dm_with_user_owner
    
    invite_to_group(user_owner['token'], dm_one['dm_id'], user_not_member1['auth_user_id'], 'dm')
    
    #check user_not_member1 is part of dm 1
    dm_content = group_details(user_owner['token'], dm_one['dm_id'], 'dm')
    assert user_not_member1['auth_user_id'] in [member['u_id'] for member in dm_content['members']]

def test_dm_invite_auth_is_member(register_users, create_dm_with_user_owner):
    _,user_owner, _, user_member, user_not_member, _ = register_users
    dm_one, _ = create_dm_with_user_owner
    invite_to_group(user_owner['token'], dm_one['dm_id'], user_member['auth_user_id'], 'dm')

    invite_to_group(user_member['token'], dm_one['dm_id'], user_not_member['auth_user_id'], 'dm')
    
    #check user_not_member is part of dm 1
    dm_content = group_details(user_member['token'], dm_one['dm_id'], 'dm')
    assert user_not_member['auth_user_id'] in [member['u_id'] for member in dm_content['members']]

def test_dm_invite_second_dm(register_users, create_dm_with_user_owner):
    _,user_owner, user_member1, user_member2, _, _ = register_users
    dm_one, _ = create_dm_with_user_owner
    dm_two = dm_create_v1(user_owner['token'], [user_member2['auth_user_id']])
    
    #check user_member1 is part of dm 1
    dm_content1 = group_details(user_owner['token'], dm_one['dm_id'], 'dm')
    assert user_member1['auth_user_id'] in [member['u_id'] for member in dm_content1['members']]

    invite_to_group(user_owner['token'], dm_two['dm_id'], user_member1['auth_user_id'], 'dm')

    #check user_member is part of dm 2
    dm_content2 = group_details(user_owner['token'], dm_two['dm_id'], 'dm')
    assert user_member1['auth_user_id'] in [member['u_id'] for member in dm_content2['members']]

###------------------------------------------------------------------------------------------------------------###
###                                        group_details Function Tests                                        ###
###------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###
def test_group_details_invalid_token(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _, _, _, _, _, unregistered_user = register_users
    channel_one, _ = create_channel_with_user_owner
    dm_one, _ = create_dm_with_user_owner
    
    # token is not valid
    with pytest.raises(AccessError):
        group_details(unregistered_user['token'], channel_one['channel_id'], 'channel')
    with pytest.raises(AccessError):
        group_details(unregistered_user['token'], dm_one['dm_id'], 'dm')

def test_group_details_token_not_member(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _, _, _, _, user_not_member, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    dm_one, _ = create_dm_with_user_owner
    
    # token is not part of channel
    with pytest.raises(AccessError):
        group_details(user_not_member['token'], channel_one['channel_id'], 'channel')
    with pytest.raises(AccessError):
        group_details(user_not_member['token'], dm_one['dm_id'], 'dm')

def test_group_details_invalid_group_id(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _,user_owner, _, _, _, _ = register_users
    _, nonexistent_channel = create_channel_with_user_owner
    _, nonexistent_dm = create_dm_with_user_owner
    
    # channel id is not valid
    with pytest.raises(InputError):
        group_details(user_owner['token'], nonexistent_channel['channel_id'], 'channel')
    with pytest.raises(InputError):
        group_details(user_owner['token'], nonexistent_dm['dm_id'], 'dm')

def test_group_details_none_input(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _,user_owner,_,_,_,_ = register_users
    _, nonexistent_channel = create_channel_with_user_owner
    _, nonexistent_dm = create_dm_with_user_owner

    with pytest.raises(AccessError):
        group_details(None, None, 'channel')
    with pytest.raises(AccessError):
        group_details(None, None, 'dm')
    with pytest.raises(AccessError):
        group_details(None, nonexistent_channel['channel_id'], 'channel')
    with pytest.raises(AccessError):
        group_details(None, nonexistent_dm['dm_id'], 'dm')

    with pytest.raises(InputError):
        group_details(user_owner['token'], None, 'channel')
    with pytest.raises(InputError):
        group_details(user_owner['token'], None, 'dm')


###---------------------------###
### Output Checking - Channel ###
###---------------------------###

def test_channel_details_global_owner_is_auth(register_users, create_channel_with_user_owner):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel_with_user_owner

    invite_to_group(user_owner['token'], channel_one['channel_id'], user_global_owner['auth_user_id'] ,'channel')

    assert group_details(user_global_owner['token'], channel_one['channel_id'], 'channel') == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_global_owner['auth_user_id'], 'name_first': 'User0', 'name_last': 'GlobalOwner',}, {'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_global_owner['auth_user_id'], 'name_first': 'User0', 'name_last': 'GlobalOwner',}, {'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
    }

def test_channel_details_owner_is_only_member(register_users, create_channel_with_user_owner):
    _, user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner

    assert group_details(user_owner['token'], channel_one['channel_id'], 'channel') == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
    }

def test_channel_details_owner_is_auth(register_users, create_channel_with_user_owner):
    _, user_owner, user_member, _, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    
    invite_to_group(user_owner['token'], channel_one['channel_id'], user_member['auth_user_id'], 'channel')

    assert group_details(user_owner['token'], channel_one['channel_id'], 'channel') == {
        'name': "Channel 1", 
        'is_public': True,
        'owner_members': [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',}],
        'all_members' : [{'u_id': user_owner['auth_user_id'], 'name_first': 'User1', 'name_last': 'Owner',},
                         {'u_id': user_member['auth_user_id'], 'name_first': 'User2', 'name_last': 'Member',},   
                        ],
    }

def test_channel_details_member_is_auth(register_users, create_channel_with_user_owner):
    _,user_owner,user_member,_,_,_ = register_users
    channel_one, _ = create_channel_with_user_owner

    invite_to_group(user_owner['token'], channel_one['channel_id'], user_member['auth_user_id'], 'channel')

    assert group_details(user_member['token'], channel_one['channel_id'], 'channel') == {
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
    dm_one = dm_create_v1(user_owner['token'], [])

    assert group_details(user_owner['token'], dm_one['dm_id'], 'dm') == {
        'name': "user1owner", 
        'members': [{'u_id': user_owner['auth_user_id'], 'email': 'address1@email.com','name_first': 'User1', 'name_last': 'Owner','handle_str': 'user1owner',},]
    }

def test_dm_details_owner_is_auth(register_users, create_dm_with_user_owner):
    _, user_owner, user_member, _, _, _ = register_users
    dm_one, _ = create_dm_with_user_owner

    assert group_details(user_owner['token'], dm_one['dm_id'], 'dm') == {
        'name': "user1owner, user2member", 
        'members' : [{'u_id': user_owner['auth_user_id'], 'email': 'address1@email.com','name_first': 'User1', 'name_last': 'Owner','handle_str': 'user1owner',},
                     {'u_id': user_member['auth_user_id'], 'email': 'address2@email.com', 'name_first': 'User2', 'name_last': 'Member','handle_str': 'user2member',},   
                    ],
    }

def test_dm_details_member_is_auth(register_users, create_dm_with_user_owner):
    _,user_owner,user_member,_,_,_ = register_users
    dm_one, _ = create_dm_with_user_owner

    assert group_details(user_member['token'], dm_one['dm_id'], 'dm') == {
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

def test_leave_group_invalid_token(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _, _, _, _, user_not_member, unregistered_user = register_users
    channel_one, _ = create_channel_with_user_owner
    dm_one, _ = create_dm_with_user_owner
    
    # token is not valid
    # token is not part of group
    with pytest.raises(AccessError):
        leave_group(unregistered_user['token'], channel_one['channel_id'], 'channel')
    with pytest.raises(AccessError):
        leave_group(user_not_member['token'], channel_one['channel_id'], 'channel')
    with pytest.raises(AccessError):
        leave_group(unregistered_user['token'], dm_one['dm_id'], 'dm')
    with pytest.raises(AccessError):
        leave_group(user_not_member['token'], dm_one['dm_id'], 'dm')

def test_leave_group_invalid_group_id(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _,user_owner, _, _, _, _ = register_users
    _, nonexistent_channel = create_channel_with_user_owner
    _, nonexistent_dm = create_dm_with_user_owner
    
    # group id is not valid
    with pytest.raises(InputError):
        leave_group(user_owner['token'], nonexistent_channel['channel_id'], 'channel')
    with pytest.raises(InputError):
        leave_group(user_owner['token'], nonexistent_dm['dm_id'], 'dm')

def test_leave_group_none_input(register_users, create_channel_with_user_owner, create_dm_with_user_owner):
    _,user_owner,_,_,_,_ = register_users
    _, nonexistent_channel = create_channel_with_user_owner
    _, nonexistent_dm = create_dm_with_user_owner

    with pytest.raises(AccessError):
        leave_group(None, None, 'channel')
    with pytest.raises(AccessError):
        leave_group(None, None, 'dm')
    with pytest.raises(AccessError):
        leave_group(None, nonexistent_channel['channel_id'], 'channel')
    with pytest.raises(AccessError):
        leave_group(None, nonexistent_dm['dm_id'], 'dm')

    with pytest.raises(InputError):
        leave_group(user_owner['token'], None, 'channel')
    with pytest.raises(InputError):
        leave_group(user_owner['token'], None, 'dm')

###---------------------------###
### Action Checking - Channel ###
###---------------------------###

# channel member leave
def test_leave_group_channel_member(register_users, create_channel_with_user_owner):
    _,user_owner,_,user_member,_,_ = register_users
    channel_one, _ = create_channel_with_user_owner

    invite_to_group(user_owner['token'], channel_one['channel_id'], user_member['auth_user_id'], 'channel')

    leave_group(user_member['token'], channel_one['channel_id'], 'channel')

    channel_content = group_details(user_owner['token'], channel_one['channel_id'], 'channel')
    assert user_member['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]

# global owner leave channel
def test_leave_group_channel_global_owner(register_users, create_channel_with_user_owner):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel_with_user_owner

    invite_to_group(user_owner['token'], channel_one['channel_id'], user_global_owner['auth_user_id'], 'channel')

    leave_group(user_global_owner['token'], channel_one['channel_id'], 'channel')

    channel_content = group_details(user_owner['token'], channel_one['channel_id'], 'channel')
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

# channel owner leave
def test_leave_group_channel_owner(register_users, create_channel_with_user_owner):
    user_global_owner,user_owner,_,_,_,_ = register_users
    channel_one, _ = create_channel_with_user_owner

    leave_group(user_owner['token'], channel_one['channel_id'], 'channel')

    channel_join_v2(user_global_owner['token'], channel_one['channel_id'])
    
    channel_content = group_details(user_global_owner['token'], channel_one['channel_id'], 'channel')
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert user_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

def test_leave_group_channel_return_type(register_users, create_channel_with_user_owner):
    _,user_owner, _, _, _, _ = register_users
    channel_one, _ = create_channel_with_user_owner
    
    assert leave_group(user_owner['token'], channel_one['channel_id'], 'channel') == {}

###----------------------###
### Action Checking - Dm ###
###----------------------###

# dm member leave
def test_leave_group_dm_member(register_users, create_dm_with_user_owner):
    _,user_owner, user_member,_,_,_ = register_users
    dm_one, _ = create_dm_with_user_owner

    leave_group(user_member['token'], dm_one['dm_id'], 'dm')

    dm_content = group_details(user_owner['token'], dm_one['dm_id'], 'dm')
    assert user_member['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

# global owner leave dm
def test_leave_group_dm_global_owner(register_users, create_dm_with_user_owner):
    user_global_owner,user_owner,_,_,_,_ = register_users
    dm_one, _ = create_dm_with_user_owner

    invite_to_group(user_owner['token'], dm_one['dm_id'], user_global_owner['auth_user_id'], 'dm')

    leave_group(user_global_owner['token'], dm_one['dm_id'], 'dm')

    dm_content = group_details(user_owner['token'], dm_one['dm_id'], 'dm')
    assert user_global_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

# dm owner leave
def test_leave_group_dm_owner(register_users, create_dm_with_user_owner):
    _,user_owner,_,_,_,_ = register_users
    dm_one, _ = create_dm_with_user_owner

    leave_group(user_owner['token'], dm_one['dm_id'], 'dm')

    assert not list_groups(user_owner['token'], 'dm')['dms']

def test_leave_group_dm_return_type(register_users, create_dm_with_user_owner):
    _,user_owner, _, _, _, _ = register_users
    dm_one, _ = create_dm_with_user_owner
    
    assert leave_group(user_owner['token'], dm_one['dm_id'], 'dm') == {}


###----------------------------------------------------------------------------------------------------------###
###                                        send_group_message Function Tests                                       ###
###----------------------------------------------------------------------------------------------------------###

###-------------###
### Test Set Up ###
###-------------###
user1 = { 
                'email': "address1@email.com", 
                'name_first': "U1", 
                'name_last': "One", 
                'handle_str': "u1one"
              }
user2 = { 
                'email': "address2@email.com", 
                'name_first': "U2", 
                'name_last': "Two", 
                'handle_str': "u2two"
              }
user3 = { 
                'email': "address3@email.com", 
                'name_first': "U3", 
                'name_last': "Three", 
                'handle_str': "u3three"
              } 


def register_users2(): 
    clear_v1()
    global user1, user2, user3
    user_one = auth_register_v2(user1['email'], "qwerty1", user1['name_first'], 
        user1['name_last'])
    user_two = auth_register_v2(user2['email'], "qwerty2", user2['name_first'], 
        user2['name_last'])
    user_three = auth_register_v2(user3['email'], "qwerty3", user3['name_first'], 
        user3['name_last'])
    
    return user_one, user_two, user_three

###-------###
### Tests ###
###-------###

def test_send_group_message_dm():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    assert "message_id" in send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert "hi" in [message['message'] for message in message_output['messages']]
   
def test_send_group_message_channel():
    
    user_one, _, _ = register_users2()
    
    new_channel = channels_create_v2(user_one['token'], "Channel", False)
    
    send_group_message(user_one['token'], new_channel['channel_id'], "hi", "channel")
    
    message_output =  extract_messages_from_group(user_one['token'], 
        new_channel['channel_id'], 0, "channel")
    
    assert "hi" in [message['message'] for message in message_output['messages']]

def test_send_group_message_invalid_dm_id():
    
    _, _, user_three = register_users2()

    with pytest.raises(AccessError):
        send_group_message(user_three['token'], 987654321, "hi", "dm")

        
def test_send_group_message_access_errors():
    
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])

    with pytest.raises(AccessError):
        send_group_message(user_three['token'], new_dm['dm_id'], "hi", "dm")
 
    
def test_send_group_message_message_too_long():
    
    user_one, user_two, _ = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    send_group_message(user_one['token'], new_dm['dm_id'], "a" * 1000, "dm")

    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert "a" * 1000 in [message['message'] for message in message_output['messages']]

    with pytest.raises(InputError):
        send_group_message(user_one['token'], new_dm['dm_id'], "a" * 1001, "dm")

def test_send_group_message_message_empty():
    
    user_one, user_two, _ = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])

    with pytest.raises(InputError):
        send_group_message(user_one['token'], new_dm['dm_id'], "", "dm") 

###----------------------------------------------------------------------------------------------------------###
###                                        list_groups Function Tests                                        ###
###----------------------------------------------------------------------------------------------------------###

## Testing list_groups output ##
def test_list_groups_dms():
    user_one, user_two, user_three = register_users2()
    
    new_dm1 = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
        user_three['auth_user_id']])
    new_dm2 = dm_create_v1(user_two['token'], [user_one['auth_user_id']])
    _ = dm_create_v1(user_two['token'], [user_three['auth_user_id']])
    
    # Test owner and members of dm can view correct dm list and that dms users who
    # are not members of the dm cannot see those dms.
    dm_list = list_groups(user_one['token'], "dm")
    assert dm_list == {'dms': [
        {'name': new_dm1['dm_name'], 'dm_id': new_dm1['dm_id']},
        {'name': new_dm2['dm_name'], 'dm_id': new_dm2['dm_id']}
    ]}

def test_list_groups_channels():
    user_one, user_two, _ = register_users2()
    
    new_chan1 = channels_create_v2(user_one['token'], "Channel1", True)
    _ = channels_create_v2(user_two['token'], "Channel2", True)
    new_chan3 = channels_create_v2(user_two['token'], "Channel3", False)
    
    invite_to_group(user_two['token'], new_chan3['channel_id'], user_one['auth_user_id'], 'channel')
    
    # Test owner and members of channel can view correct dm list and that dms users who
    # are not members of the channel cannot see those channels.
    channel_list = list_groups(user_one['token'], "channel")
    assert channel_list == {'channels': [
        {'name': "Channel1", 'channel_id': new_chan1['channel_id']},
        {'name': "Channel3", 'channel_id': new_chan3['channel_id']}
    ]}
  
## Testing when token user is not a member of any groups
def test_list_groups_empty():
    user_one, _, _ = register_users2()
    
    assert list_groups(user_one['token'], "dm") == {"dms": []}
    assert list_groups(user_one['token'], "channel") == {"channels": []}

## Testing list_groups AccessError ## 
def test_list_groups_invalid_token():
    
    with pytest.raises(AccessError):
        list_groups("invalid_token", "channel")     

###--------------------------------------------------------------------------------------------------------------------------###
###                                        extract_messages_from_group Function Tests                                        ###
###--------------------------------------------------------------------------------------------------------------------------###

def test_extract_messages_output_check():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    assert "message_id" in send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert "hi" in [message['message'] for message in message_output['messages']]
    assert "message_id" in message_output['messages'][0]
    assert "u_id" in message_output['messages'][0]
    assert "message" in message_output['messages'][0]
    assert "time_created" in message_output['messages'][0]
    assert "is_pinned" in message_output['messages'][0]
    assert message_output["start"] == 0
    assert message_output["end"] == -1

def test_extract_messages_channels():
    user_one, user_two, _ = register_users2()
    
    new_chan1 = channels_create_v2(user_one['token'], "Channel1", True)
    new_chan2 = channels_create_v2(user_two['token'], "Channel2", True)
    new_chan3 = channels_create_v2(user_two['token'], "Channel2", False)
    
    invite_to_group(user_one['token'], new_chan1['channel_id'], user_two['auth_user_id'], 'channel')
    invite_to_group(user_two['token'], new_chan3['channel_id'], user_one['auth_user_id'], 'channel')

    send_group_message(user_two['token'], new_chan1['channel_id'], "hi", "channel")
    send_group_message(user_two['token'], new_chan2['channel_id'], "hey", "channel")
    send_group_message(user_two['token'], new_chan3['channel_id'], "hello", "channel")
    
    message_output = extract_messages_from_group(user_one['token'], new_chan1['channel_id'], 0, "channel")
    message_output2 = extract_messages_from_group(user_one['token'], new_chan3['channel_id'], 0, "channel")

    assert "hi" in [message['message'] for message in message_output['messages']]
    assert "hello" in [message['message'] for message in message_output2['messages']]
    assert not "hey" in [message['message'] for message in message_output['messages']]
    assert not "hey" in [message['message'] for message in message_output2['messages']]
    
def test_extract_messages_empty():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert message_output == {"messages": [], "start" : 0, "end": -1}
     
    
def test_extract_messages_indexing():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    for _ in range(50):
        send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert message_output["start"] == 0
    assert message_output["end"] == -1
    
    send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert message_output["start"] == 0
    assert message_output["end"] == 50
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 1, "dm")
        
    assert message_output["start"] == 1
    assert message_output["end"] == -1
    
def test_extract_messages_invalid_dm_id():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    
    with pytest.raises(InputError):
        extract_messages_from_group(user_one['token'], 987654321, 0, "dm")
    
def test_extract_messages_invalid_token():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    with pytest.raises(AccessError):
        extract_messages_from_group("invalid_token", new_dm['dm_id'], 0, "dm")

def test_extract_messages_invalid_indexing():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    with pytest.raises(InputError):
        extract_messages_from_group(user_one['token'], new_dm['dm_id'], 1, "dm")
    
def test_extract_messages_unauthorised_user():
    user_one, user_two, user_three = register_users2()
    
    # Create group without user_three as a member
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    with pytest.raises(AccessError):
        # Have user_three try to access message data from group they aren't part of.
        extract_messages_from_group(user_three['token'], new_dm['dm_id'], 0, "dm")
    
