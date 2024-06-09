from src.error import AccessError, InputError
from json import dumps, loads
from src.helper_func import check_valid_token, check_valid_group_id, check_user_in_group, check_valid_user_id, load_database, save_to_database

def channel_join_v2(token, channel_id):
    '''
     Description: 
        Given a channel_id of a channel that the authorised user can join, adds them to that channel

    Arguments:
        token           <int>   - the token of the authorised user that is joining the channel
        channel_id      <int>   - the id of the channel the authorised user is joining

    Exceptions:
        AccessError -  Occurs when the authorised user is already a member of the channel or
                              when the authorised user is not a valid user or
                              when the channel is private and the authorised user is not a global owner
        InputError  -  Occurs when the channel_id does not refer to a valid channel

    Return Value: 
        Returns {}
    '''

    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')

    data = load_database()
    
    channels = data['channels']
    users = data['users']
    
    if check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description=f"You are already a member of this channel")
    
    #  Get the channel they are trying to join
    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]

    # Get the user trying to join
    user = [user for user in users if token in user['token']][0]

    if not channel['is_public'] and not user['global_owner']:
        raise AccessError(description=f"You are not authorised to join a private channel")

    # Add the authorised user to the channel
    channel['channel_member_ids'].append(user['u_id'])

    if user['global_owner']:
        channel['channel_owner_ids'].append(user['u_id'])
    
    # Save changes to data.json file
    save_to_database(data)
    
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    '''
     Description: 
        Makes user with user id u_id an owner of the channel with channel_id

    Arguments:
        token           <int>   - the token of the authorised user that is adding an owner
        channel_id      <int>   - the id of the channel recieving an owner
        u_id            <int>   - the id of the user being added as an owner

    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the channel or
                              when the authorised user is not a valid user or
                              when the authorised user is not a global owner or channel owner
        InputError  -  Occurs when the channel_id does not refer to a valid channel or
                              when the u_id is already an owner of the channel or
                              when the u_id does not refer to a valid user

    Return Value: 
        Returns {}
    '''
    
    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')
    check_valid_user_id(u_id)

    data = load_database() 
    
    channels = data['channels']
    users = data['users']

    if not check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description="Authorising user is not a member of this channel")

    # add user if not in channel

    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]
    token_user = [user for user in users if token in user['token']][0]

    if not token_user['global_owner'] and token_user['u_id'] not in channel['channel_owner_ids']:
        raise AccessError(description="Authorising user is authorised to change this channel's permissions")

    if u_id in channel['channel_owner_ids']:
        raise InputError(description="User is already an owner of this channel")

    if not check_user_in_group(u_id, 'u_id', channel_id, 'channel'):
        channel['channel_member_ids'].append(u_id)

    #add ownership
    channel['channel_owner_ids'].append(u_id)

    # Save changes to data.json file
    save_to_database(data)

    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
     Description: 
        Removes user with user id u_id as an owner of the channel with channel_id

    Arguments:
        token           <int>   - the token of the authorised user that removing an owner
        channel_id      <int>   - the id of the channel that the owner is being removed from
        u_id            <int>   - the id of the user being removed as an owner

    Exceptions:
        AccessError -  Occurs when the authorised user is not a member of the channel or
                              when the authorised user is not a valid user or
                              when the authorised user is not a global owner or channel owner
        InputError  -  Occurs when the channel_id does not refer to a valid channel or
                              when the u_id is not a valid user or
                              when the u_id is not in the channel or
                              when the u_id is not an owner in the channel

    Return Value: 
        Returns {}
    '''
    
    check_valid_token(token)
    check_valid_group_id(channel_id, 'channel')
    check_valid_user_id(u_id)
    
    data = load_database()
    
    channels = data['channels']
    users = data['users']

    channel = [channel for channel in channels if channel['channel_id'] == channel_id][0]
    token_user = [user for user in users if token in user['token']][0]

    if not check_user_in_group(token, 'token', channel_id, 'channel'):
        raise AccessError(description="Authorising user is not a member of this channel")

    if not token_user['global_owner'] and token_user['u_id'] not in channel['channel_owner_ids']:
        raise AccessError(description="Authorising user is authorised to change this channel's permissions")

    if u_id not in channel['channel_member_ids']:
        raise InputError(description="User is not an member of this channel")

    if u_id not in channel['channel_owner_ids']:
        raise InputError(description="User is not an owner of this channel")

    if count_channel_owners(channel) == 1:
        raise InputError(description="You cannot remove the only owner of a channel")

    # remove ownership  
    channel['channel_owner_ids'].remove(u_id)

    # Save changes to data.json file
    save_to_database(data)

    return {}

def count_channel_owners(channel):
    return len(channel['channel_owner_ids'])
