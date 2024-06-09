'''
test file for src/extra_features
'''
import pytest

from src.extra_features import group_rename
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.common import group_details
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError, InputError
from json import loads

###---------------------------------------------------------###
### group_rename(token, name, group_id, group_type) return {} ###
###---------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function group_rename
def test_group_rename_empty_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(AccessError):
        group_rename("", "new_name", public_channel["channel_id"], "channel")

# invalid parameter None input token for function group_rename
def test_group_rename_none_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(AccessError):
        group_rename(None, "new_name", public_channel["channel_id"], "channel")

# invalid parameter string input token for function group_rename
def test_group_rename_invalid_token_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(AccessError):
        group_rename(123456789, "new_name", public_channel["channel_id"], "channel")

# input of none existing token for function group_rename
def test_group_rename_token_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(AccessError):
        group_rename("invalid_token", "new_name", public_channel["channel_id"], "channel")

# invalid parameter None input name for function group_rename
def test_group_rename_none_name():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], None, public_channel["channel_id"], "channel")

# invalid parameter string input name for function group_rename
def test_group_rename_invalid_name_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], 123456789, public_channel["channel_id"], "channel")

# input of name exceed 20 characters for function group_rename
def test_group_rename_name_too_long():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], "a"*21, public_channel["channel_id"], "channel")

# invalid parameter None input group_id for function group_rename
def test_group_rename_none_group_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", None, "channel")

# invalid parameter string input group_id for function group_rename
def test_group_rename_invalid_group_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", "invalid_channel_id", "channel")

# input of none existing group_id for function group_rename
def test_group_rename_group_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", 123456789, "channel")

# invalid parameter None input group_type for function group_rename
def test_group_rename_none_group_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", public_channel["channel_id"], None)

# invalid parameter string input group_type for function group_rename
def test_group_rename_invalid_group_type_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", public_channel["channel_id"], "dm")

# input of none existing token for function group_rename
def test_group_rename_group_type_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        group_rename(user_one["token"], "new_name", public_channel["channel_id"], "invalid")

# non channel owner trying to rename channel for function group_rename
def test_group_rename_non_channel_owner():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_three = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_three['token'], public_channel['channel_id'])
    with pytest.raises(AccessError):
        group_rename(user_three["token"], "new_name", public_channel["channel_id"], "channel")

# non dm owner trying to rename dm for function group_rename
def test_group_rename_non_dm_owner():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    with pytest.raises(AccessError):
        group_rename(user_two["token"], "new_name", dm_one["dm_id"], "dm")

### ----output checking---- ###
# channel owner trying to rename channel for function group_rename
def test_group_rename_change_channel_name():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    group_rename(user_one["token"], "new_name", public_channel["channel_id"], "channel")
    data = group_details(user_one["token"], public_channel["channel_id"], "channel")
    assert data["name"] == 'new_name'

# dm owner trying to rename dm for function group_rename
def test_group_rename_change_dm_name():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    group_rename(user_one["token"], "new_name", dm_one["dm_id"], "dm")
    data = group_details(user_one["token"], dm_one["dm_id"], "dm")
    assert data["name"] == 'new_name'