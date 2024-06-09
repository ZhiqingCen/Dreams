from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import AccessError, InputError
from src.dm import dm_create_v1, dm_remove_v1
from src.user import users_all_v1
from src.common import list_groups
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

def extract_dm_name(dm_members):
    users = users_all_v1(dm_members[0]['token'])['users']
    user_handles = []
    
    for user in users:
        for member in dm_members:
            if user['u_id'] == member['auth_user_id']:
                user_handles.append(user['handle_str'])
    
    user_handles.sort()
    dm_name = ", ".join(user_handles)
    
    return dm_name

## Testing dm_create_v1 output ##
def test_dm_create_v1():
    user_one, user_two, user_three = register_users()
    
    dm_name = extract_dm_name([user_one, user_two, user_three])
    
    assert dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
        user_three['auth_user_id']]) == {'dm_id': 0, 'dm_name': dm_name}
        
    dm_name = extract_dm_name([user_one, user_two])
    
    assert dm_create_v1(user_two['token'], [user_one['auth_user_id']]) ==  {'dm_id'
        : 1, 'dm_name': dm_name}
        
## Testing dm_create_v1 AccessError ## 
def test_dm_create_v1_invalid_token():
    user_one, _, _ = register_users()   
    with pytest.raises(AccessError):
        dm_create_v1("invalid_token", [user_one['auth_user_id']])
       

## Testing dm_create_v1 InputError ##   
def test_dm_create_v1_invalid_user_id():
    user_one, user_two, _ = register_users()   
    with pytest.raises(InputError):
        dm_create_v1(user_one['token'], [user_two['auth_user_id'], 98765432])       
       
## Testing dm_remove_v1 output ##
def test_dm_remove_v1():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
        user_three['auth_user_id']])
    
    # Check dm_remove_v1 output
    assert dm_remove_v1(user_one['token'], new_dm['dm_id']) == {}
    
    # Check dm_remove_v1 sucessfully removed the dm
    assert list_groups(user_one['token'], "dm") == {'dms': []}
    
## Testing dm_remove_v1 InputError ##
def test_dm_remove_v1_invalid_dm_id():
    user_one, _, _ = register_users()
    
    with pytest.raises(InputError):
        dm_remove_v1(user_one['token'], 987654321)     
    
## Testing dm_remove_v1 AccessError ##
def test_dm_remove_v1_invalid_token():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
        user_three['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_remove_v1("invalid_token", new_dm["dm_id"])
        
def test_dm_remove_v1_non_owner():
    user_one, user_two, user_three = register_users()
    
    new_dm = dm_create_v1(user_one['token'], [user_two['auth_user_id'], 
        user_three['auth_user_id']])
    
    # Access Error should be raised since user_two is not the owner of new_dm
    with pytest.raises(AccessError):
        dm_remove_v1(user_two['token'], new_dm["dm_id"])             
    

