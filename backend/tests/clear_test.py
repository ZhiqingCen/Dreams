import pytest

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.other import clear_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.error import InputError, AccessError

###-------------###
### Test Set Up ###
###-------------###

def register_users():
    user_one = auth_register_v2("address1@email.com", "onetwothree", "User1", "One")
    return user_one

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_users_cleared():
    
    ## Add user to the list of registered users.
    user_one = register_users()
    
    
    ## Check that user_one is stored in register.
    assert auth_login_v2("address1@email.com", "onetwothree")['auth_user_id'] \
        == user_one['auth_user_id']
    
    clear_v1()
    
    ## Check that the user profile cannot be found after cleared
    with pytest.raises(InputError):
        auth_login_v2("address1@email.com", "onetwothree")


def test_channels_cleared():
    
    ## Add user to the list of registered users.
    user_one = register_users()
    
    ## Create channels
    channels_create_v2(user_one['token'], "Test Channel_1", True)
    channels_create_v2(user_one['token'], "Test Channel_2", False)
    
    clear_v1()
    
    ## Re-register a user
    user_one = register_users()

    ## Confirm Test Channels have been cleared
    assert channels_listall_v2(user_one['token']) == {'channels':[]}
    assert channels_listall_v2(user_one['token']) == {'channels':[]}

def test_channels_clear_output():
    assert clear_v1() == {}
