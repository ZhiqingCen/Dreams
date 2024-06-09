'''
test file for src/user_stats_v1
'''
from src.helper_func import extract_current_time
import pytest

from src.user import user_stats_v1
from src.common import send_group_message, extract_messages_from_group
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError

###--------------------------------------------------------###
### user_stats_v1(token) return {'user_stats': user_stats} ###
###--------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function user_stats_v1
def test_user_stats_empty_token():
    clear_v1()
    with pytest.raises(AccessError):
        user_stats_v1("",)

# invalid parameter None input token for function user_stats_v1
def test_user_stats_none_token():
    clear_v1()
    with pytest.raises(AccessError):
        user_stats_v1(None)

# invalid parameter string input token for function user_stats_v1
def test_user_stats_invalid_token_type():
    clear_v1()
    with pytest.raises(AccessError):
        user_stats_v1(123456789)

# input of none existing token for function user_stats_v1
def test_user_stats_token_not_exist():
    clear_v1()
    with pytest.raises(AccessError):
        user_stats_v1("invalid_token")

### ----output checking---- ###
# no channels, dms, messages in database for function user_stats_v1
def test_user_stats_no_channels_dms_messages():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    data = user_stats_v1(owner["token"])
    assert data["user_stats"]["involvement_rate"] == 0

# test output, 100% involvement_rate for function user_stats_v1
def test_user_stats_fully_involved():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")

    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    send_group_message(owner["token"], dm["dm_id"], "message", "dm")

    timestamp = extract_current_time()

    data = user_stats_v1(owner["token"])
    assert data["user_stats"] == {
        'channels_joined': [{'num_channels_joined': 1, 'time_stamp': timestamp}],
        'dms_joined': [{'num_dms_joined': 1, 'time_stamp': timestamp}],
        'messages_sent': [{'num_messages_sent': 2, 'time_stamp': timestamp}],
        'involvement_rate': 1.0
    }

# test output, 50% involvement_rate for function user_stats_v1
def test_user_stats_halfly_involved():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")

    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    send_group_message(dm_member["token"], dm["dm_id"], "message", "dm")

    timestamp = extract_current_time()

    data = user_stats_v1(dm_member["token"])
    assert data["user_stats"] == {
        'channels_joined': [{'num_channels_joined': 0, 'time_stamp': timestamp}],
        'dms_joined': [{'num_dms_joined': 1, 'time_stamp': timestamp}],
        'messages_sent': [{'num_messages_sent': 1, 'time_stamp': timestamp}],
        'involvement_rate': 0.5
    }

