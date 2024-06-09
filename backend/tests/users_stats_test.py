'''
test file for src/users_stats_v1
'''
from src.helper_func import extract_current_time
import pytest

from src.user import users_stats_v1
from src.common import send_group_message, extract_messages_from_group
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError

###-----------------------------------------------------------###
### users_stats_v1(token) return {'dreams_stats': user_stats} ###
###-----------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function users_stats_v1
def test_users_stats_empty_token():
    clear_v1()
    with pytest.raises(AccessError):
        users_stats_v1("",)

# invalid parameter None input token for function users_stats_v1
def test_users_stats_none_token():
    clear_v1()
    with pytest.raises(AccessError):
        users_stats_v1(None)

# invalid parameter string input token for function users_stats_v1
def test_users_stats_invalid_token_type():
    clear_v1()
    with pytest.raises(AccessError):
        users_stats_v1(123456789)

# input of none existing token for function users_stats_v1
def test_users_stats_token_not_exist():
    clear_v1()
    with pytest.raises(AccessError):
        users_stats_v1("invalid_token")

### ----output checking---- ###
# user not in any channels, dms for function users_stats_v1
def test_users_stats_user_not_in_channels_dms():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    data = users_stats_v1(owner["token"])
    assert data["dreams_stats"]["utilization_rate"] == 0

# all users joined channels/dms for function users_stats_v1
def test_users_stats_all_users_joined_channels_dms():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")

    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    send_group_message(owner["token"], dm["dm_id"], "message", "dm")

    timestamp = extract_current_time()

    data = users_stats_v1(owner["token"])
    assert data["dreams_stats"] == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': timestamp,}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': timestamp,}],
        'messages_exist': [{'num_messages_exist': 2, 'time_stamp': timestamp,}],
        'utilization_rate': 1.0,
    }

# half users joined channels/dms for function users_stats_v1
def test_users_stats_half_users_joined_channels_dms():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    auth_register_v2("address@email2.com", "onetwothree", "two", "Two")

    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    timestamp = extract_current_time()

    data = users_stats_v1(owner["token"])
    assert data["dreams_stats"] == {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': timestamp,}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': timestamp,}],
        'messages_exist': [{'num_messages_exist': 1, 'time_stamp': timestamp,}],
        'utilization_rate': 0.5,
    }
