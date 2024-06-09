import pytest
from src.error import InputError
from src.auth import auth_register_v2, auth_login_v2
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

#Test with a valid input
def test_full_pass(clear_data):
    clear_data
    john = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    mary = auth_register_v2('mary_jane@example.com', 'password2', 'Mary', 'Jane')
    login1 = auth_login_v2('john.apple@example.com', 'password1')
    login2 = auth_login_v2('mary_jane@example.com', 'password2')
    assert john['auth_user_id'] == login1['auth_user_id']
    assert mary['auth_user_id'] == login2['auth_user_id']

###----------------###
### Error Checking ###
###----------------###

#Tests for invalid passwords
def test_wrong_password():
    with pytest.raises(InputError):
        auth_login_v2('john.apple@example.com', 'wrongpassword')

def test_switched_passwords():
    with pytest.raises(InputError):
        auth_login_v2('john.apple@example.com', 'password2')

def test_empty_password():
    with pytest.raises(InputError):
        auth_login_v2('john.apple@example.com', '')

#Tests for invalid emails
def test_incorrect_email():
    with pytest.raises(InputError):
        auth_login_v2('dave.path@example.com', 'password3')

def test_no_at_sign():
    with pytest.raises(InputError):
        auth_login_v2('invalidformat.com', 'password4')

def test_invalid_divider_char():
    with pytest.raises(InputError):
        auth_login_v2('invalid~character@example.com', 'password5')

def test_invalid_start_char():
    with pytest.raises(InputError):
        auth_login_v2('-invalidstart@example.com', 'password6')

def test_invalid_end_char():
    with pytest.raises(InputError):
        auth_login_v2('invalidend//@example.com', 'password7')

def test_short_tld():
    with pytest.raises(InputError):
        auth_login_v2('invalid_tld@example.a', 'password8')

def test_long_tld():
    with pytest.raises(InputError):
        auth_login_v2('invalid_tld@example.abcd', 'password9')

def test_empty_email():
    with pytest.raises(InputError):
        auth_login_v2('','password10')
