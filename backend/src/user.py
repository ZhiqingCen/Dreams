import os
import sys
import jwt
import random
import requests
import urllib.request as img
from PIL import Image
from json import dumps, loads
from src.error import InputError, AccessError
from src.auth import val_email
from src.helper_func import check_valid_token, extract_current_time, extract_u_id, check_valid_channel_member, check_valid_dm_member, check_valid_message_sender, load_database, save_to_database

SECRET = 'COMP1531AERO'

def valid_name(name_first, name_last):
    if f"{name_first} {name_last}" == 'Removed user':
        raise InputError(description='Invalid first or last name, cannot use the name Removed User')
    if len(name_first) < 1:
        raise InputError(description='Please enter a first name')
    if len(name_first) > 50:
        raise InputError(description='First name is too long')
    if len(name_last) < 1:
        raise InputError(description='Please enter a last name')
    if len(name_last) > 50:
        raise InputError(description='Last name is too long')
    return True

def user_profile_v2(token, u_id):
    check_valid_token(token)
    
    data = load_database()
    users = data['users']

    if u_id == None or u_id not in [user['u_id'] for user in users]:
        raise InputError(description="The user id is invalid.")

    user = [user for user in users if u_id == user['u_id']][0]

    return {
        'user': {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],
            'profile_img_url': user['profile_img_url']
        },
    }

def user_profile_setname_v2(token, name_first, name_last):
    check_valid_token(token)
    
    data = load_database()
    users = data['users']

    if valid_name(name_first, name_last):
        user = [user for user in users if token in user['token']][0]

        user['name_first'] = name_first
        user['name_last'] = name_last
        
        save_to_database(data)
    return {}

def user_profile_setemail_v2(token, email):
    check_valid_token(token)
    val_email(email)
    
    data = load_database()
    users = data['users']
    
    if email in [user['email'] for user in users]:
        raise InputError(description='Email already in use')

    token_user = [user for user in users if token in user['token']][0]

    token_user['email'] = email

    save_to_database(data)
    return {}

def user_profile_sethandle_v1(token, handle_str):
    check_valid_token(token)
    
    data = load_database()
    users = data['users']
    if len(handle_str) < 3:
        raise InputError(description='Handle must be at least 3 characters')
    if len(handle_str) > 20:
        raise InputError(description='Handle must be at most 20 characters')
    
    if handle_str in [user['handle_str'] for user in users]:
            raise InputError(description='Handle already in use')

    token_user = [user for user in users if token in user['token']][0]

    token_user['handle_str'] = handle_str

    save_to_database(data)
    return {}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    data = load_database()
    users = data['users']

    check_valid_token(token)
    
    image_name = random.randint(100000,999999)

    fullfilename = os.path.join('src/imgurl/', f'{image_name}.jpg')
    img.urlretrieve(img_url, str(fullfilename))
    image_file = Image.open(fullfilename)

    if image_file.format != 'JPEG':
        os.remove(fullfilename)
        raise InputError('File must be a JPEG')

    width, height = image_file.size

    if (
        x_start < 0 or 
        y_start < 0 or 
        (x_end - x_start) < 0 or 
        (y_end - y_start) < 0 or 
        (x_end - x_start) > width or 
        (y_end - y_start) > height):
        os.remove(fullfilename)
        raise InputError('Crop invalid')

    cropped = image_file.crop((x_start, y_start, x_end, y_end))
    cropped.save(fullfilename)

    for user in users:
        for tokens in user['token']:
            if tokens == token:
                user['profile_img_url'] = fullfilename

    save_to_database(data)
    return {}

def users_all_v1(token):
    check_valid_token(token)
    
    data = load_database()
    users = data['users']

    user_list = []
    for user in users:
        user_list.append({'u_id': user['u_id'], 'email': user['email'], 'name_first': user['name_first'], 'name_last': user['name_last'], 'handle_str': user['handle_str']})
    
    return {"users": user_list}


def user_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Dreams

    Arguments:
        token(str) - token of user

    Exceptions:
        NA

    Return Value:
        return {user_stats:
            {channels_joined: [{num_channels_joined, time_stamp}],
            dms_joined: [{num_dms_joined, time_stamp}], 
            messages_sent: [{num_messages_sent, time_stamp}], 
            involvement_rate} 
        }
    '''
    check_valid_token(token)
    
    data = load_database()
    channels = data['channels']
    dms = data['dms']
    messages = data['messages']
    
    auth_user_id = extract_u_id(token)

    channels_joined = []
    dms_joined = []
    messages_sent = []

    timestamp = extract_current_time()

    for channel in channels:
        if check_valid_channel_member(auth_user_id, channel['channel_id']):
            channels_joined.append(channel['channel_id'])
    for dm in dms:
        if check_valid_dm_member(auth_user_id, dm['dm_id']):
            dms_joined.append(dm['dm_id'])
    for message in messages:
        if check_valid_message_sender(auth_user_id, message['message_id']):
            messages_sent.append(message['message_id'])
    if len(channels) == 0 and len(dms) == 0 and len(messages) == 0:
        involvement_rate = 0
    else:
        involvement_rate = (len(channels_joined) + len(dms_joined) + len(messages_sent)) / (len(channels) + len(dms) + len(messages))

    user_stats = {
        'channels_joined': [{'num_channels_joined': len(channels_joined), 'time_stamp': timestamp}],
        'dms_joined': [{'num_dms_joined': len(dms_joined), 'time_stamp': timestamp}],
        'messages_sent': [{'num_messages_sent': len(messages_sent), 'time_stamp': timestamp}],
        'involvement_rate': involvement_rate,
    }
    return {'user_stats': user_stats,}

def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Dreams

    Arguments:
        token(str) - token of user

    Exceptions:
        NA

    Return Value:
        return {dreams_stats: 
            {channels_exist: [{num_channels_exist, time_stamp}], 
            dms_exist: [{num_dms_exist, time_stamp}], 
            messages_exist: [{num_messages_exist, time_stamp}], 
            utilization_rate }
        }
    '''
    check_valid_token(token)
    
    data = load_database()
    users = data['users']
    channels = data['channels']
    dms = data['dms']
    messages = data['messages']

    extract_u_id(token)

    users_joined = []
    
    timestamp = extract_current_time()

    for user in users:
        status = False
        for channel in channels:
            if check_valid_channel_member(user['u_id'], channel['channel_id']):
                status = True
        for dm in dms:
            if check_valid_dm_member(user['u_id'], dm['dm_id']):
                status = True
        if status:
            users_joined.append(user['u_id'])

    if len(users) == 0:
        utilization_rate = 0
    else:
        utilization_rate = len(users_joined) / len(users)

    dreams_stats = {
        'channels_exist': [{'num_channels_exist': len(channels), 'time_stamp': timestamp,}],
        'dms_exist': [{'num_dms_exist': len(dms), 'time_stamp': timestamp,}],
        'messages_exist': [{'num_messages_exist': len(messages), 'time_stamp': timestamp,}],
        'utilization_rate': utilization_rate,
    }
    return {"dreams_stats": dreams_stats,}