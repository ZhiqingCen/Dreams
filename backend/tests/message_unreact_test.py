'''
test file for src/message_unreact_v1
'''
import pytest

from src.message import message_react_v1, message_unreact_v1
from src.common import send_group_message, extract_messages_from_group
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError, InputError
from json import loads

###-----------------------------------------------------------###
### message_unreact_v1(token, message_id, react_id) return {} ###
###-----------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_unreact_v1
def test_message_unreact_empty_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_unreact_v1("", message_one["message_id"], 1)

# invalid parameter None input token for function message_unreact_v1
def test_message_unreact_none_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_unreact_v1(None, message_one["message_id"], 1)

# invalid parameter string input token for function message_unreact_v1
def test_message_unreact_invalid_token_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_unreact_v1(123456789, message_one["message_id"], 1)

# input of none existing token for function message_unreact_v1
def test_message_unreact_token_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_unreact_v1("invalid_token", message_one["message_id"], 1)

# invalid parameter None input message_id for function message_unreact_v1
def test_message_unreact_none_message_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], None, 1)

# invalid parameter string input message_id for function message_unreact_v1
def test_message_unreact_invalid_message_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], "invalid_message_id", 1)

# input of none existing message_id for function message_unreact_v1
def test_message_unreact_message_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], 123456789, 1)

# invalid parameter None input react_id for function message_unreact_v1
def test_message_unreact_none_react_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], message_one["message_id"], None)

# invalid parameter string input react_id for function message_unreact_v1
def test_message_unreact_invalid_react_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], message_one["message_id"], "invalid_react_id")

# input of none existing react_id for function message_unreact_v1
def test_message_unreact_react_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_unreact_v1(user_one["token"], message_one["message_id"], 2)

# user trying to unreact channel message but not a channel member for function message_unreact_v1
def test_message_unreact_not_channel_member():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_unreact_v1(user_two["token"], message_one["message_id"], 1)

# user trying to unreact dm message but not a dm member for function message_unreact_v1
def test_message_unreact_not_dm_member():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    user_three = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    with pytest.raises(AccessError):
        message_unreact_v1(user_three["token"], dm_message_one["message_id"], 1)

# user trying to unreact message that had not been reacted before for function message_unreact_v1
def test_message_unreact_not_reacted_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_two['token'], public_channel['channel_id'])
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_unreact_v1(user_two["token"], message_one["message_id"], 1)

### ----output checking---- ###
# user unreact to channel message with react exists for function message_unreact_v1
def test_message_unreact_channel_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    channel_join_v2(user_two['token'], public_channel['channel_id'])
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    message_react_v1(user_two["token"], message_one["message_id"], 1)
    message_unreact_v1(user_two["token"], message_one["message_id"], 1)
    get_messages =  extract_messages_from_group(user_two["token"], public_channel['channel_id'], 0, "channel")
    react = [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}]
    assert react in [message['reacts'] for message in get_messages['messages']]

# user unreact to dm message with react exists for function message_unreact_v1
def test_message_unreact_dm_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    message_react_v1(user_one["token"], dm_message_one["message_id"], 1)
    message_unreact_v1(user_one["token"], dm_message_one["message_id"], 1)
    get_messages =  extract_messages_from_group(user_one["token"], dm_one['dm_id'], 0, "dm")
    react = [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}]
    assert react in [message['reacts'] for message in get_messages['messages']]
