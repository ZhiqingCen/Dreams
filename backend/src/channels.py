'''
implement channels_list_v1, channels_listall_v1, channels_create_v1
'''
from src.error import AccessError, InputError
from src.helper_func import check_valid_token, check_valid_user_id, load_database, save_to_database
from json import dumps, loads

def channels_listall_v2(token):
    
    check_valid_token(token)
    
    data = load_database()
    channels = data["channels"]

    all_channels = []
    for channel in channels:
        all_channels.append({
            'channel_id': channel['channel_id'],
            'name': channel['name']
        })

    return {'channels': all_channels}

def channels_create_v2(token, name, is_public):
    
    check_valid_token(token)

    data = load_database()
    channels = data["channels"]
    users = data['users']

    token_user = [user for user in users if token in user['token']][0]

    if name == None or not isinstance(name, str):
        raise InputError(description="Input for name cannot be 'None'")
    elif len(name) > 20:
        raise InputError(description="Invalid input, name cannot be more than 20 characters")
    elif len(name) == 0:
        raise InputError(description="Invalid input, please enter a channel name")

    if not isinstance(is_public, bool):
        raise InputError(description="Invalid input, please enter whether the channel is public or private")

    # get channel_id
    channel_id = 0
    for channel in channels:
        if channel["channel_id"] == channel_id:
            channel_id += 1

    # store channel details
    new_channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'channel_owner_ids': [],
        'channel_member_ids': [],
        'time_finish': None,
        'standup_messages': [],
    }

    # owner_id, member_id, message lists are to be added in next iteration
    new_channel['channel_owner_ids'].append(token_user['u_id'])
    new_channel['channel_member_ids'].append(token_user['u_id'])

    # add new_channel to list of channels
    channels.append(new_channel)

    save_to_database(data)

    return {'channel_id': channel_id}