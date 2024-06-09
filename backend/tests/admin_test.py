import pytest
from src.error import AccessError, InputError
from src.other import clear_v1, search_v2
from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_create_v2
from src.common import invite_to_group, group_details, send_group_message
from src.admin import admin_remove_user_v1, admin_change_user_permissions_v1
from src.dm import dm_create_v1
from src.user import user_profile_v2

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def register_users():
    clear_v1()

    user_global_owner = auth_register_v2("address0@email.com", "onetwothree", "User0", "GlobalOwner")
    
    user_group_owner = auth_register_v2("address1@email.com", "onetwothree", "User1", "ChannelOwner")
    
    user_global_member = auth_register_v2("address2@email.com", "onetwothree", "User2", "GlobalMember")
    
    user_group_member = auth_register_v2("address3@email.com", "onetwothree", "User3", "ChannelMember")
    
    unregistered_user = {'token': 4, 'auth_user_id': 4}

    return user_global_owner, user_group_owner, user_global_member, user_group_member, unregistered_user

@pytest.fixture
def create_channel(register_users):
    global_owner, group_owner, _, group_member, _ = register_users
    channel = channels_create_v2(group_owner['token'], "Channel 1", True)
    invite_to_group(group_owner['token'], channel['channel_id'], group_member['auth_user_id'], 'channel')
    invite_to_group(group_owner['token'], channel['channel_id'], global_owner['auth_user_id'], 'channel')

    return channel

@pytest.fixture
def create_dm(register_users):
    global_owner, group_owner, _, group_member, _ = register_users
    dm = dm_create_v1(group_owner['token'], [global_owner['auth_user_id'], group_member['auth_user_id']])

    return dm

###-----------------------------------------------------------------------------------------------------------###
###                                        admin_remove Function Tests                                        ###
###-----------------------------------------------------------------------------------------------------------###

# Assumptions
    # it is valid for an owner to remove themselves
    # it is valid to remove a channel owner as the global owner is an owner of all channels
    # it is an imput error if u_id has already been removed
    # it is an access error if token has already been removed
    # Removed Users is a reserved name for the system - no user can register with any variation of "Removed user"

###----------------###
### Error Checking ###
###----------------###

def test_admin_remove_user_token_not_global_owner(register_users):
    _, channel_owner, global_member, channel_member, _ = register_users
    
    with pytest.raises(AccessError):
        # When token is not a global owner - global member, channel owner
        admin_remove_user_v1(channel_owner['token'], channel_member['auth_user_id'])
    with pytest.raises(AccessError):    
        # When token is not a global owner - global member
        admin_remove_user_v1(global_member['token'], channel_member['auth_user_id'])

def test_admin_remove_user_token_invalid(register_users):
    _, _, global_member, _, unregistered_user = register_users

    with pytest.raises(AccessError):
        # When token is an unregistered user
        admin_remove_user_v1(unregistered_user['token'], global_member['auth_user_id'])
    with pytest.raises(AccessError):    
        # When token is None
        admin_remove_user_v1(None, global_member['auth_user_id'])

def test_admin_remove_user_token_already_removed(register_users):
    global_owner, _, global_member_to_owner, channel_member, _ = register_users
    global_owner_permission_id = 1

    admin_change_user_permissions_v1(global_owner['token'], global_member_to_owner['auth_user_id'], global_owner_permission_id)
    
    admin_remove_user_v1(global_owner['token'], global_member_to_owner['auth_user_id'])

    with pytest.raises(AccessError):
        # When token has already been removed
        admin_remove_user_v1(global_member_to_owner['token'], channel_member['auth_user_id'])

def test_admin_remove_only_global_owner(register_users):
    global_owner, _, _, _, _ = register_users

    with pytest.raises(InputError):
        # When u_id is currently the only global owner
        admin_remove_user_v1(global_owner['token'], global_owner['auth_user_id'])

def test_admin_remove_user_u_id_invalid(register_users):
    global_owner, _, _, _, unregistered_user = register_users

    with pytest.raises(InputError):
        # When u_id is an unregistered user
        admin_remove_user_v1(global_owner['token'], unregistered_user['auth_user_id'])
    with pytest.raises(InputError):    
        # When u_id is None
        admin_remove_user_v1(global_owner['token'], None)

def test_admin_remove_user_u_id_already_removed(register_users):
    global_owner, _, global_member, _, _ = register_users

    admin_remove_user_v1(global_owner['token'], global_member['auth_user_id'])

    with pytest.raises(InputError):
        # When u_id has already been removed
        admin_remove_user_v1(global_owner['token'], global_member['auth_user_id'])

###-----------------###
### Action Checking ###
###-----------------###

# remove a global member, channel member + dm member
def test_admin_remove_user_global_member(register_users, create_channel, create_dm): 
    global_owner, _, _, global_member, _ = register_users
    channel = create_channel
    dm = create_dm

    send_group_message(global_member['token'],channel['channel_id'], "hi", 'channel')
    send_group_message(global_member['token'],dm['dm_id'], "hello", 'dm')

    admin_remove_user_v1(global_owner['token'], global_member['auth_user_id'])

    # verify that their name is "Removed user" and that their profile is retrievable
    removed_user = user_profile_v2(global_owner['token'], global_member['auth_user_id'])['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == "Removed user"
    
    # Verify messages that they have sent contains contents 'removed user'
    user_messages = search_v2(global_owner['token'], f"u_id={global_member['auth_user_id']}")

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    with pytest.raises(InputError):
        auth_login_v2("address3@email.com", "onetwothree")

    # verify that they are no longer in channel or dm
    channel_content = group_details(global_owner['token'], channel['channel_id'], 'channel')
    assert global_member['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]

    dm_content = group_details(global_owner['token'], dm['dm_id'], 'dm')
    assert global_member['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

# remove a global member, channel owner 
def test_admin_remove_user_global_member_channel_owner(register_users, create_channel, create_dm): 
    global_owner, channel_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm

    send_group_message(channel_owner['token'],channel['channel_id'], "hi", 'channel')
    send_group_message(channel_owner['token'],dm['dm_id'], "hello", 'dm')

    admin_remove_user_v1(global_owner['token'], channel_owner['auth_user_id'])

    # verify that their name is "Removed user" and that their profile is retrievable
    removed_user = user_profile_v2(global_owner['token'], channel_owner['auth_user_id'])['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == 'Removed user'
    
    # Verify messages that they have sent contains contents 'removed user'
    user_messages = search_v2(global_owner['token'], f"u_id={channel_owner['auth_user_id']}")

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"

    # Verify that they cannot login
    with pytest.raises(InputError):
        auth_login_v2("address1@email.com", "onetwothree")

    # verify that they are no longer in any groups (both owner and all members)
    channel_content = group_details(global_owner['token'], channel['channel_id'], 'channel')
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    dm_content = group_details(global_owner['token'], dm['dm_id'], 'dm')
    assert channel_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

# remove a global owner
def test_admin_remove_user_global_owner(register_users, create_channel, create_dm): 
    global_owner, group_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm
    owner_permission_id = 1

    send_group_message(global_owner['token'],channel['channel_id'], "hi", 'channel')
    send_group_message(global_owner['token'],dm['dm_id'], "hello", 'dm')

    admin_change_user_permissions_v1(global_owner['token'], group_owner['auth_user_id'], owner_permission_id)

    admin_remove_user_v1(group_owner['token'], global_owner['auth_user_id'])

    # verify that their name is "Removed user" and that their profile is retrievable
    removed_user = user_profile_v2(group_owner['token'], global_owner['auth_user_id'])['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == 'Removed user'
    
    # Verify messages that they have sent contains contents 'removed user'
    user_messages = search_v2(group_owner['token'], f"u_id={global_owner['auth_user_id']}")

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"
    
    # Verify that they cannot login
    with pytest.raises(InputError):
        auth_login_v2("address0@email.com", "onetwothree")

    # verify that they are no longer in any groups (both owner and all members)
    channel_content = group_details(group_owner['token'], channel['channel_id'], 'channel')
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    dm_content = group_details(group_owner['token'], dm['dm_id'], 'dm')
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

# remove theselves
def test_admin_remove_token_user(register_users, create_channel, create_dm): 
    global_owner, group_owner, _, _, _ = register_users
    channel = create_channel
    dm = create_dm
    owner_permission_id = 1

    send_group_message(global_owner['token'],channel['channel_id'], "hi", 'channel')
    send_group_message(global_owner['token'],dm['dm_id'], "hello", 'dm')

    admin_change_user_permissions_v1(global_owner['token'], group_owner['auth_user_id'], owner_permission_id)

    admin_remove_user_v1(global_owner['token'], global_owner['auth_user_id'])

    # verify that their name is "Removed user" and that their profile is retrievable
    removed_user = user_profile_v2(group_owner['token'], global_owner['auth_user_id'])['user']

    assert f"{removed_user['name_first']} {removed_user['name_last']}" == 'Removed user'
    
    # Verify messages that they have sent contains contents 'removed user'
    user_messages = search_v2(group_owner['token'], f"u_id={global_owner['auth_user_id']}")

    for message in user_messages['messages']:
        assert message['message'] == "Removed user"
    
    # Verify that they cannot login
    with pytest.raises(InputError):
        auth_login_v2("address0@email.com", "onetwothree")

    # verify that they are no longer in any groups (both owner and all members)
    channel_content = group_details(group_owner['token'], channel['channel_id'], 'channel')
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['all_members']]
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in channel_content['owner_members']]

    dm_content = group_details(group_owner['token'], dm['dm_id'], 'dm')
    assert global_owner['auth_user_id'] not in [member['u_id'] for member in dm_content['members']]

###----------------------------------------------------------------------------------------------------------------------------###
###                                        admin_change_user_permissions Function Tests                                        ###
###----------------------------------------------------------------------------------------------------------------------------###

# Assumptions
    # does nothing if permissions are already set to whatever they are desiring to change it to
    # it is valid to change your own permissions
    # nothing happens when you try to change the user's permissions to they permissions they already have
    # input error if trying to change permissions to member of the only owner

###----------------###
### Error Checking ###
###----------------###

def test_admin_change_permissions_token_not_global_owner(register_users):
    _, channel_owner, global_member, channel_member, _ = register_users
    owner_permission_id = 1
    
    with pytest.raises(AccessError):
        # When token is not a global owner - global member, channel owner
        admin_change_user_permissions_v1(channel_owner['token'], global_member['auth_user_id'], owner_permission_id)
    with pytest.raises(AccessError):    
        # When token is not a global owner - global member
        admin_change_user_permissions_v1(global_member['token'], channel_member['auth_user_id'], owner_permission_id)

def test_admin_change_permissions_token_invalid(register_users):
    _, _, global_member, _, unregistered_user = register_users
    owner_permission_id = 1

    with pytest.raises(AccessError):
        # When token is an unregistered user
        admin_change_user_permissions_v1(unregistered_user['token'], global_member['auth_user_id'], owner_permission_id)
    with pytest.raises(AccessError):    
        # When token is None
        admin_change_user_permissions_v1(None, global_member['auth_user_id'], owner_permission_id)

def test_admin_change_permissions_token_removed_user(register_users):
    global_owner, _, global_member_to_owner, channel_member, _ = register_users
    owner_permission_id = 1

    admin_change_user_permissions_v1(global_owner['token'], global_member_to_owner['auth_user_id'], owner_permission_id)

    admin_remove_user_v1(global_owner['token'], global_member_to_owner['auth_user_id'])

    with pytest.raises(AccessError):
        # When token is a removed user
        admin_change_user_permissions_v1(global_member_to_owner['token'], channel_member['auth_user_id'], owner_permission_id)

def test_admin_change_permissions_u_id_invalid(register_users):
    global_owner, _, _, _, unregistered_user = register_users
    owner_permission_id = 1

    with pytest.raises(InputError):
        # When u_id is an unregistered user
        admin_change_user_permissions_v1(global_owner['token'], unregistered_user['auth_user_id'], owner_permission_id)
    with pytest.raises(InputError):    
        # When u_id is None
        admin_change_user_permissions_v1(global_owner['token'], None, owner_permission_id)

def test_admin_change_permissions_u_id_only_global_owner(register_users):
    global_owner, _, _, _, _ = register_users
    member_permission_id = 2

    with pytest.raises(InputError):
        # When u_id is currently the only global owner
        admin_change_user_permissions_v1(global_owner['token'], global_owner['auth_user_id'], member_permission_id)

def test_admin_change_permissions_u_id_removed_user(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1

    admin_remove_user_v1(global_owner['token'], global_member['auth_user_id'])

    with pytest.raises(InputError):
        # When token is a removed user
        admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], owner_permission_id)

def test_admin_change_permissions_permission_id_invalid(register_users):
    global_owner, _, global_member, _, _ = register_users
    invalid_permission_id = 0

    with pytest.raises(InputError):
        # When permission_id is an invalid value
        admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], invalid_permission_id)
    with pytest.raises(InputError):    
        # When permission_id is None
        admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], None)

###-----------------###
### Output Checking ###
###-----------------###

#global member to global owner
def test_admin_change_permissions_to_owner(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2
    
    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], owner_permission_id)

    # should be valid, if an error is raised then it didnt work.
    admin_change_user_permissions_v1(global_member['token'], global_owner['auth_user_id'], member_permission_id)

#global owner to global member
def test_admin_change_permissions_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2

    #add another global owner
    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], owner_permission_id)

    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], member_permission_id)

    with pytest.raises(AccessError):
        admin_change_user_permissions_v1(global_member['token'], global_owner['auth_user_id'], member_permission_id)

# no change in permissions - owner
def test_admin_change_permissions_owner_to_owner(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1

    admin_change_user_permissions_v1(global_owner['token'], global_owner['auth_user_id'], owner_permission_id)
    
    # should be valid, if an error is raised then it didnt work.
    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], owner_permission_id)

# no change in permissions - member
def test_admin_change_permissions_member_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    member_permission_id = 2

    #should be valid, should not raise an error
    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], member_permission_id)

    # Verify not owner permissions
    with pytest.raises(AccessError):
        admin_change_user_permissions_v1(global_member['token'], global_owner['auth_user_id'], member_permission_id)

# changing own permissions (only possible owner to member)
def test_admin_change_permissions_self_to_member(register_users):
    global_owner, _, global_member, _, _ = register_users
    owner_permission_id = 1
    member_permission_id = 2

    # add a second global owner
    admin_change_user_permissions_v1(global_owner['token'], global_member['auth_user_id'], owner_permission_id)

    admin_change_user_permissions_v1(global_member['token'], global_member['auth_user_id'], member_permission_id)

    with pytest.raises(AccessError):
        admin_change_user_permissions_v1(global_member['token'], global_owner['auth_user_id'], member_permission_id)

    
