from json import dumps, loads
from src.common import send_message
from src.error import InputError, AccessError
from src.helper_func import check_valid_group_id, check_valid_token, check_user_in_group, extract_current_time, extract_u_id, load_database, save_to_database
import threading

def standup_start_v1(token, channel_id, length):
    '''
    Description: 
        For a given channel, starts the standup period whereby for the next "length" seconds if someone calls "standup_send" with a message, 
        it is buffered during the X second window. Then at the end of the X second window, a message will be added to the message queue in the channel 
        from the user who started the standup. X is an integer that denotes the number of seconds that the standup occurs for.

    Arguments:
        token           <int>   -  the token of the authorised user (who is part of the channel) that is starting the standup
        channel_id      <int>   -  the id of the channel where the standup will occur
        length          <int>   -  the length of the standup from the time it starts (in seconds)
    
    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the channel or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the channel_id does not refer to a valid channel or
                              when an active standup is currently occuring in the channel or
                              when length is not a valid input

    Return Value:
       {time_finish}    <int>  -  the time the standup will finish (Unix timestamp)
    '''
    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')

    if not check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description='Authorised user must be in the channel')

    if not isinstance(length, int):
        raise InputError(description="Standup length must be an integer in seconds")
    
    data = load_database()

    channels = data['channels']

    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]

    if channel['time_finish'] != None:
        raise InputError(description="A standup is already active in this channel")

    # start thread to send summary 
    t = threading.Timer(float(length), collate_and_send_standup_summary, (token, channel_id))
    t.start()

    # calculate time finish
    time_start = extract_current_time()
    time_finish = time_start + length

    channel['time_finish'] = time_finish

    save_to_database(data)

    return {'time_finish': time_finish}

def standup_active_v1(token, channel_id):
    '''
    Description: 
        For a given channel, return whether a standup is active in it, and what time the standup finishes. 
        If no standup is active, then time_finish returns None.

    Arguments:
        token           <int>   -  the token of the authorised user (who is part of the channel) that is checking if a standup is active.
        channel_id      <int>   -  the id of the channel where the user is enquiring about the standup status
    
    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the channel or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the channel_id does not refer to a valid channel

    Return Value:
       {
            is_active,     <bool>  -  indicates whether a standup is active in the channel or not. 
            time_finish    <int> or None  -  the time the standup will finish 
       }
    '''
    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')
    
    if not check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description='Authorised user must be in the channel')
    
    data = load_database()
    
    channels = data["channels"]

    # Get the channel
    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]

    active_condition = channel['time_finish'] != None

    return {'is_active': active_condition, 'time_finish': channel['time_finish']}

def standup_send_v1(token, channel_id, message):
    '''
    Description: 
        Sending a message to get buffered in the standup queue, assuming a standup is currently active.
        
    Arguments:
        token           <int>   -  the token of the authorised user (who is part of the channel) that is sending the standup message
        channel_id      <int>   -  the id of the channel where the standup message is being sent
        message         <int>   -  the startup message being sent
    
    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the channel or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the channel_id does not refer to a valid channel or
                              when a standup is not currently active in the channel or
                              when message is more than 1000 characters (not including the username and colon)

    Return Value:
        {}  
    '''
    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')
    
    if not check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description='Authorised user must be in the channel')
    
    data = load_database()
    
    channels = data["channels"]
    users = data['users']

    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]

    if channel['time_finish'] == None:
        raise InputError(description="A standup is not currently active in this channel")

    if len(message) > 1000:
        raise InputError(description=f"Message in {channel['name']} standup is too long")

    # add message to standup_summary
    user = [user for user in users if token in user['token']][0]

    channel['standup_messages'].append(f"{user['handle_str']}: {message}")

    save_to_database(data)

    return {}

def collate_and_send_standup_summary(token, channel_id):
    '''
    Once standups are finished, 

    Description: 
        Sends a standup summary message to the channel where the standup occured. The message contains all of the messages sent during the 
        standup packaged together in one single message, posted by the user who started the standup, and is timestamped at the moment the 
        standup finished.
        
    Arguments:
        token           <int>   -  the token of the user that started the standup
        channel_id      <int>   -  the id of the channel where the standup is being held
    
    Exceptions:
        None
    
    Assumption:
        When no messages are sent in a standup (i.e. summary_message = ''), the summary message is replaced to indicate this 
        so that a valid message can be sent.

    Return Value:
        {}  
    '''

    data = load_database()
    
    channels = data['channels']

    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]

    summary_message = '\n'.join(channel['standup_messages'])

    if summary_message == '':
        summary_message = '[No messages were sent during this standup]'

    auth_user_id = extract_u_id(token)
    send_message(channel_id, summary_message, 'channel', data, auth_user_id)

    channel['time_finish'] = None
    channel['standup_messages'] = []

    return {}
