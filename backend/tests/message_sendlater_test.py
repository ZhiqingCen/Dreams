from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import AccessError, InputError
from src.common import extract_messages_from_group, send_group_message
from src.dm import dm_create_v1
import pytest
from src.helper_func import extract_current_time
from src.message import message_sendlater


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

#############################################
#         Test message_sendlater            #
#############################################

def test_message_sendlater_dm():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    time_now = extract_current_time()
    
    assert "message_id" in message_sendlater(user_one['token'], new_dm['dm_id'],
        "hi", time_now + 1, "dm")
        
    message_output = extract_messages_from_group(user_one['token'], 
        new_dm['dm_id'], 0, "dm")
    
    # Confirm message is sent
    assert message_output['messages'][0]['message'] == "hi"

    # Confirm the message timestamp is correct
    assert message_output['messages'][0]['time_created'] >= time_now
    assert message_output['messages'][0]['time_created'] <= time_now + 2

def test_message_sendlater_channel():
    user_one, _, _ = register_users2()
    
    new_channel = channels_create_v2(user_one['token'], "Channel", False)
    
    time_now = extract_current_time()
    
    assert "message_id" in message_sendlater(user_one['token'], 
        new_channel['channel_id'], "hi", time_now + 1, "channel")
    
    message_output =  extract_messages_from_group(user_one['token'], 
        new_channel['channel_id'], 0, "channel")

    # Confirm message is sent
    assert message_output['messages'][0]['message'] == "hi"

    # Confirm the message timestamp is correct
    assert message_output['messages'][0]['time_created'] >= time_now
    assert message_output['messages'][0]['time_created'] <= time_now + 2

def test_message_sendlater_time_edgecase():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    time_now = extract_current_time()
    
    assert "message_id" in message_sendlater(user_one['token'], new_dm['dm_id'],
        "hi", time_now, "dm")

def test_message_sendlater_invalid_time():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    time_now = extract_current_time()
    
    with pytest.raises(InputError):
        message_sendlater(user_one['token'], new_dm['dm_id'], "hi", time_now - 1, "dm")

def test_message_sendlater_invalid_group_id():
    user_one, _, _ = register_users2()
    
    time_now = extract_current_time()
    
    with pytest.raises(InputError):
        message_sendlater(user_one['token'], 987654321, "hi", time_now + 3, "dm")
        
def test_message_sendlater_too_long():
    MAX_MESSAGE_LEN = 1000
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    time_now = extract_current_time()
    
    assert "message_id" in message_sendlater(user_one['token'], new_dm['dm_id'],
        "a" * MAX_MESSAGE_LEN, time_now + 3, "dm")
    
    with pytest.raises(InputError):
        message_sendlater(user_one['token'], new_dm['dm_id'], 
            "a" * (MAX_MESSAGE_LEN + 1), time_now + 3, "dm")

def test_message_sendlater_invalid_token():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
                user_three['auth_user_id']])
    
    time_now = extract_current_time()
    
    with pytest.raises(AccessError):
        message_sendlater("invalid_token", new_dm['dm_id'], "a", time_now + 3, "dm")

def test_message_sendlater_not_group_member():
    user_one, user_two, user_three = register_users2()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    time_now = extract_current_time()
    
    with pytest.raises(AccessError):
        message_sendlater(user_three['token'], new_dm['dm_id'], "a", time_now + 3, "dm")
