import pytest
from src.error import InputError, AccessError
from src.auth import auth_login_v2, auth_register_v2
from src.user import user_profile_uploadphoto_v1, user_profile_v2
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
    user_profile_uploadphoto_v1(login['token'], 'https://www.501commons.org/donate/Heart.jpg/image_preview', 0, 0, 200, 400)
    user_dict = user_profile_v2(login['token'], 0)
    user = user_dict['user']
    assert user['profile_img_url'] != 'imgurl/default.jpg'

###----------------###
### Error Checking ###
###----------------###

def test_invalid_token(clear_data):
    clear_data
    with pytest.raises(AccessError):
        user_profile_uploadphoto_v1('invalid_token', 'https://www.501commons.org/donate/Heart.jpg/image_preview', 0, 0, 200, 400)

def test_not_jpg(clear_data):
    clear_data
    
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(login['token'], 'https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png', 0, 0, 200, 400)
    
def test_invalid_crop1(clear_data):
    clear_data
    
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(login['token'], 'https://www.501commons.org/donate/Heart.jpg/image_preview', 0, 0, 600, 500)

def test_invalid_crop2(clear_data):
    clear_data
    
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(login['token'], 'https://www.501commons.org/donate/Heart.jpg/image_preview', -100, 0, 200, 300)

def test_invalid_crop3(clear_data):
    clear_data
    
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(login['token'], 'https://www.501commons.org/donate/Heart.jpg/image_preview', 200, 200, 100, 100)

'''
A different error code will always be spit before my InputError since the library has its own errors for invalid URL
def test_invalid_url(clear_data):
    clear_data
    
    login = auth_register_v2('john.apple@example.com', 'password1', 'John', 'Apple')
    with pytest.raises(InputError):
        user_profile_uploadphoto_v1(login['token'], 'https://www.notavalidwebsiteatall.com', 0, 0, 200, 400)'''