from json import dumps, loads
from time import time
from src.error import AccessError, InputError

def load_database():
    with open('data.json', 'r') as file:
        return loads(file.read())

def save_to_database(data):
    with open('data.json', 'w') as write_file:
        write_file.write(dumps(data))

def create_id(groups, group_type):
    '''
    Given a list of groups, create a new group_id which is not used by any 
    existing group.

    Arguments:
        groups (list of directories) - database of existing groups
        group_type (str) - string of "u" for users, "channel" for channels and 
                            "dm" for dms

    Return Value:
        return group_id - unique ID for a given group
    '''
    group_id_str = group_type + "_id"
       
    group_id = 0
    for group in groups:
        if group[group_id_str] == group_id:
            group_id += 1
    
    return group_id

def extract_current_time():
    return int(time())

# function to check if token valid
def extract_u_id(token):
    data = load_database()
    
    users = data["users"]
    
    # Check token is from a valid user
    check_valid_token(token)

    token_user = [user for user in users if token in user['token']][0]

    return token_user['u_id']

def extract_dm_details(users, token, u_ids):
    '''
    Given a list of users, a token and a list of u_ids, extract the owner_u_id 
    from the u_id of the token and create a dm_name using the handles of the 
    owner and the users given in the list of u_ids.

    Arguments:
        users (list of directories) - data stored of exsisting users
        token (string) - unique token for the owner of a dm
        u_ids (list of int) - list of u_ids of members with a dm.
    
    Exceptions:
        AccessError - Occurs when given token is not stored in users data.
    
    Return Value:
        return (dm_name (str), owner_u_id (int))
        Tuple containing the generated string dm_name which is a list of the 
        user handles and the owner_u_id which is the u_id extracted from token.
    '''
    user_handles = []
    
    valid_token = False
    for user in users:
        for active_token in user['token']:
            if active_token == token:
                # If valid token is found add corresponding user handle to 
                # user_handles and assign owner_u_id.
                valid_token = True
                owner_u_id = user['u_id']
                user_handles.append(user['handle_str'])
        # Add handles of users within u_ids to user_handles
        for u_id in u_ids:
            if user['u_id'] == u_id:
                user_handles.append(user['handle_str'])
                
    if not valid_token:
        raise AccessError(description="invalid token")
    
    # Extract the appropriate dm_name given the user handles
    user_handles.sort()
    dm_name = ", ".join(user_handles)
    
    return (dm_name, owner_u_id)

# function to check if u_id is valid - do not use for token!! this needs a different function that will raise an Access Error instead
def check_valid_token(token):
    data = load_database()
    
    users = data["users"] 

    token_lists = [user['token'] for user in users]
    user_tokens = [token for list_of_tokens in token_lists for token in list_of_tokens]

    if token == None:
        raise AccessError(description="The token is invalid.")
    elif token not in [token for token in user_tokens]:
        raise AccessError(description="The token is invalid or the token user has logged out.")
    elif "Removed user" in [f"{user['name_first']} {user['name_last']}" for user in users if token in user['token']]:
        raise AccessError(description="The authorising user is invalid.")

    return True

# function to check if u_id is valid - do not use for token!! this needs a different function that will raise an Access Error instead
def check_valid_user_id(u_id):
    data = load_database()

    users = data['users']

    if u_id == None or u_id not in [user['u_id'] for user in users]:
        raise InputError(description="The user id is invalid.")
    elif "Removed user" in [f"{user['name_first']} {user['name_last']}" for user in users if user['u_id'] == u_id]:
        raise InputError(description="The user id belongs to a removed user.")

    return True


def check_valid_group_id(group_id, group_type):
    data = load_database()

    groups = data[group_type + 's'] 
    group_id_str = group_type + '_id'

    if group_id == None or group_id not in [group[group_id_str] for group in groups]:
        raise InputError(description="The group id is invalid.")

    return True

def check_user_in_group(identifier, id_type, group_id, group_type):
    '''
    Returns false if the user with identifier is not in the group, and True otherwise
    '''

    data = load_database()
    
    check_valid_group_id(group_id, group_type)

    groups = data[group_type + 's'] 
    group_id_str = group_type + '_id'
    group_member_ids = group_type + '_member_ids'

    users = data['users']
    
    if id_type == 'token':
        user = [user for user in users if identifier in user['token']][0]
    
    if id_type == 'u_id':
        user = [user for user in users if user['u_id'] == identifier][0]
    
    if user['u_id'] not in [group[group_member_ids] for group in groups if group[group_id_str] == group_id][0]:
        return False

    return True

# function to check if channel_id exist
def check_valid_channel_id(channel_id):
    data = load_database()

    channels = data['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id:
            return True
    return False

# function to check if user a member of a channel
def check_valid_channel_member(auth_user_id, channel_id):
    data = load_database()

    channels = data['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id and auth_user_id in channel['channel_member_ids']:
            return True
    return False

# function to check if member is an owner of a channel
def check_valid_channel_owner(auth_user_id, channel_id):
    data = load_database()

    channels = data['channels']

    for channel in channels:
        if channel['channel_id'] == channel_id and auth_user_id in channel['channel_owner_ids']:
            return True
    return False

# function to check if message_id exist
def check_valid_message_id(message_id):
    data = load_database()

    messages = data['messages']

    for message in messages:
        if message['message_id'] == message_id:
            return True
    return False

# function to check if member is the sender of a message:
def check_valid_message_sender(auth_user_id, message_id):
    data = load_database()

    messages = data['messages']

    for message in messages:
        if message['message_id'] == message_id and message['u_id'] == auth_user_id:
            return True
    return False

# Function which raises an InputError if message_id does not exist and returns the group_id the message was sent in.
def extract_message_group_id(message_id):
    data = load_database()

    messages = data["messages"]
    
    if not message_id in [message['message_id'] for message in messages]:
        raise InputError(description = 'message_id is invalid')
    
    for message in messages:
        if message['message_id'] == message_id:
            return {"channel_id": message['channel_id'], "dm_id": message['dm_id']}


# function to check if dm_id exist
def check_valid_dm_id(dm_id):
    data = load_database()

    dms = data['dms']

    for dm in dms:
        if dm['dm_id'] == dm_id:
            return True
    return False

# function to check if user is member of dm
def check_valid_dm_member(auth_user_id, dm_id):
    data = load_database()

    dms = data['dms']

    for dm in dms:
        if dm['dm_id'] == dm_id and auth_user_id in dm['dm_member_ids']:
            return True
    return False

# function to check if user is owner of dm
def check_valid_dm_owner(auth_user_id, dm_id):
    data = load_database()

    dms = data['dms']

    for dm in dms:
        if dm['dm_id'] == dm_id and auth_user_id in dm['dm_owner_ids']:
            return True
    return False

def create_notification(inviter_u_id, auth_user_id, group_id, message_id, group_type, react_id):
    
    data = load_database()

    messages = data['messages']
    notifications = data['notifications']

    if group_type == "channel":
        channel_id = group_id
        dm_id = -1
    
    if group_type == "dm":
        channel_id = -1
        dm_id = group_id

    # only get message details when inviter_u_id is -1
    message = -1
    reactors = []

    if message_id != -1:
        for m in messages:
            if m["message_id"] == message_id:
                message = m["message"]
                for react in m["reacts"]:
                    if react["react_id"] == react_id:
                        reactors = react["u_ids"]

    timestamp = extract_current_time()

    new_notification = {
        'u_id': auth_user_id,
        'inviter_u_id': inviter_u_id,
        'channel_id': channel_id,
        'dm_id': dm_id,
        'message': message,
        'time_create': timestamp,
        'react_id': react_id,
        'reactors': reactors,
    }

    notifications.append(new_notification)

    save_to_database(data)

    data = load_database()