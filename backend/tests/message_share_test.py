'''
test file for src/message_share_v1.py
'''
import pytest

from src.message import message_share_v1#, message_senddm_v1
from src.common import send_group_message
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError, InputError

###-------------------------------------------------------------------------------------------------###
### message_share_v1(token, og_message_id, message, channel_id, dm_id) return { shared_message_id } ###
###-------------------------------------------------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function message_share_v1
def test_message_share_empty_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_share_v1("", message_one["message_id"], "message", public_channel["channel_id"], -1)

# invalid parameter None input token for function message_share_v1
def test_message_share_none_token():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_share_v1(None, message_one["message_id"], "message", public_channel["channel_id"], -1)

# invalid parameter string input token for function message_share_v1
def test_message_share_invalid_token_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_share_v1(123456789, message_one["message_id"], "message", public_channel["channel_id"], -1)

# input of none existing token for function message_share_v1
def test_message_share_token_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_share_v1("invalid_token", message_one["message_id"], "message", public_channel["channel_id"], -1)

# invalid parameter None input og_message_id for function message_share_v1
def test_message_share_none_og_message_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], None, "message", public_channel["channel_id"], -1)

# invalid parameter string input og_message_id for function message_share_v1
def test_message_share_invalid_og_message_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], "invalid_message_id", "message", public_channel["channel_id"], -1)

# input of none existing og_message_id for function message_share_v1
def test_message_share_og_message_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    # message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], 123456789, "message", public_channel["channel_id"], -1)

# invalid parameter None input message for function message_share_v1
def test_message_share_none_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], None, public_channel["channel_id"], -1)

# invalid parameter string input message for function message_share_v1
def test_message_share_invalid_message_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], 123456789, public_channel["channel_id"], -1)

# invalid parameter input message exceed 1000 characters for function message_share_v1
def test_message_share_exceed_length_limit_message():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "a"*1001, public_channel["channel_id"], -1)

# invalid parameter None input channel_id for function message_share_v1
def test_message_share_none_channel_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", None, -1)

# invalid parameter string input channel_id for function message_share_v1
def test_message_share_invalid_channel_id_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", "invalie_channel_id", -1)

# input of none existing channel_id for function message_share_v1
def test_message_share_channel_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", 123456789, -1)

# invalid parameter None input dm_id for function message_share_v1
def test_message_share_none_dm_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", -1, None)

# invalid parameter string input dm_id for function message_share_v1
def test_message_share_invalid_dm_type():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", -1, "invalid_dm_id")

# input of none existing dm_id for function message_share_v1
def test_message_share_dm_id_not_exist():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", -1, 123456789)

# input of non-channel_member trying to share og_message from channel for function message_share_v1
def test_message_share_non_channel_member():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(AccessError):
        message_share_v1(user_two["token"], message_one["message_id"], "message", public_channel["channel_id"], -1)

# input of non-dm_member tring to share og_message from dm for function message_share_v1
def test_message_share_non_dm_member():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    user_three = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    with pytest.raises(AccessError):
        message_share_v1(user_three["token"], dm_message_one["message_id"], "message", -1, dm_one["dm_id"])

# input of invalid channel_id and dm_id for function message_share_v1
def test_message_share_invalid_channel_id_and_dm_id():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    with pytest.raises(InputError):
        message_share_v1(user_one["token"], message_one["message_id"], "message", -1, -1)

### ----output checking---- ###
# output testing, sharing message to a channel for function message_share_v1
def test_message_share_channel_message_output():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    public_channel = channels_create_v2(user_one['token'], "public_channel", True)
    message_one = send_group_message(user_one["token"], public_channel["channel_id"], "first message", "channel")
    assert message_share_v1(user_one["token"], message_one["message_id"], "share message", public_channel["channel_id"], -1) == {'shared_message_id': 1}

# output testing, sharing message to a dm for function message_share_v1
def test_message_share_dm_message_output():
    clear_v1()
    user_one = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    user_two = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm_one = dm_create_v1(user_one["token"], [user_two["auth_user_id"]])
    dm_message_one = send_group_message(user_one["token"], dm_one["dm_id"], "first message", "dm")
    assert message_share_v1(user_one["token"], dm_message_one["message_id"], "share message", -1, dm_one["dm_id"]) == {'shared_message_id': 1}
