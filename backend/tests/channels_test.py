'''
test file for src/channels.py
'''
import pytest

from src.channels import channels_listall_v2, channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import AccessError, InputError

# create accounts for testing
def register_account():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    user_three = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    return user_one, user_two, user_three

###------------------------------------------------###
### channels_listall_v2(token) return { channels } ###
###------------------------------------------------###

### ----input checking---- ###
# invalid parameter empty string input token for function channels_listall_v2
def test_channels_listall_empty_token():
    with pytest.raises(AccessError):
        channels_listall_v2("")

# invalid parameter string input token for function channels_listall_v2
def test_channels_listall_invalid_token_type():
    with pytest.raises(AccessError):
        channels_listall_v2(123456789)

# input of none existing token for function channels_listall_v2
def test_channels_listall_token_not_exist():
    with pytest.raises(AccessError):
        channels_listall_v2("invalid_token!@#123")

### ----output checking---- ###
# check channels_listall output
def test_channels_listall_return():
    user_one, user_two, user_three = register_account()
    channels_create_v2(user_one["token"], "teamONE", True)
    channels_create_v2(user_two["token"], "teamTWO", False)
    channels_create_v2(user_three["token"], "teamTHREE", True)
    list_one = channels_listall_v2(user_one["token"])
    assert isinstance(list_one, dict)
    assert isinstance(list_one["channels"], list)
    assert list_one == {'channels': [{'channel_id': 0, 'name': 'teamONE'}, {'channel_id': 1, 'name': 'teamTWO'}, {'channel_id': 2, 'name': 'teamTHREE'}]}

# check when there is no channels, channels_listall return channels as empty list
def test_channels_listall_empty():
    user_one, _, _ = register_account()
    list_one = channels_listall_v2(user_one["token"])
    assert list_one == {'channels': []}

# check when there are channels, but auth_user_id not in any channels, should return all channels
def test_channels_listall_user_not_in_channels():
    user_one, user_two, _ = register_account()
    channels_create_v2(user_one["token"], "teamONE", True)
    channels_create_v2(user_two["token"], "teamTWO", False)
    list_three = channels_listall_v2(user_one["token"])
    assert list_three == {'channels': [{'channel_id': 0, 'name': 'teamONE'}, {'channel_id': 1, 'name': 'teamTWO'}]}


###------------------------------------------------------------------###
### channels_create_v2(token, name, is_public) return { channel_id } ###
###------------------------------------------------------------------###

### ----input checking---- ###
# invalid parameter input token for function channels_create_v2
def test_channels_create_empty_token():
    with pytest.raises(AccessError):
        channels_create_v2("", "name", True)
    
def test_channels_create_invalid_token_type():
    with pytest.raises(AccessError):
        channels_create_v2(123456789, "name", True)

# invalid parameter input token with not existing id for function channels_create_v2
def test_channels_create_token_not_exist():
    with pytest.raises(AccessError):
        channels_create_v2("invalid_user_id!@#123", "name", True)

# invalid parameter empty string input name for function channels_create_v2
def test_channels_create_empty_name():
    user_one, _, _ = register_account()
    with pytest.raises(InputError):
        channels_create_v2(user_one["token"],"", True)

# invalid parameter input name for function channels_create_v2
def test_channels_create_invalid_name():
    user_one, _, _ = register_account()
    with pytest.raises(InputError):
        channels_create_v2(user_one["token"],123, True)

# invalid parameter input name exceed 20 characters for function channels_create_v2
def test_channels_create_exceed_length_limit_name():
    user_one, _, _ = register_account()
    with pytest.raises(InputError):
        # Name <= 20 characters
        channels_create_v2(user_one["token"], "a"*21, True)

# invalid parameter empty string input is_public for function channels_create_v2
def test_channels_create_empty_is_public():
    user_one, _, _ = register_account()
    with pytest.raises(InputError):
        channels_create_v2(user_one["token"], "name", "")

# invalid parameter string input is_public for function channels_create_v2
def test_channels_create_invalid_is_public():
    user_one, _, _ = register_account()
    with pytest.raises(InputError):
        channels_create_v2(user_one["token"], "name", "public!@#123")

# other wrong parameter input for function channels_create_v2
def test_channels_create_other_invalid_input():
    with pytest.raises(AccessError):
        channels_create_v2("","","")

### ----output checking---- ###
# check channels_create output
def test_channels_create_return():
    user_one, _, _ = register_account()
    team_one = channels_create_v2(user_one["token"], "teamONE", True)
    assert isinstance(team_one, dict)
    assert isinstance(team_one["channel_id"], int)
    assert team_one == {'channel_id': 0}