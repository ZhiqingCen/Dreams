'''
test file for src/message_edit_v2.py
'''
import pytest
from src.helper_func import load_database
from src.message import message_edit_v2
from src.common import send_group_message, list_groups
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError, InputError
from json import loads

###-------------------------------------------------------###
### message_edit_v2(token, message_id, message) return {} ###
###-------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_edit_v2
def test_message_edit_empty_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2("", message_one["message_id"], "new_message")

# invalid parameter None input token for function message_edit_v2
def test_message_edit_none_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2(None, message_one["message_id"], "new_message")

# invalid parameter string input token for function message_edit_v2
def test_message_edit_invalid_token_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2(123456789, message_one["message_id"], "new_message")

# input of none existing token for function message_edit_v2
def test_message_edit_token_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2("invalid_token", message_one["message_id"], "new_message")

# input of non-sender trying to edit message for function message_edit_v2
def test_message_edit_non_sender():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2(user_two["token"], message_one["message_id"], "new_message")

# invalid parameter None input message_id for function message_edit_v2
def test_message_edit_none_message_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], None, "new_message")

# invalid parameter string input message_id for function message_edit_v2
def test_message_edit_invalid_message_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], "invalid_message_id", "new_message")

# input of none existing message_id for function message_edit_v2
def test_message_edit_message_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], 123456789, "new_message")

# invalid parameter None input message for function message_edit_v2
def test_message_edit_none_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], message_one["message_id"], None)

# invalid parameter string input message for function message_edit_v2
def test_message_edit_invalid_message_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], message_one["message_id"], 123456789)

# invalid parameter input message exceed 1000 characters for function message_edit_v2
def test_message_edit_exceed_length_limit_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_edit_v2(user_one["token"], message_one["message_id"], "a"*1001)

# input of non-channel_owner tring to edit message from channel for function message_remove_v1
def test_message_edit_non_channel_owner():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_three = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_three['token'], public_channel['channel_id'])
    message_two = send_group_message(user_three["token"], public_channel["channel_id"], "second message", "channel")
    with pytest.raises(AccessError):
        message_edit_v2(user_three["token"], message_two["message_id"], "new_message")

### ----output checking---- ###
# check message_edit_v2 output, input empty message
def test_message_edit_empty_channel_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    message_edit_v2(user_one["token"], message_one["message_id"], "")
    data = load_database()
    assert data["messages"] == []

# check message_edit_v2 output for channel_message
def test_message_edit_channel_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    message_edit_v2(user_one["token"], message_one["message_id"], "new_message")
    data = load_database()
    messages = data["messages"]
    assert len(messages) == 1
    assert messages[0]["message"] == "new_message"

# check message_edit_v2 output, input empty message
def test_message_edit_empty_dm_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    message_edit_v2(user_one["token"], dm_message_one["message_id"], "")
    data = load_database()
    assert data["messages"] == []

# check message_edit_v2 output for channel_message
def test_message_edit_dm_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    message_edit_v2(user_one["token"], dm_message_one["message_id"], "new_message")
    data = load_database()
    messages = data["messages"]
    assert len(messages) == 1
    assert messages[0]["message"] == "new_message"
