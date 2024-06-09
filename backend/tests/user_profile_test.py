import pytest
from src.error import InputError, AccessError
from src.auth import auth_login_v2, auth_register_v2
from src.user import user_profile_v2
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
    assert user_profile_v2(login['token'], 0) == {
        'user': {
            'u_id': 0,
            'email': 'john.apple@example.com',
            'name_first': 'John',
            'name_last': 'Apple',
            'handle_str': 'johnapple',
            'profile_img_url': 'imgurl/default.jpg'
        }
    }

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token(clear_data):
    clear_data
    auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(AccessError):
        user_profile_v2('invalid_token', 0)

def test_invalid_u_id(clear_data):
    clear_data
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_v2(login['token'],  999)