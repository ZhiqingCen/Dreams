import pytest
from src.error import InputError
from src.auth import auth_register_v2, auth_logout_v1
from src.other import clear_v1

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def clear_data():
    clear_v1()

def test_pass(clear_data):
    clear_data
    login = auth_register_v2('adam.orange@gmail.com', 'validpassword', 'Adam', 'Orange')
    assert auth_logout_v1(login['token'])['is_success'] == True

def test_invalid_token(clear_data):
    clear_data

    assert auth_logout_v1('invalid_token')['is_success'] == False