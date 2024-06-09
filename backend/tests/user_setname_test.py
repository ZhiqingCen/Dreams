import pytest
from src.error import InputError, AccessError
from src.auth import auth_login_v2, auth_register_v2
from src.user import user_profile_setname_v2, user_profile_v2
from src.other import clear_v1

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def clear_data():
    clear_v1()

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_basic_pass(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    user_profile_setname_v2(login['token'], 'Darcy', 'Bold')
    user_dict = user_profile_v2(login['token'], 0)
    user = user_dict['user']
    assert user['name_first'] == 'Darcy' and user['name_last'] == 'Bold'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token(clear_data):
    clear_data
    
    with pytest.raises(AccessError):
        user_profile_setname_v2('invalid_token', 'Darcy', 'Bold')

def test_short_firstname(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_setname_v2(login['token'],  '', 'tooshort')

def test_short_lastname(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_setname_v2(login['token'], 'tooshort', '')

def test_long_firstname(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_setname_v2(login['token'],  51*'L', 'toolong')

def test_long_lastname(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_setname_v2(login['token'], 'toolong', 51*'L')

def test_name_is_removed_user(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'Removed', 'User')
    with pytest.raises(InputError):
        user_profile_setname_v2(login['token'], 'Removed', 'user')