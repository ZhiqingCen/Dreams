from src.error import AccessError, InputError
from src.helper_func import check_user_in_group, check_valid_token, check_valid_user_id, check_valid_group_id, create_id, extract_u_id, create_notification, extract_current_time, load_database, save_to_database

# ---------------------------- #
# channel_invite and dm_invite #
# ---------------------------- #
def invite_to_group(token, group_id, u_id, group_type):
    '''
    Description: 
        Invites a user with u_id to join a group with group_id of type group_type. 
        Once invited, the user is added to the group immediately.

    Arguments:
        token           <int>   - the token of the authorised user (who is part of the group) that is inviting the user with u_id
        group_id        <int>   - the id of the group the user with u_id is being invited to
        u_id            <int>   - the id of the user being invited to the group
        group_type      <str>   - either 'channel' or 'dm', specifying the type of group to join

    Exceptions:
        AccessError -  Occurs when the authorised user is not already a member of the group or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the group_id does not refer to a valid group or
                              when the u_id does not refer to a valid user          or
                              when any of the inputs are 'None'                     or
                              when the user with u_id is already a member of the group

    Return Value:
        Returns {}

    '''
    
    check_valid_token(token)
    check_valid_group_id(group_id, group_type)
    check_valid_user_id(u_id)

    if not check_user_in_group(token, 'token', group_id, group_type):
        raise AccessError(description=f"Authorising user is not in the {group_type}")

    if check_user_in_group(u_id, 'u_id', group_id, group_type):
        raise InputError(description=f"User is already a member of this {group_type}")
    
    # Add the user to the group immediately

    data = load_database()
    
    users = data['users']

    groups = data[group_type + 's']
    group_id_str = group_type + '_id'
    group_member_ids = group_type + '_member_ids'
    group_owner_ids = group_type + '_owner_ids'

    # Find the group for the user to join
    group = [group for group in groups if group[group_id_str] == group_id][0]
    # Append the u_id to the list of members for the group
    group[group_member_ids].append(u_id)

    if True in [user['global_owner'] for user in users if user['u_id'] == u_id]:
        group[group_owner_ids].append(u_id)

    # Save changes to data.json file
    save_to_database(data)

    inviter_u_id = extract_u_id(token)

    if group_type == "channel":
        create_notification(inviter_u_id, u_id, group_id, -1, "channel", -1)
    else:
        create_notification(inviter_u_id, u_id, group_id, -1, "dm", -1)
    
    return {}

# ------------------------------ #
# channel_details and dm_details #
# ------------------------------ #
def group_details(token, group_id, group_type):
    '''
    Description: 
        Provides basic details about a group when given the id of the requesting user, the id of the group being requested
        and the type of group being requested. 

    Arguments:
        token           <int> - the token of the authorised user (who is part of the group) requesting the group details
        group_id        <int> - the id of the group whose details are being requested
        group_type      <str> - either 'channel' or 'dm', specifying what type of group group_id is

    Exceptions:
        AccessError -  Occurs when the authorised user is not already a member of the group or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the group_id does not refer to a valid group or
                              when any of the inputs are 'None'                     

    Return Value:
        For a channel:
            Returns {
                'name', 
                'owner_members': [{
                    'u_id'
                    'name_first'
                    'name_last'
                },], 
                'all_members': [{
                    'u_id'
                    'name_first'
                    'name_last'
                },],
            } 
        For a dm:
            Returns {
                'name', 
                'members': [{
                    'u_id'
                    'email'
                    'name_first'
                    'name_last'
                    'handle_str'
                },], 
            }

    '''
    check_valid_token(token)
    check_valid_group_id(group_id, group_type)

    if not check_user_in_group(token, 'token', group_id, group_type):
        raise AccessError(description=f"Authorised user is not in the {group_type}")

    data = load_database()
    
    users = data['users']

    groups = data[group_type + 's']
    group_id_str = group_type + '_id'
    group_member_ids = group_type + '_member_ids'

    #Fetch details
    details = {}

    # Get the group name
    group = [group for group in groups if group[group_id_str] == group_id][0]
    group_name = group['name']
    
    # Get the group members
    group_members = [user for user in users if user['u_id'] in group[group_member_ids]]

    #if the group type is dm, format members and name
    if group_type == 'dm':
        
        details['name'] = group_name

        details['members'] = []
        for member in group_members:
            # Create user dictionary to add to dm details
            member_data = {
                'u_id': member['u_id'], 
                'email': member['email'], 
                'name_first': member['name_first'], 
                'name_last': member['name_last'],
                'handle_str': member['handle_str'],
            }
            # Add user dictionary to details
            details['members'].append(member_data)

    if group_type == 'channel':
        
        details['name'] = group_name

        details['is_public'] = group['is_public']
        
        details['all_members'] = []
        for member in group_members:

            # Create user dictionary to add to channel details
            member_data = {
                'u_id': member['u_id'], 
                'name_first': member['name_first'], 
                'name_last': member['name_last'],
            }
            # Add user dictionary to details
            details['all_members'].append(member_data)

        group_owners = [user for user in users if user['u_id'] in group['channel_owner_ids']]
        
        details['owner_members'] = []
        for owner in group_owners:
            # Create user dictionary to add to channel details
            owner_data = {
                'u_id': owner['u_id'], 
                'name_first': owner['name_first'], 
                'name_last': owner['name_last']
            }
            # Add user dictionary to details
            details['owner_members'].append(owner_data)

    return details

# -------------------------- #
# channel_leave and dm_leave #
# -------------------------- #
def leave_group(token, group_id, group_type):
    '''
    Description: 
        Allows authorised user to leave a group with group_id of type group_type. 

    Arguments:
        token           <int>   - the token of the user (who is part of the group) that is leaving the group
        group_id        <int>   - the id of the group the user with u_id is leaving
        group_type      <str>   - either 'channel' or 'dm', specifying the type of group to leave

    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the group or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the group_id does not refer to a valid group                   

    Return Value:
        Returns {}

    '''
    check_valid_token(token)
    check_valid_group_id(group_id, group_type)

    if not check_user_in_group(token, 'token', group_id, group_type):
        raise AccessError(description=f"Authorising user is not in the {group_type}")
    
    data = load_database()
    
    users = data['users']

    groups = data[group_type + 's']
    group_id_str = group_type + '_id'
    group_member_ids = group_type + '_member_ids'
    group_owner_ids = group_type + '_owner_ids'

    # Find the group for the user to leave
    group = [group for group in groups if group[group_id_str] == group_id][0]
    
    #Find the user with token
    user = [user for user in users if token in user['token']][0]

    # Delete the u_id from the list of members for the group
    group[group_member_ids].remove(user['u_id'])

    # If owner, delete the u_id from the list of owners for the group
    if user['global_owner'] == True or user['u_id'] in group[group_owner_ids]:
        group[group_owner_ids].remove(user['u_id'])
    
    # Save changes to data.json file
    save_to_database(data)
    
    return {}

# ------------------------- #
# channels_list and dm_list #
# ------------------------- #
def list_groups(token, group_type):
    '''
    Provide a list of all channels or dms (and their associated details) that
    the authorised user is part of

    Arguments:
        token (str)         - unique token for user in active session
        message_type (str)  - either the string "dm" if the groups being listed 
                                are dms or "channel" if the groups being listed
                                are channels

    Exceptions:
        AccessError - Occurs when input token is invalid.

    Return Value:
        For a channel:
        return {'channels': [{'channel_id': int, 'name': str}]}
        dictionary containing list of dictionaries with keys channel_id and name
        
        For a dm:
        return {'dms': [{'dm_id': (int), 'name': (str)}]}
        dictionary containing list of dictionaries with keys channel_id and name
    '''
    check_valid_token(token)  
    
    data = load_database() 
    
    users = data['users'] 
    groups = data[group_type + 's']
    group_id_str = group_type + '_id'
    group_member_ids = group_type + '_member_ids'    

    user = [user for user in users if token in user['token']][0]

    user_groups = [group for group in groups if user['u_id'] in group[group_member_ids]]

    list_groups = []

    for group in user_groups:
        list_groups.append({
            group_id_str: group[group_id_str],
            'name': group['name']
        })

    return {group_type + 's': list_groups, } 

# ------------------------------- #
# message_send and message_senddm #
# ------------------------------- #
def send_group_message(token, group_id, message, group_type):
    """
    Send a message from authorised_user to the group specified by group_id and group_type. 
    Each message has its own unique ID within a group type but may share an id across groups.
    i.e. channel_id = 0 & dm_id = 0 refers to 2 different messages, one with a unique channel_id, one with a unique dm_id
         channel_id = 0 & channel_id = 0 refers to 1 message with a unique channel_id

    Arguments:
        token (str)         - unique token for user in active session
        group_id (int)      - the unique id of a group within a given group_type
        message (str)       - either the string "dm" if the groups being listed 
                                are dms or "channel" if the groups being listed
                                are channels
        group_type (str)    - either 'channel' or 'dm' to specify the type of group to send a message to

    Exceptions:
        AccessError - Occurs when the token user is not a member of the group
        InputError - Ocurs when the message is >1000 characters.

    Return Value:
        return {'message_id': (int)}
        dictionary containing the message id of the group message
    """
    check_valid_token(token)  
    
    data = load_database()

    groups = data[group_type + 's']
    group_id_str = group_type + '_id'

    # Check that group exists
    if group_id == None or group_id not in [group[group_id_str] for group in groups]:
        raise AccessError(description="User is not a member of the DM they are trying to post to")

    # Check the member trying to send a message is in the group
    if not check_user_in_group(token, 'token', group_id, group_type):
        raise AccessError(description=f"Only members of a {group_type} can send messages in that {group_type}")

    # message <= 1000 characters
    if len(message) > 1000:
        raise InputError(description="Message cannot exceed 1000 characters")
    if message == '':
        raise InputError(description="Message cannot be empty")

    auth_user_id = extract_u_id(token)
    message_id = send_message(group_id, message, group_type, data, auth_user_id)

    return {'message_id': message_id}

def send_message(group_id, message, group_type, data, auth_user_id):
    """
    Description:
        Stores a given message in the database
    """
    timestamp = extract_current_time()
    message_id = create_id(data['messages'], "message")
    
    if group_type == "channel":
        channel_id = group_id
        dm_id = -1
    
    if group_type == "dm":
        channel_id = -1
        dm_id = group_id
   
    new_message = {
        'message_id' : message_id,
        'u_id': auth_user_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'message': message,
        'time_created': timestamp,
        'reacts': [],
        'is_pinned': False,
    }   
    
    data['messages'].append(new_message)
    
    # Save changes to data.json file
    save_to_database(data)

    # create_notification commented out while waiting on function.,    
    create_notification(-1, auth_user_id, group_id, message_id, group_type, -1) 
    
    return message_id

# -------------------------------- #
# channel_messages and dm_messages #
# -------------------------------- #
def extract_messages_from_group(token, group_id, start, message_type):
    '''
    Provide a list of up to 50 messages (and their associated details) sent within 
    a channel or dm. The messages given begin from an index specified by the user, once 
    all the messages after that index have been given or 50 messages have been
    given, the user is also given the index of the next message or is told they have 
    reached the end of the messages. The messages are ordered in terms of the most 
    recently creates messages.

    Arguments:
        auth_user_id    (int)   - id of user
        group_id        (int)   - id of channel or dm
        start           (int)   - index for most recent message returned 
        message_type    (str)   - string (either 'channel' or 'dm' which indicates whether to 
                                  extract messages from a channel or from a dm.

    Exceptions:
        InputError  -   Occurs when input parameters are in different type, 
                            channel or dm ID given is invalid or start message 
                            is out of range.
        
        AccessError -   Occurs when input auth_user_id does not exit or the 
                            auth_user_id is not a member of the channel or dm it
                            wishes to see messages from.

    Return Value:
       return {
            'messages': 
                [   
                    {
                        'message_id': (int),
                        'u_id': (int),
                        'message': (str),
                        'time_created': (int),
                    }
                ],
            'start': (int),
            'end': (int),
        }
        dictionary containing:  list of dictionary (with keys message_id, u_id, 
                                message and time_created), start and end
                        
    '''
    # Confirm that the given user is a valid 
    check_valid_token(token)

    # Confirm that the given user is member of the group they are attempting
    # to view messages from.
    if not check_user_in_group(token, 'token', group_id, message_type):
        raise AccessError(description=f'Authorising user not in this {message_type}')
    
    data = load_database() 

    start = int(start)    
    
    group_id_str = message_type + '_id'

    messages = data["messages"]

    NUM_MESSAGES_RETURNED = 50
    end = start + NUM_MESSAGES_RETURNED
    output = {'messages': [], 'start': start, 'end': end}
    
    # Add message details to be returned for the appropriate group.
    group_messages = [message for message in messages if message[group_id_str] == group_id]
    num_messages = len(group_messages)
    
    # Check that the range of messages to be displayed is possible.        
    if start > num_messages:
        raise InputError(description=f"There are no messages beyond index {start} to be displayed")

    # Set the value of end for cases where there are or aren't remaining 
    # messages to be displayed
    output['end'] = -1 if end >= num_messages else end

    for message in group_messages:
        message_data = {
            'message_id': message['message_id'], 
            'u_id': message['u_id'], 
            'message': message['message'], 
            'time_created': message['time_created'],
            'reacts': message['reacts'],
            'is_pinned': message['is_pinned'],
        }
        output['messages'].append(message_data)
        
    output['messages'].sort(key = extract_time, reverse = True)
    
    # Splice the output messages so only the appropriate range is displayed.
    output['messages'] = output['messages'][start : end]      
    
    return output

## Function used to extract the time_created element from a dictionary
def extract_time(dictionary):
    return dictionary['time_created']


