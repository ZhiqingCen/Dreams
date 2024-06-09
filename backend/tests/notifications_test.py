'''
test file for src/notifications.py
'''
import pytest
from src.helper_func import load_database
from src.notifications import notifications_get_v1
from src.auth import auth_register_v2
from src.channel import channel_join_v2
from src.channels import channels_create_v2
from src.common import invite_to_group, send_group_message, leave_group
from src.message import message_edit_v2, message_share_v1, message_react_v1, message_unreact_v1
from src.dm import dm_create_v1
from src.other import clear_v1
from src.error import AccessError

###------------------------------------------------------###
### notifications_get_v1(token) return { notifications } ###
###------------------------------------------------------###
### ----input checking---- ###
# invalid parameter empty string input token for function notifications_get_v1
def test_notifications_get_empty_token():
    with pytest.raises(AccessError):
        notifications_get_v1("")

# invalid parameter None input token for function notifications_get_v1
def test_notifications_get_none_token():
    with pytest.raises(AccessError):
        notifications_get_v1(None)

# invalid parameter string input token for function notifications_get_v1
def test_notifications_get_invalid_token_type():
    with pytest.raises(AccessError):
        notifications_get_v1(123456789)

# input of none existing token for function notifications_get_v1
def test_notifications_get_token_not_exist():
    with pytest.raises(AccessError):
        notifications_get_v1("invalid_token")

### ----output checking---- ###
# ------- tag ------- #
# channel send_group_message without tag
def test_notifications_get_send_group_message_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# channel send_group_message tag member
def test_notifications_get_send_group_message_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    channel_member_handle = next(user["handle_str"] for user in users if user["u_id"] == channel_member["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    send_group_message(owner["token"], channel["channel_id"], f"@{channel_member_handle} message", "channel")

    m = f"@{channel_member_handle} message"

    message = f"{owner_handle} tagged you in channel_one: {m[0:20]}"
    assert notifications_get_v1(channel_member["token"]) == {'notifications': [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]}

# channel edit_message without tag
def test_notifications_get_edit_message_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    sent_m = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_edit_v2(owner["token"], sent_m["message_id"], "editted message")

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# channel edit_message tag member
def test_notifications_get_edit_message_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    channel_member_handle = next(user["handle_str"] for user in users if user["u_id"] == channel_member["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    sent_m = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_edit_v2(owner["token"], sent_m["message_id"], f"@{channel_member_handle} editted message")

    m = f"@{channel_member_handle} editted message"

    message = f"{owner_handle} tagged you in channel_one: {m[0:20]}"
    assert notifications_get_v1(channel_member["token"]) == {'notifications': [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]}

# channel share_message without tag
def test_notifications_get_share_message_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    sent_m = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_share_v1(owner["token"], sent_m["message_id"], "shared message", channel["channel_id"], -1)

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# channel share_message tag member
def test_notifications_get_share_message_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    channel_member_handle = next(user["handle_str"] for user in users if user["u_id"] == channel_member["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    sent_m = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_share_v1(owner["token"], sent_m["message_id"], f"@{channel_member_handle} shared message", channel["channel_id"], -1)

    m = f"message shared_message: shared message"

    message = f"{owner_handle} tagged you in channel_one: {m[0:20]}"
    assert notifications_get_v1(channel_member["token"]) == {'notifications': [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]}

# dm send_group_message without tag
def test_notifications_get_send_dm_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    send_group_message(owner["token"], dm["dm_id"], "message", "dm")

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# dm send_group_message tag member
def test_notifications_get_send_dm_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    dm_member_handle = next(user["handle_str"] for user in users if user["u_id"] == dm_member["auth_user_id"])
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    send_group_message(owner["token"], dm["dm_id"], f"@{dm_member_handle} message", "dm")

    m = f"@{dm_member_handle} message"

    message = f"{owner_handle} tagged you in oneone, twotwo: {m[0:20]}"
    assert notifications_get_v1(dm_member["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]}

# dm edit_message without tag
def test_notifications_get_edit_dm_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    sent_dm = send_group_message(owner["token"], dm["dm_id"], "message", "dm")
    message_edit_v2(owner["token"], sent_dm["message_id"], "editted message")

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# dm edit_message tag member
def test_notifications_get_edit_dm_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    dm_member_handle = next(user["handle_str"] for user in users if user["u_id"] == dm_member["auth_user_id"])
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    sent_dm = send_group_message(owner["token"], dm["dm_id"], "message", "dm")
    message_edit_v2(owner["token"], sent_dm["message_id"], f"@{dm_member_handle} editted message")

    m = f"@{dm_member_handle} editted message"
    message = f"{owner_handle} tagged you in oneone, twotwo: {m[0:20]}"
    # message = f"{owner_handle} tagged you in {dm["dm_name"]}: {m[0:20]}"
    assert notifications_get_v1(dm_member["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]}

# dm share_message without tag
def test_notifications_get_share_dm_without_tag():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    sent_dm = send_group_message(owner["token"], dm["dm_id"], "message", "dm")
    message_share_v1(owner["token"], sent_dm["message_id"], "shared message", -1, dm["dm_id"])

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# dm share_message tag member
def test_notifications_get_share_dm_tag_member():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    dm_member_handle = next(user["handle_str"] for user in users if user["u_id"] == dm_member["auth_user_id"])
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    sent_dm = send_group_message(owner["token"], dm["dm_id"], "message", "dm")
    message_share_v1(owner["token"], sent_dm["message_id"], f"@{dm_member_handle} shared message", -1, dm["dm_id"])

    m = f"message shared_message: shared message"
    message = f"{owner_handle} tagged you in oneone, twotwo: {m[0:20]}"

    assert notifications_get_v1(dm_member["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]}

# ------- invite ------- #
# channel_invite
def test_notifications_get_channel_invite():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    invite_to_group(owner['token'], channel['channel_id'], channel_member['auth_user_id'], "channel")

    message = f"{owner_handle} added you to channel_one"

    assert notifications_get_v1(channel_member["token"]) == {'notifications': [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]}

# dm_invite
def test_notifications_get_dm_invite():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    owner_handle = next(user["handle_str"] for user in users if user["u_id"] == owner["auth_user_id"])
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    invite_to_group(owner["token"], dm["dm_id"], channel_member["auth_user_id"], "dm")

    message = f"{owner_handle} added you to oneone, twotwo"

    assert notifications_get_v1(channel_member["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]}

# ------- react ------- #
# react to channel message
def test_notifications_get_react_channel_message():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    member_handle = next(user["handle_str"] for user in users if user["u_id"] == channel_member["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    channel_join_v2(channel_member['token'], channel['channel_id'])
    channel_message = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_react_v1(channel_member['token'], channel_message['message_id'], 1)

    message = f"{member_handle} reacted to your message in channel_one"
    assert notifications_get_v1(owner["token"]) == {'notifications': [{'channel_id': 0, 'dm_id': -1, 'notification_message': message}]}

# react to dm message
def test_notifications_get_react_dm_message():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    dm_member = auth_register_v2("address@email2.com", "onetwothree", "two", "Two")
    data = load_database()
    users = data["users"]
    member_handle = next(user["handle_str"] for user in users if user["u_id"] == dm_member["auth_user_id"])
    dm = dm_create_v1(owner["token"], [dm_member["auth_user_id"]])
    dm_message = send_group_message(owner["token"], dm["dm_id"], "first message", "dm")
    message_react_v1(dm_member['token'], dm_message['message_id'], 1)

    message = f"{member_handle} reacted to your message in oneone, twotwo"
    assert notifications_get_v1(owner["token"]) == {'notifications': [{'channel_id': -1, 'dm_id': 0, 'notification_message': message}]}

# ------- other output ------- #
# no notification for channel message
def test_notifications_no_notification_output():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    channel_join_v2(channel_member['token'], channel['channel_id'])
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

def test_notifications_message_not_react_output():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    channel_join_v2(channel_member['token'], channel['channel_id'])
    channel_message1 = send_group_message(channel_member["token"], channel["channel_id"], "message", "channel")
    send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    message_react_v1(owner['token'], channel_message1['message_id'], 1)

    assert notifications_get_v1(owner["token"]) == {'notifications': []}

# only output 20 most recent notifications
def test_notifications_react_more_than_twenty():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    channel = channels_create_v2(owner['token'], "channel_one", True)
    channel_join_v2(channel_member['token'], channel['channel_id'])
    channel_message = send_group_message(owner["token"], channel["channel_id"], "message", "channel")
    for _ in range(21):
        message_react_v1(channel_member['token'], channel_message['message_id'], 1)
        message_unreact_v1(channel_member['token'], channel_message['message_id'], 1)

    data = notifications_get_v1(owner["token"])
    assert len(data["notifications"]) == 20

# only output 20 most recent tag notifications
def test_notifications_tag_more_than_twenty():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    data = load_database()
    users = data["users"]
    channel_member_handle = next(user["handle_str"] for user in users if user["u_id"] == channel_member["auth_user_id"])
    channel = channels_create_v2(owner['token'], "channel_one", True)
    channel_join_v2(channel_member['token'], channel['channel_id'])

    for _ in range(21):
        send_group_message(owner["token"], channel["channel_id"], f"@{channel_member_handle} message", "channel")
    
    data = notifications_get_v1(channel_member["token"])
    assert len(data["notifications"]) == 20

# only output 20 most recent invite notifications
def test_notifications_invite_more_than_twenty():
    clear_v1()
    owner = auth_register_v2("address@email1.com", "onetwothree", "one", "One")
    channel_member = auth_register_v2("address@email3.com", "onetwothree", "three", "Three")
    channel = channels_create_v2(owner['token'], "channel_one", True)

    for _ in range(21):
        invite_to_group(owner['token'], channel['channel_id'], channel_member['auth_user_id'], "channel")
        leave_group(channel_member['token'], channel['channel_id'], "channel")

    data = notifications_get_v1(channel_member["token"])
    assert len(data["notifications"]) == 20