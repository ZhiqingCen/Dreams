'''
implement notifications_v1
'''
from src.error import AccessError, InputError
from json import loads
from src.helper_func import check_valid_token, check_valid_user_id, extract_u_id, check_valid_channel_id, check_valid_dm_id, load_database
'''
-   channel_id is the id of the channel that the event happened in,
    and is -1 if it is being sent to a DM.
-   dm_id is the DM that the event happened in,
    and is -1 if it is being sent to a channel.
-   Notification_message is a string of the following format for each trigger action:
    * tagged: "{User’s handle} tagged you in {channel name}: {first 20 characters of the message}"
    * reacted message: "{User’s handle} reacted to your message in {channel name}"
    * added to a channel: "{User’s handle} added you to {channel name}"
'''
def notifications_get_v1(token):
    '''
    Description: 
        Return the user's most recent 20 notifications

    Arguments:
        token<int>   - the token of the authorised user (who is part of the group) that is inviting the user with u_id

    Exceptions:

    Return Value:
        Returns { notifications }

    '''
    data = load_database()

    notifications = data["notifications"]

    check_valid_token(token)
    auth_user_id = extract_u_id(token)

    user_handle = get_user_handle(auth_user_id)
    tag_handle = f"@{user_handle} "

    user_notifications = []
    sorted(notifications, key=lambda i: i['time_create'], reverse=True)

    for notification in notifications:
        # invited to channel/dm
        if notification["u_id"] == auth_user_id and notification["inviter_u_id"] != -1:
            # if notification["inviter_u_id"] != -1:
            inviter_handle = get_user_handle(notification["inviter_u_id"])
            if check_valid_user_id(notification["inviter_u_id"]):
                notification_message = ""
                if notification["channel_id"] != -1 and check_valid_channel_id(notification["channel_id"]):
                    channel_name = get_channel_name(notification["channel_id"])
                    notification_message = f"{inviter_handle} added you to {channel_name}"
                elif notification["dm_id"] != -1 and check_valid_dm_id(notification["dm_id"]):
                    dm_name = get_dm_name(notification["dm_id"])
                    notification_message = f"{inviter_handle} added you to {dm_name}"
                
                if notification_message != "":
                    new_notification = {
                        'channel_id': notification["channel_id"],
                        'dm_id': notification["dm_id"],
                        'notification_message': notification_message,
                    }
                    user_notifications.append(new_notification)
                    # get most reacent 20 notificaitons
                    if len(user_notifications) == 20:
                        break

        # tagged by member from channel/dm
        elif notification["message"] != "" and tag_handle in notification["message"]:
            sender_handle = get_user_handle(notification["u_id"])
            if sender_handle != None:
                # first 20 characters
                message_head = notification["message"][0:20]
                notification_message = ""
                if notification["channel_id"] != -1 and check_valid_channel_id(notification["channel_id"]):
                    channel_name = get_channel_name(notification["channel_id"])
                    notification_message = f"{sender_handle} tagged you in {channel_name}: {message_head}"
                elif notification["dm_id"] != -1 and check_valid_dm_id(notification["dm_id"]):
                    dm_name = get_dm_name(notification["dm_id"])
                    notification_message = f"{sender_handle} tagged you in {dm_name}: {message_head}"
                
                if notification_message != "":
                    new_notification = {
                        'channel_id': notification["channel_id"],
                        'dm_id': notification["dm_id"],
                        'notification_message': notification_message,
                    }
                    user_notifications.append(new_notification)
                    # get most reacent 20 notificaitons
                    if len(user_notifications) == 20:
                        break

        
        # message reacted by channel/dm member
        # elif notification["u_id"] == auth_user_id and notification["message"] != "" and notification["react_id"] == 1:
        elif notification["u_id"] == auth_user_id and notification["message"] != "" and notification["react_id"] == 1:
            reacter_handle = get_user_handle(notification["reactors"][-1])
            if reacter_handle != None:
                notification_message = ""
                if notification["channel_id"] != -1 and check_valid_channel_id(notification["channel_id"]):
                    channel_name = get_channel_name(notification["channel_id"])
                    notification_message = f"{reacter_handle} reacted to your message in {channel_name}"
                elif notification["dm_id"] != -1 and check_valid_dm_id(notification["dm_id"]):
                    dm_name = get_dm_name(notification["dm_id"])
                    notification_message = f"{reacter_handle} reacted to your message in {dm_name}"
                
                if notification_message != "":
                    new_notification = {
                        'channel_id': notification["channel_id"],
                        'dm_id': notification["dm_id"],
                        'notification_message': notification_message,
                    }
                    user_notifications.append(new_notification)
                    # get most reacent 20 notificaitons
                    if len(user_notifications) == 20:
                        break
    
    return { 'notifications' : user_notifications, }

# function to get a channel's name
def get_channel_name(channel_id):
    data = load_database()
    channels = data["channels"]

    channel_name = None
    for channel in channels:
        if channel_id == channel["channel_id"]:
            channel_name = channel["name"]

    return channel_name

# function to get a dm's name
def get_dm_name(dm_id):
    data = load_database()
    dms = data["dms"]

    dm_name = None
    for dm in dms:
        if dm_id == dm["dm_id"]:
            dm_name = dm["name"]

    return dm_name

# function to get a user's handle
def get_user_handle(auth_user_id):
    data = load_database()
    users = data["users"]

    for user in users:
        if user["u_id"] == auth_user_id:
            return user["handle_str"]
    return None

# function to check if user handle is valid
def check_valid_handle(handle):
    data = load_database()
    users = data["users"]

    for user in users:
        if user["handle_str"] == handle and check_valid_user_id(user["u_id"]):
            return True
    return False

