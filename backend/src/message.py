'''
implement message_edit_v2, message_remove_v1, message_share_v1, message_pinning
'''
from src.common import send_message
from src.error import AccessError, InputError
from src.helper_func import check_valid_token, check_valid_user_id, check_valid_channel_id, check_valid_channel_member, check_valid_channel_owner, check_valid_message_id, check_valid_message_sender, check_valid_dm_id, check_valid_dm_member, check_valid_dm_owner, extract_u_id, create_notification, extract_message_group_id, check_valid_group_id, extract_current_time, check_user_in_group, load_database, save_to_database
from src.timer_class import TimerAndResult

def message_edit_v2(token, message_id, message):
    '''
    Given a message, update its text with new text. If the new message is an empty 
    string, the message is deleted.

    Arguments:
        token(str) - token of user
        message_id(int) - id for message
        message(str) - message

    Exceptions:
        InputError  - Length of message is over 1000 characters
                    - message_id refers to a deleted message
        AccessError - Message with message_id was sent by the authorised user making this request
                    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        return {}
    '''
    data = load_database()
    messages = data["messages"]

    auth_user_id = extract_u_id(token)
    if message_id == None:
        raise InputError(description = "Input for message_id cannot be 'None'")
    if message == None:
        raise InputError(description = "Input for message cannot be 'None'")
    if isinstance(message_id, int) is False:
        raise InputError(description = "Invalid data type: message_id")
    if isinstance(message, str) is False:
        raise InputError(description = "Invalid data type: message")
    if not check_valid_message_id(message_id):
        raise InputError(description = f"Message with id {message_id} does not exist")
    # message <= 1000 characters
    if len(message) > 1000:
        raise InputError(description = "Message cannot exceed 1000 characters")
    for m in messages:
        if m["message_id"] == message_id:
            channel_id = m["channel_id"]
            dm_id = m["dm_id"]
    if not check_valid_message_sender(auth_user_id, message_id):
        raise AccessError(description = f"User {auth_user_id} is not an owner of this channel, does not have permission to edit this message")
    if channel_id != -1 and not check_valid_channel_owner(auth_user_id, channel_id):
        raise AccessError(description = f"User {auth_user_id} is not an owner of this channel")
    if dm_id != -1 and not check_valid_dm_owner(auth_user_id, dm_id):
        raise AccessError(description = f"User {auth_user_id} is not an owner of this dm, does not have permission to edit message")

    # should works for both channel & dm
    if message != '':
        for m in messages:
            if m["message_id"] == message_id:
                m["message"] = message
    else:
        # if the new message is an empty string, the message is deleted
        for i in range(len(messages)):
            if messages[i]["message_id"] == message_id:
                messages.pop(i)

    # Save changes to data.json file
    save_to_database(data)

    if channel_id != -1:
        create_notification(-1, auth_user_id, channel_id, message_id, "channel", -1)
    else:
        create_notification(-1, auth_user_id, dm_id, message_id, "dm", -1)

    return {}

def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        token(str) - token of user
        message_id(int) - id for message

    Exceptions:
        InputError  - Message (based on ID) no longer exists
        AccessError - Message with message_id was sent by the authorised user making this request
                    - The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**

    Return Value:
        return {}
    '''
    data = load_database()
    messages = data["messages"]

    auth_user_id = extract_u_id(token)

    if message_id == None:
        raise InputError(description = "Input for message_id cannot be 'None'")
    if isinstance(message_id, int) is False:
        raise InputError(description = "invalid data type: message_id")
    if not check_valid_user_id(auth_user_id):
        raise AccessError(description = f"User with id {auth_user_id} is not a registered user")
    if not check_valid_message_id(message_id):
        raise InputError(description = f"Message with id {message_id} does not exist")
    if not check_valid_message_sender(auth_user_id, message_id):
        raise AccessError(description = f"User {auth_user_id} does not have permission to delete this message")
    for m in messages:
        if m["message_id"] == message_id:
            channel_id = m["channel_id"]
            dm_id = m["dm_id"]
    if channel_id != -1 and not check_valid_channel_owner(auth_user_id, channel_id):
        raise AccessError(description = f"User {auth_user_id} is not an owner of the channel, does not have permission to delete message")
    if dm_id != -1 and not check_valid_dm_owner(auth_user_id, dm_id):
        raise AccessError(description = f"User {auth_user_id} is not an owner of this dm, does not have permission to delete message")

    # should works for both channel & dm
    for i in range(len(messages)):
        if messages[i]["message_id"] == message_id:
            messages.pop(i)

    # Save changes to data.json file
    save_to_database(data)

    if channel_id != -1:
        create_notification(-1, auth_user_id, channel_id, message_id, "channel", -1)
    else:
        create_notification(-1, auth_user_id, dm_id, message_id, "dm", -1)

    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Given a message_id for a message, this message is shared.

    Arguments:
        token(str) - token of user
        og_message_id(int) - id for original message
        message(str) - message
        channel_id(int) - id for channel, -1 if message not shared to channel
        dm_id(int) - id for dm, -1 if message not shared to dm

    Exceptions:
        AccessError - the authorised user has not joined the channel or DM they are trying to share the message to
    
    Return Value:
        return { shared_message_id }
    '''
    data = load_database()
    messages = data["messages"]

    auth_user_id = extract_u_id(token)

    if og_message_id == None:
        raise InputError(description = "Input for og_message_id cannot be 'None'")
    if message == None:
        raise InputError(description = "Input for message cannot be 'None'")
    if channel_id == None:
        raise InputError(description = "Input for channel_id cannot be 'None'")
    if dm_id == None:
        raise InputError(description = "Input for dm_id cannot be 'None'")
    if isinstance(og_message_id, int) is False:
        raise InputError(description = "invalid data type: og_message_id")
    if isinstance(message, str) is False:
        raise InputError(description = "invalid data type: message")
    if isinstance(channel_id, int) is False:
        raise InputError(description = "invalid data type: channel_id")
    if isinstance(dm_id, int) is False:
        raise InputError(description = "invalid data type: dm_id")
    if not check_valid_message_id(og_message_id):
        raise InputError(description = f"Og_message with id {og_message_id} does not exist")
    if not check_valid_user_id(auth_user_id):
        raise AccessError(description = f"User with id {auth_user_id} is not a registered user")
    if channel_id == -1 and dm_id == -1:
        raise InputError(description = "both channel and dm does not exist")
    if channel_id != -1 and not check_valid_channel_id(channel_id):
        raise InputError(description = f"Channel with id {channel_id} does not exist")
    if channel_id != -1 and not check_valid_channel_member(auth_user_id, channel_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this channel")
    if dm_id != -1 and not check_valid_dm_id(dm_id):
        raise InputError(description = f"Dm with is {dm_id} does not exist")
    if dm_id != -1 and not check_valid_dm_member(auth_user_id, dm_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this dm")
    for m in messages:
        if m["message_id"] == og_message_id:
            og_message = m
            if m["channel_id"] != channel_id:
                raise InputError(description = f"Message not found in channel with id {channel_id}")
            if m["dm_id"] != dm_id:
                raise InputError(description = f"Message not found in dm with id {dm_id}")
    # message <= 1000 characters
    if len(message) > 1000:
        raise InputError(description = "Message cannot exceed 1000 characters")

    timestamp = extract_current_time()

    shared_message = og_message["message"] + " shared_message: " + message

    # get message_id
    message_id = 0
    for m in data["messages"]:
        if m["message_id"] == message_id:
            message_id += 1

    new_message = {
        'message_id' : message_id,
        'u_id': auth_user_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'message': shared_message,
        'time_created': timestamp,
        'reacts': [],
        'is_pinned': False,
    }

    messages.append(new_message)

    # Save changes to data.json file
    save_to_database(data)

    if channel_id != -1:
        create_notification(-1, auth_user_id, channel_id, message_id, "channel", -1)
    else:
        create_notification(-1, auth_user_id, dm_id, message_id, "dm", -1)

    return {'shared_message_id': message_id,}

def message_react_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message

    Arguments:
        token(str) - token of user
        message_id(int) - id for message
        react_id(int) - id for react, only id 1 exists

    Exceptions:
        InputError  - message_id is not a valid message within a channel or DM that the authorised user has joined
                    - react_id is not a valid React ID. The only valid react ID the frontend has is 1
                    - Message with ID message_id already contains an active React with ID react_id from the authorised user
        AccessError - The authorised user is not a member of the channel or DM that the message is within

    Return Value:
        return {}
    '''
    data = load_database()
    messages = data["messages"]

    auth_user_id = extract_u_id(token)
    if message_id == None:
        raise InputError(description = "Input for message_id cannot be 'None'")
    if react_id != 1:
        raise InputError(description = "Invalid input for react_id")
    if isinstance(message_id, int) is False:
        raise InputError(description = "Invalid data type: message_id")
    if not check_valid_message_id(message_id):
        raise InputError(description = f"Message with id {message_id} does not exist")
    for m in messages:
        if m["message_id"] == message_id:
            channel_id = m["channel_id"]
            dm_id = m["dm_id"]
            reacts = m["reacts"]
    if channel_id != -1 and not check_valid_channel_member(auth_user_id, channel_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this channel, cannot react to message")
    if dm_id != -1 and not check_valid_dm_member(auth_user_id, dm_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this dm, cannot react to message")
    for react in reacts:
        if react['react_id'] == react_id and auth_user_id in react['u_ids']:
            raise InputError(description = f"User {auth_user_id} has already reacted to this message")
    status = False
    for m in messages:
        if m["message_id"] == message_id:
            sender_id = m["u_id"]
            for react in m["reacts"]:
            # if react_id in [react["react_id"] for react in m["reacts"]]:
                if react["react_id"] == react_id:
                    react["u_ids"].append(auth_user_id)
                    react["is_this_user_reacted"] = True
                    status = True
            if status == False:
                new_react = {
                    "react_id": react_id,
                    "u_ids": [auth_user_id],
                    "is_this_user_reacted": True,
                }
                m["reacts"].append(new_react)


    # Save changes to data.json file
    save_to_database(data)

    if channel_id != -1:
        create_notification(-1, sender_id, channel_id, message_id, "channel", react_id)
    else:
        create_notification(-1, sender_id, dm_id, message_id, "dm", react_id)

    return {}

def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message

    Arguments:
        token(str) - token of user
        message_id(int) - id for message
        react_id(int) - id for react, only id 1 exists

    Exceptions:
        InputError  - message_id is not a valid message within a channel or DM that the authorised user has joined
                    - react_id is not a valid React ID
                    - Message with ID message_id does not contain an active React with ID react_id from the authorised user
        AccessError - The authorised user is not a member of the channel or DM that the message is within
        
    Return Value:
        return {}
    '''
    data = load_database()
    messages = data["messages"]

    auth_user_id = extract_u_id(token)
    if message_id == None:
        raise InputError(description = "Input for message_id cannot be 'None'")
    if react_id != 1:
        raise InputError(description = "Invalid input for react_id")
    if isinstance(message_id, int) is False:
        raise InputError(description = "Invalid data type: message_id")
    if not check_valid_message_id(message_id):
        raise InputError(description = f"Message with id {message_id} does not exist")
    for m in messages:
        if m["message_id"] == message_id:
            channel_id = m["channel_id"]
            dm_id = m["dm_id"]
            reacts = m["reacts"]
    if channel_id != -1 and not check_valid_channel_member(auth_user_id, channel_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this channel, cannot react to message")
    if dm_id != -1 and not check_valid_dm_member(auth_user_id, dm_id):
        raise AccessError(description = f"User {auth_user_id} is not a member of this dm, cannot react to message")
    if react_id not in [react['react_id'] for react in reacts]:
        raise InputError(description = f"react_id {react_id} does not exist in message")
    for react in reacts:
        if react['react_id'] == react_id and auth_user_id not in react['u_ids']:
            raise InputError(description = f"User {auth_user_id} has not reacted to this message yet")

    for m in messages:
        if m["message_id"] == message_id:
            for react in m["reacts"]:
                if react["react_id"] == react_id:
                    react["u_ids"].remove(auth_user_id)
                    react["is_this_user_reacted"] = False

    # Save changes to data.json file
    save_to_database(data)

    return{}
    
    
def message_pinning(token, message_id, pin_action):
    '''
    Given a message_id for a message, this message this message is pinned if pin_action
    is True and unpinned if pin_action is False.

    Arguments:
        token(str)          - token of user
        message_id(int)     - ID for the message to be pinned/unpinned
        pin_action(bool)    - True if pinning, False if unpinning.

    Exceptions:
        AccessError     - When the authorised user is not an owner member of the 
                            channel/dm where the message was sent
                        - The token given is invalid.
        InputError  
                        - Message ID is not a valid message
                        - Message is already pinned/unpinned
    
    Return Value:
        return {}
    '''
    data = load_database()
    messages = data['messages']
    
    user_id = extract_u_id(token)
    
    message_group_ids = extract_message_group_id(message_id)
    
    if not (check_valid_channel_owner(user_id, message_group_ids['channel_id']) or
    check_valid_dm_owner(user_id, message_group_ids['dm_id'])):
        raise AccessError(description = 'do not have permission to pin this message, only group owners may pin messages')
    
    for message in messages:
        if message['message_id'] == message_id:
            if message['is_pinned'] == pin_action:
                raise InputError(description = 'the message is already pinned or unpinned')
            else:
                message['is_pinned'] = pin_action
                
    # Save changes to data.json file
    save_to_database(data)
    return {}


def message_sendlater(token, group_id, message, time_sent, group_type):
    '''
    This function sends a message to a channel or dm with group_id at some point
    in the future specified by the input time_sent. 

    Arguments:
        token(str)          - token of user
        group_id(int)       - ID of the group the message will be sent in.
        message(str)        - Contents of the message to be sent
        time_sent(int)      - Timestamp of the time the message should be sent.
        group_type(str)     - Either the string "dm" if message is to be sent to
                                a dm or "channel" if the message is being sent
                                to a channel
        
    Exceptions:
        AccessError     - When the authorised user is not a member of the 
                            channel/dm where the message is being sent
                        - The token given is invalid.
        InputError  
                        - Channel or DM IDs are not valid group IDs
                        - Message is more than 1000 characters
                        - Time sent is a time in the past.
    
    Return Value:
        return {"message_id": (int)}
        
        Returns the message_id of the message after it has been sent.
    '''
    MAX_MESSAGE_LEN = 1000
    check_valid_token(token)
    check_valid_group_id(group_id, group_type)
    if not check_user_in_group(token, 'token', group_id, group_type):
        raise AccessError(description = 'user must be in group to send a message')
    
    curr_time = extract_current_time()
    
    if time_sent < curr_time:
        raise InputError(description = 'message cannot be sent in the past')
    if len(message) > MAX_MESSAGE_LEN:
        raise InputError(description = 'message cannot be over 1000 characters')
    
    data = load_database()
    auth_user_id = extract_u_id(token)

    timer = TimerAndResult(time_sent - curr_time, send_message, (group_id, message, group_type, data, auth_user_id))
    timer.start()
    
    timer.join()

    return timer.output()

