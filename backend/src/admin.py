from src.error import AccessError, InputError
from src.helper_func import check_valid_user_id, check_valid_token, load_database, save_to_database
from json import dumps, load, loads

def admin_remove_user_v1(token, u_id):
    '''
    Description: 
       Given a User by their user ID, remove the user from the Dreams. 
       Dreams owners can remove other **Dreams** owners (including the original first owner). 
       Once users are removed from **Dreams**, the contents of the messages they sent will be replaced by 'Removed user'. 
       Their profile must still be retrievable with user/profile/v2, with their name replaced by 'Removed user'.

    Arguments:
        token    <str>   - the token of the authorised user making the change
        u_id     <int>   - the u_id of the user being removed from Dreams

    Exceptions:
        AccessError -  Occurs when the authorised user is not an owner          or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the u_id does not refer to a valid user      or
                              when the u_id is currently the only owner

    Return Value:
        Returns {}
    '''
    data = load_database()
    
    users = data['users']
    messages = data['messages']

    check_valid_token(token)

    check_valid_user_id(u_id)

    token_user = [user for user in users if token in user['token']][0]
    u_id_user = [user for user in users if user['u_id'] == u_id][0]

    if not token_user['global_owner']:
        raise AccessError(description="You are not authorised to make this change.")

    #check u_id is not only global owner
    if u_id_user['global_owner'] and count_global_owners(users) == 1:
        raise InputError(description="You cannot remove yourself if you are the only owner of Dreams.")

    # Remove user:

    # change name to Removed User
    u_id_user['name_first'] = "Removed"
    u_id_user['name_last'] = "user"

    # remove token
    u_id_user['token'] = ''

    #Find channels they are a part of and remove them
    remove_user_from_groups(data, u_id_user, 'channel')

    #Find dms they are a part of and remove them
    remove_user_from_groups(data, u_id_user, 'dm')

    # replace user's messages contents to "Removed User"
    user_messages = [message for message in messages if message['u_id'] == u_id]
    for message in user_messages:
        message['message'] = "Removed user"

    # Save changes to data.json file
    save_to_database(data)

    return {}

def admin_change_user_permissions_v1(token, u_id, permission_id):
    '''
    Description: 
       Given a User by their user ID, set their permissions to new permissions described by permission_id

    Arguments:
        token           <str>   - the token of the authorised user making the change
        u_id            <int>   - the u_id of the user whose permissions are being changed
        permission_id   <int>   - the permission type to assign the user. Global Owner = id 1, Member = id 2.

    Exceptions:
        AccessError -  Occurs when the authorised user is not an owner          or
                              when the authorised user is not a valid user
        InputError  -  Occurs when the u_id does not refer to a valid user      or
                              when the permission_id does not refer to a valid permission type

    Return Value:
        Returns {}
    '''
    
    data = load_database() 
    
    users = data['users']

    check_valid_token(token)

    check_valid_user_id(u_id)

    check_valid_permission_id(permission_id)

    token_user = [user for user in users if token in user['token']][0]
    u_id_user = [user for user in users if user['u_id'] == u_id][0]

    if not token_user['global_owner']:
        raise AccessError(description="You are not authorised to make this change.")

    #check u_id is not only global owner
    if u_id_user['global_owner'] and permission_id == 2 and count_global_owners(users) == 1:
        raise InputError(description="You cannot downgrade your permissions if you are the only owner of Dreams.")

    # Find the user matching u_id and change permissions
    u_id_user['global_owner'] = (permission_id == 1)

    # Save changes to data.json file
    save_to_database(data)

    return {}

###------------------###
### Helper Functions ###
###------------------###

def check_valid_permission_id(permission_id):
    if permission_id not in [1,2]:
        raise InputError(description="The permission type entered does not exist.")
    
    return True

def count_global_owners(users):
    return len([user for user in users if user['global_owner'] == True])

def remove_user_from_groups(data, user, group_type):
    
    groups = data[group_type + 's'] 
    group_member_ids = group_type + '_member_ids'
    group_owner_ids = group_type + '_owner_ids'

    user_groups = [group for group in groups if user['u_id'] in group[group_member_ids]]
    
    if user_groups:
        for group in user_groups:
            group[group_member_ids].remove(user['u_id'])
            if user['u_id'] in group[group_owner_ids]:
                group[group_owner_ids].remove(user['u_id'])