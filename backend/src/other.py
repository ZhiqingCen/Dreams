from json import dumps, loads
from src.error import InputError
from src.helper_func import extract_u_id, load_database, save_to_database

def clear_v1():
    '''
    Description: Resets the internal data of the application to it's initial state

    Arguments: None

    Exceptions: None

    Return Value: None
    '''
    
    save_to_database({
        "users": [],
        "channels": [],
        "dms": [],
        "messages": [],
        "notifications": []
    })
    
    return {}

def search_v2(token, query_str):
    data = load_database() 
    
    messages = data['messages']
    channels = data['channels']
    dms = data['dms']
    
    if len(query_str) > 1000:
        raise InputError(description = "query_str is too long")
    
    search_results = {"messages": []}
    
    u_id = extract_u_id(token)
    
    user_dms = [dm['dm_id'] for dm in dms if (u_id in dm['dm_member_ids'])]
    user_channels = [channel['channel_id'] for channel in channels if (u_id 
        in channel['channel_member_ids'])]
    
    for message in messages:
        if message['dm_id'] in user_dms or message['channel_id'] in user_channels:
            search_results['messages'].append({
                'message_id': message['message_id'],
                'u_id': message['u_id'],
                'message': message['message'],
                'time_created': message['time_created'],
                'is_pinned': message['is_pinned'] 
            })    

    return search_results
