import requests
import pytest
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR

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
def register_users(): 
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

def extract_dm_name(dm_members):
    resp = requests.get(config.url + "users/all/v1", params = {
        "token": dm_members[0]["token"]
    })
    
    users = resp.json()['users']
    user_handles = []
    
    for user in users:
        for member in dm_members:
            if user["u_id"] == member["auth_user_id"]:
                user_handles.append(user["handle_str"])
    
    user_handles.sort()
    dm_name = ", ".join(user_handles)
    
    return dm_name

# ----------------------------- #
#         dm/create/v1          #
# ----------------------------- #

def test_dm_create(register_users):
    """
    A test to check dm/create/v1 
    """
    user_one, user_two, user_three = register_users

    resp = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two['auth_user_id'], user_three['auth_user_id']]
    })

    dm_create_output = resp.json()

    dm_name = extract_dm_name([user_one, user_two, user_three])
    
    assert dm_create_output["dm_name"] == dm_name
    assert isinstance(dm_create_output["dm_id"], int)
  
    
def test_dm_create_invalid_token(register_users):
    user_one, _, _ = register_users 
     
    resp = requests.post(config.url + "dm/create/v1", json = {
        "token": "invalid_token",
        "u_ids": [user_one["auth_user_id"]]
    }) 
     
    assert resp.status_code == ACCESS_ERROR
  
def test_dm_create_invalid_user_id(register_users):
    user_one, user_two, _ = register_users  
     
    resp = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], 987654321]
    }) 
     
    assert resp.status_code == INPUT_ERROR    

# ----------------------------- #
#         dm/remove/v1          #
# ----------------------------- #   

## Testing dm_remove output ##
def test_dm_remove(register_users):
    user_one, user_two, user_three = register_users
    
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json() 
    resp = requests.delete(config.url + "dm/remove/v1", json = {
        "token": user_one["token"],
        "dm_id": new_dm["dm_id"]
    })
    
    # Check dm/remove/v1 output
    assert resp.json() == {}
    
    resp = requests.get(config.url + "dm/list/v1", params = {
        "token": user_one["token"]
    })
    
    # Check dm_remove sucessfully removed the dm
    assert resp.json() == {"dms": []}
    
## Testing dm_remove InputError ##
def test_dm_remove_invalid_dm_id(register_users):
    user_one, _, _ = register_users
    
    resp = requests.delete(config.url + "dm/remove/v1", json = {
        "token": user_one["token"],
        "dm_id": 987654321
    })
    
    assert resp.status_code == INPUT_ERROR    
    
## Testing dm_remove AccessError ##
def test_dm_remove_invalid_token(register_users):
    user_one, user_two, user_three = register_users
    
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json() 
    resp = requests.delete(config.url + "dm/remove/v1", json = {
        "token": "invalid_token",
        "dm_id": new_dm["dm_id"]
    })
    
    assert resp.status_code == ACCESS_ERROR
        
def test_dm_remove_non_owner(register_users):
    user_one, user_two, user_three = register_users
    
    r = requests.post(config.url + "dm/create/v1", json = {
        "token": user_one["token"],
        "u_ids": [user_two["auth_user_id"], user_three["auth_user_id"]]
    })
    new_dm = r.json() 
    resp = requests.delete(config.url + "dm/remove/v1", json = {
        "token": user_two["token"],
        "dm_id": new_dm["dm_id"]
    })
    
    assert resp.status_code == ACCESS_ERROR       

