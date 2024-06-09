import pytest
from src.auth import auth_passwordreset_reset_v1
from src.error import InputError

# It is impossible to test if this code functions fully without accessing your email

###----------------###
### Error Checking ###
###----------------###

def test_invalid_reset_code():
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1('invalid code', 'validpassword')

def test_password_too_short():
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1('Valid Code', 'short')