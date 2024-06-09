import pytest
from src.auth import auth_register_v2, auth_passwordreset_request_v1
from src.error import InputError
from src.other import clear_v1

###-------------###
### Test Set Up ###
###-------------###

@pytest.fixture
def clear_data():
    clear_v1()

# It is impossible to test if this code functions fully without accessing your email
def test_runs():
    clear_data
    auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    auth_passwordreset_request_v1('john.apple@example.com')
    assert True == True
# Tests that the function runs


###----------------###
### Error Checking ###
###----------------###

def test_email_not_registered():
    with pytest.raises(InputError):
        auth_passwordreset_request_v1('not_registered@email.com')
