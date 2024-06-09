from src.common import send_group_message, invite_to_group
from src.other import search_v2, clear_v1
from src.dm import dm_create_v1
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.error import InputError
import pytest


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

def register_users(): 
    clear_v1()
    global user1, user2, user3
    user_one = auth_register_v2(user1['email'], "qwerty1", user1['name_first'], 
        user1['name_last'])
    user_two = auth_register_v2(user2['email'], "qwerty2", user2['name_first'], 
        user2['name_last'])
    user_three = auth_register_v2(user3['email'], "qwerty3", user3['name_first'], 
        user3['name_last'])
    
    user1['u_id'] = user_one['auth_user_id']
    user2['u_id'] = user_two['auth_user_id']
    user3['u_id'] = user_three['auth_user_id']
    
    return user_one, user_two, user_three

def test_search_empty():
    user_one, user_two, _ = register_users()
    
    _ = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    assert search_v2(user_one['token'], "hey") == {"messages" : []}

def test_search_output_dm():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    send_group_message(user_one['token'], new_dm['dm_id'], "hi", "dm")
    
    search_results1 = search_v2(user_one['token'], "hi")
    search_results2 = search_v2(user_two['token'], "hi")
    search_results3 = search_v2(user_three['token'], "hi")
    
    assert "hi" in [message['message'] for message in search_results1['messages']]
    assert "hi" in [message['message'] for message in search_results2['messages']]
    assert not "hi" in [message['message'] for message in search_results3['messages']]
    
    
def test_search_output_channel():
    user_one, user_two, user_three = register_users()
    
    new_channel = channels_create_v2(user_one['token'], "Channel", False)
    invite_to_group(user_one['token'], new_channel['channel_id'], user_two['auth_user_id'], 'channel')
    
    send_group_message(user_one['token'], new_channel['channel_id'], "hi", "channel")
    
    search_results1 = search_v2(user_one['token'], "hi")
    search_results2 = search_v2(user_two['token'], "hi")
    search_results3 = search_v2(user_three['token'], "hi")
    
    assert "hi" in [message['message'] for message in search_results1['messages']]
    assert "hi" in [message['message'] for message in search_results2['messages']]
    assert not "hi" in [message['message'] for message in search_results3['messages']]
    
     # Check search output keys and types
    assert isinstance(search_results1['messages'][0]["message_id"], int)
    assert isinstance(search_results1['messages'][0]["u_id"], int)
    assert isinstance(search_results1['messages'][0]["message"], str)
    assert isinstance(search_results1['messages'][0]["time_created"], int)
    assert isinstance(search_results1['messages'][0]["is_pinned"], bool)
    
def test_search_query_too_long():
    user_one, user_two, _ = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id']])
    
    send_group_message(user_one['token'], new_dm['dm_id'], "a" * 1000, "dm")
    
    search_results = search_v2(user_one['token'], "a" * 1000)
    
    assert ("a" * 1000) in [message['message'] for message in search_results['messages']]
    
    with pytest.raises(InputError):
        search_v2(user_one['token'], "a" * 1001)