import requests
import json
from src import config
from src.error import INPUT_ERROR

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

def register_users(): 
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
    
def test_search_empty():
    '''
    Check that a search result will return the appropriate output if no messages
    match the search query.
    '''
    user_one, user_two, _ = register_users()
    
    requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    
    # Search for a query_str which does not exist
    r = requests.get(config.url + "search/v2", params = {
        "token": user_one["token"],
        "query_str": "hey"
    })
    
    # Comfirm there are no messges output 
    assert r.json() == {"messages" : []}

def test_search_output_dm():
    '''
    Have 3 users search for a query under different conditions; dm owner, 
    dm member or not a member and ensure only autherised users can view message 
    outputs
    '''
    user_one, user_two, user_three = register_users()
    
    # Create group with owner user_one and member user_two and send a message in that dm.
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "hi"
    })
    
    # Have users 1, 2 and 3 serach for the message
    r = requests.get(config.url + "search/v2", params = {
        "token": user_one["token"],
        "query_str": "hi"
    })
    search_results1 = r.json()
    
    r = requests.get(config.url + "search/v2", params = {
        "token": user_two["token"],
        "query_str": "hi"
    })
    search_results2 = r.json()
    
    r = requests.get(config.url + "search/v2", params = {
        "token": user_three["token"],
        "query_str": "hi"
    })
    search_results3 = r.json()
    
    # Ensure only user_one and user_two can view the message
    assert "hi" in [message['message'] for message in search_results1['messages']]
    assert "hi" in [message['message'] for message in search_results2['messages']]
    assert not "hi" in [message['message'] for message in search_results3['messages']]
    
    # Check search output keys and types
    assert isinstance(search_results1['messages'][0]["message_id"], int)
    assert isinstance(search_results1['messages'][0]["u_id"], int)
    assert isinstance(search_results1['messages'][0]["message"], str)
    assert isinstance(search_results1['messages'][0]["time_created"], int)
    assert isinstance(search_results1['messages'][0]["is_pinned"], bool)
    
    
def test_search_v1_output_channel():
    user_one, user_two, user_three = register_users()
    
    r = requests.post(config.url + "channels/create/v2", json = {
        "token": user_one["token"],
        "name": "Channel",
        "is_public": False
    })
    new_channel = r.json()
    
    requests.post(config.url + "channel/invite/v2", json = {
        "token": user_one["token"],
        "channel_id": new_channel['channel_id'],
        "u_id": user_two['auth_user_id']
    })
    
    requests.post(config.url + "message/send/v2", json = {
        "token": user_one["token"],
        "channel_id": new_channel['channel_id'],
        "message": "hi"
    })
    
    # Have users 1, 2 and 3 serach for the message
    r = requests.get(config.url + "search/v2", params = {
        "token": user_one["token"],
        "query_str": "hi"
    })
    search_results1 = r.json()
    
    r = requests.get(config.url + "search/v2", params = {
        "token": user_two["token"],
        "query_str": "hi"
    })
    search_results2 = r.json()
    
    r = requests.get(config.url + "search/v2", params = {
        "token": user_three["token"],
        "query_str": "hi"
    })
    search_results3 = r.json()
    
    # Check only users 1 and 2 can view the message, as they are the only channel members
    assert "hi" in [message['message'] for message in search_results1['messages']]
    assert "hi" in [message['message'] for message in search_results2['messages']]
    assert not "hi" in [message['message'] for message in search_results3['messages']]
     
def test_search_v1_query_too_long():
    '''
    Check that a message of MAX_QUERY_LEN can be searched for and returned and 
    that any query longer than MAX_QUERY_LEN will raise an INPUT_ERROR
    '''
    MAX_QUERY_LEN = 1000
    
    user_one, user_two, _ = register_users()
    
    # Create group with owner user_one and member user_two and send a message in that dm.
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"]]
    })
    new_dm = r.json()
    
    requests.post(config.url + "message/senddm/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"],
        "message": "a" * MAX_QUERY_LEN
    })
    
    # Check message with MAX_QUERY_LEN can be viewed
    r = requests.get(config.url + "search/v2", params = {
        "token": user_one["token"],
        "query_str": "a" * MAX_QUERY_LEN
    })
    search_results = r.json()
    
    assert ("a" * MAX_QUERY_LEN) in [message['message'] for message in search_results['messages']]
    
    # Check InputError raised if query > MAX_QUERY_LEN
    r = requests.get(config.url + "search/v2", params = {
        "token": user_one["token"],
        "query_str": "a" * (MAX_QUERY_LEN + 1)
    })
    
    assert r.status_code == INPUT_ERROR