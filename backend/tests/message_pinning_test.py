from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import AccessError, InputError
from src.dm import dm_create_v1, dm_remove_v1
from src.user import users_all_v1
from src.common import list_groups, send_group_message, extract_messages_from_group
from src.message import message_pinning
from src.channels import channels_create_v2
import pytest

user1 = {   
                'u_id': -1,
                'email': "address1@email.com", 
                'name_first': "U1", 
                'name_last': "One", 
                'handle_str': "u1one"
              }
user2 = {   
                'u_id': -1,
                'email': "address2@email.com", 
                'name_first': "U2", 
                'name_last': "Two", 
                'handle_str': "u2two"
              }
user3 = {   
                'u_id': -1,
                'email': "address3@email.com", 
                'name_first': "U3", 
                'name_last': "Three", 
                'handle_str': "u3three"
              }              

def register_users():
    clear_v1() 
    global user1, user2, user3
    user_one = auth_register_v2(user1['email'], "qwerty1", user1['name_first'], user1['name_last'])
    user_two = auth_register_v2(user2['email'], "qwerty2", user2['name_first'], user2['name_last'])
    user_three = auth_register_v2(user3['email'], "qwerty3", user3['name_first'], user3['name_last'])
    
    user1['u_id'] = user_one['auth_user_id']
    user2['u_id'] = user_two['auth_user_id']
    user3['u_id'] = user_three['auth_user_id']
    
    return user_one, user_two, user_three
 
#################################################
#              Test message_pin                 #
#################################################
    
def test_message_pin_dm():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert not message_output['messages'][0]['is_pinned']
    
    assert message_pinning(user_one['token'], message_id, True) == {}
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert message_output['messages'][0]['is_pinned']
    
    
def test_message_pin_channel():    
    user_one, _, _ = register_users()
    new_chan = channels_create_v2(user_one['token'], "Channel1", True)
    
    message_id = send_group_message(user_one['token'], new_chan['channel_id'], "hi", "channel")['message_id']
    
    message_output = extract_messages_from_group(user_one['token'], new_chan['channel_id'], 0, "channel")

    assert not message_output['messages'][0]['is_pinned']
    
    assert message_pinning(user_one['token'], message_id, True) == {}
    message_output = extract_messages_from_group(user_one['token'], new_chan['channel_id'], 0, "channel")
    
    assert message_output['messages'][0]['is_pinned']


def test_message_pin_invalid_message_id():
    user_one, _, _ = register_users()
    
    with pytest.raises(InputError):
        message_pinning(user_one['token'], 987654321, True)     

def test_message_pin_already_pinned():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    message_pinning(user_one['token'], message_id, True) 
    
    with pytest.raises(InputError):
        message_pinning(user_one['token'], message_id, True) 
        
def test_message_pin_user_not_member():
    user_one, user_two, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    with pytest.raises(AccessError):
        message_pinning(user_two['token'], message_id, True) 

def test_message_pin_user_not_owner():
    user_one, user_two, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    with pytest.raises(AccessError):
        message_pinning(user_two['token'], message_id, True) 

def test_message_pin_invalid_token():
    user_one, _, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    with pytest.raises(AccessError):
        message_pinning("invalid_token", message_id, True)     

#################################################
#             Test message_unpin                #
#################################################

def test_message_unpin_dm():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    message_pinning(user_one['token'], message_id, True)
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")

    assert message_output['messages'][0]['is_pinned']
    
    assert message_pinning(user_one['token'], message_id, False) == {}
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    assert not message_output['messages'][0]['is_pinned']

def test_message_unpin_channel():    
    user_one, _, _ = register_users()
    new_chan = channels_create_v2(user_one['token'], "Channel1", True)
    
    message_id = send_group_message(user_one['token'], new_chan['channel_id'], "hi", "channel")['message_id']
    
    message_pinning(user_one['token'], message_id, True)
    
    message_output = extract_messages_from_group(user_one['token'], new_chan['channel_id'], 0, "channel")
    
    assert message_output['messages'][0]['is_pinned']
    
    assert message_pinning(user_one['token'], message_id, False) == {}
    
    message_output = extract_messages_from_group(user_one['token'], new_chan['channel_id'], 0, "channel")
    
    assert not message_output['messages'][0]['is_pinned']

def test_message_unpin_invalid_message_id():
    user_one, _, _ = register_users()
    
    with pytest.raises(InputError):
        message_pinning(user_one['token'], 987654321, False)     

def test_message_unpin_already_unpinned():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    with pytest.raises(InputError):
        message_pinning(user_one['token'], message_id, False) 
        
def test_message_unpin_user_not_member():
    user_one, user_two, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    message_pinning(user_one['token'], message_id, True)
    
    with pytest.raises(AccessError):
        message_pinning(user_two['token'], message_id, False) 

def test_message_unpin_user_not_owner():
    user_one, user_two, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    message_pinning(user_one['token'], message_id, True)
    
    with pytest.raises(AccessError):
        message_pinning(user_two['token'], message_id, False)     

def test_message_unpin_invalid_token():
    user_one, _, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [])
    
    message_id = send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")['message_id']
    
    message_pinning(user_one['token'], message_id, True)
    
    with pytest.raises(AccessError):
        message_pinning("invalid_token", message_id, False)     
