#auth_register_v2 test file

import pytest
from src.error import InputError
from src.auth import auth_register_v2
from src.other import clear_v1

###------------------------###
### Output/Action Checking ###
###------------------------###

@pytest.fixture
def clear_data():
    clear_v1()

#Tests for valid inputs
def test_valid_new_user(clear_data):
    clear_data
    login = auth_register_v2('adam.orange@gmail.com', 'validpassword', 'Adam', 'Orange')
    assert login['auth_user_id'] == 0

def test_3_valid_new_users(clear_data):
    clear_data
    login1 = auth_register_v2('john.apple@outlook.com', 'newuser1', 'John', 'Apple')
    login2 = auth_register_v2('mary_jane@yahoo.com', 'newuser2', 'Mary', 'Jane')
    login3 = auth_register_v2('dave.reallylongname@hotmail.com', 'newuser3', 'Dave', 'Path')
    login4 = auth_register_v2('john.apple2@outlook.com', 'newuser4', 'John', 'Apple')
    assert type(login1['auth_user_id']) == int
    assert type(login2['auth_user_id']) == int
    assert type(login3['auth_user_id']) == int
    assert type(login4['auth_user_id']) == int

#Tests that showcase that the stored data is correct
#is this required?

###----------------###
### Error Checking ###
###----------------###

#Tests for invalid inputs

#Test for invalid emails

#Invalid formats
def test_format_no_at():
    with pytest.raises(InputError):
        auth_register_v2('invalidformat.com', 'password1', 'Invalid', 'Email')
def test_format_no_tld():
    with pytest.raises(InputError):
        auth_register_v2('invalidformat@example', 'password2', 'Invalid', 'Email')

#Invalid Characters
def test_invalid_divider():
    with pytest.raises(InputError):
        auth_register_v2('invalid~character@example.com', 'password3', 'Invalid', 'Email')
def test_invalid_start():
    with pytest.raises(InputError):
        auth_register_v2('-invalidstart@example.com', 'password4', 'Invalid', 'Email')
def test_invalid_end():
    with pytest.raises(InputError):
        auth_register_v2('invalidend//@example.com', 'password5', 'Invalid', 'Email')

#Invalid TLD
def test_short_tld():
    with pytest.raises(InputError):
        auth_register_v2('invalid_tld@example.a', 'password6', 'Invalid', 'Email')
def test_long_tld():
    with pytest.raises(InputError):
        auth_register_v2('invalid_tld@example.abcd', 'password7', 'Invalid', 'Email')  

#Other invalid cases    
def test_email_in_use(clear_data):
    clear_data
    auth_register_v2('john.apple@outlook.com', 'newuser1', 'John', 'Apple')
    with pytest.raises(InputError):
        auth_register_v2('john.apple@outlook.com', 'password8', 'Used', 'Email')
def test_empty_email():
    with pytest.raises(InputError):
        auth_register_v2('', 'password8', 'Invalid', 'Email')

#Tests for invalid passwords
def test_short_password():
    with pytest.raises(InputError):
        auth_register_v2('short.password@example.com', 'short', 'Short', 'Password')
def test_empty_password():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', '', 'Empty', 'Password')

#Tests for invalid name_first  
def test_empty_name_first():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password10', '', 'Empty')
def test_long_name_first():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password11', 'Toooooooooooooooooooooooooooooooooooooooooooooooooo', 'Long')

#Tests for invalid name_last
def test_empty_name_last():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password12', 'Empty', '')
def test_long_name_last():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password13', 'Too', 'Loooooooooooooooooooooooooooooooooooooooooooooooong')

#Tests for both name_first and name_last
def test_empty_first_last():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password14', '', '')
def test_long_first_last():
    with pytest.raises(InputError):
        auth_register_v2('empty.password@example.com', 'password15', 'Toooooooooooooooooooooooooooooooooooooooooooooooooo', 'Loooooooooooooooooooooooooooooooooooooooooooooooong')
