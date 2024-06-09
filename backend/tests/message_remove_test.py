'''
test file for src/message_remove_v1.py
'''
from src.helper_func import load_database
import pytest

from src.message import message_remove_v1#, message_senddm_v1
from src.common import send_group_message
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError, InputError
from json import loads

###-------------------------------------------------###
### message_remove_v1(token, message_id) return { } ###
###-------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_remove_v1
def test_message_remove_empty_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1("", message_one["message_id"])

# invalid parameter None input token for function message_remove_v1
def test_message_remove_none_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1(None, message_one["message_id"])

# invalid parameter string input token for function message_remove_v1
def test_message_remove_invalid_token_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1(123456789, message_one["message_id"])

# input of none existing token for function message_remove_v1
def test_message_remove_token_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1("invalid_token", message_one["message_id"])

# invalid parameter None input message_id for function message_remove_v1
def test_message_remove_none_message_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_remove_v1(user_one["token"], None)

# invalid parameter string input message_id for function message_remove_v1
def test_message_remove_invalid_message_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_remove_v1(user_one["token"], "invalid_message_id")

# input of none existing message_id for function message_remove_v1
def test_message_remove_message_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_remove_v1(user_one["token"], 123456789)

# input of non-sender trying to remove message for function message_remove_v1
def test_message_remove_non_sender():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_two['token'], public_channel['channel_id'])
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1(user_two["token"], message_one["message_id"])

# input of non-channel_owner tring to delete message from channel for function message_remove_v1
def test_message_remove_non_channel_owner():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_three = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_three['token'], public_channel['channel_id'])
    message_one = send_group_message(user_three["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_remove_v1(user_three["token"], message_one["message_id"])

# input of non-channel_owner tring to delete message from dm for function message_remove_v1
def test_message_remove_non_dm_owner():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_two["token"], dm_one["dm_id"], "first message", "dm")
    with pytest.raises(AccessError):
        message_remove_v1(user_two["token"], dm_message_one["message_id"])

### ----output checking---- ###
# check message_remove_v1 output for channel_message
def test_message_remove_channel_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    message_remove_v1(user_one["token"], message_one["message_id"])
    data = load_database()
    messages = data["messages"]
    assert messages == []

# check message_remove_v1 output for dm_message
def test_message_remove_dm_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    message_remove_v1(user_one["token"], dm_message_one["message_id"])
    data = load_database()
    messages = data["messages"]
    assert messages == []
