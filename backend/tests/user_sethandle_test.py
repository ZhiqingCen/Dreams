import pytest
from src.error import InputError, AccessError
from src.auth import auth_login_v2, auth_register_v2
from src.user import user_profile_sethandle_v1, user_profile_v2
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
    user_profile_sethandle_v1(login['token'], 'newhandle')
    user_dict = user_profile_v2(login['token'], 0)
    user = user_dict['user']
    assert user['handle_str'] == 'newhandle'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token(clear_data):
    clear_data
    auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(AccessError):
        user_profile_sethandle_v1('invalid_token', 'newhandle')

def test_short_handle(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(login['token'], 'ts')

def test_long_handle(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(login['token'], 21*'L')

def test_handle_in_use(clear_data):
    clear_data
    auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    auth_register_v2('mary_jane@yahoo.com', 'password2', 'Mary', 'Jane')
    login = auth_login_v2('john.apple@example.com', 'password1')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(login['token'], 'maryjane')