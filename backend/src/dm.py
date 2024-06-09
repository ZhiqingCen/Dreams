from json import dumps, loads
from flask import Flask, request
from src.error import AccessError, InputError
from src.helper_func import check_valid_group_id, check_valid_token, check_valid_user_id, create_id, extract_dm_details, extract_u_id, load_database, save_to_database

def dm_create_v1(token, u_ids):
    '''
    Given a token and list of u_ids, create a dm with the token as the owner and
    listed u_ids as the members

    Arguments:
        token(str) - unique token for user in active session
        u_ids(list of str) - the u_ids of members to be added to dm

    Exceptions:
        InputError - Occurs when any u_id given is invalid
        AccessError - Occurs when given token is invalid

    Return Value:
        return {'dm_id': (int), 'dm_name': (str)}
        dictionary containing the dm_name which is an alphabetical list of the 
        member handles and the unique dm_id.

    '''
    for u_id in u_ids:
        check_valid_user_id(u_id)
    
    data = load_database()
    dms = data['dms']
    users = data['users']
    
    dm_name, owner_u_id = extract_dm_details(users, token, u_ids)
    
    u_ids.append(owner_u_id)
    
    dm_id = create_id(dms, "dm")
    
    # Add the new dm to the exsisting database of dms
    dms.append({
        'dm_owner_ids': [owner_u_id],
        'dm_id': dm_id,
        'dm_member_ids': u_ids,
        'name': dm_name
    })

    save_to_database(data)
        
    return {'dm_id': dm_id, 'dm_name': dm_name}

def dm_remove_v1(token, dm_id):
    '''
    Given a token and a dm_id, remove the dm with dm_id from the database
    if the user with token is the owner of that dm.

    Arguments:
        token(str) - unique token for user in active session
        dm_ids(int) - unique id for dm
    
    Exceptions:
        InputError  -   Occurs when dm_id given is invalid
        AccessError -   Occurs when given token is invalid or user with token is
                            not the owner of the dm they are tryimng to delete.

    Return Value:
        return {}   -   Empty dictionary

    '''
    # Check token is from a valid user
    check_valid_token(token)
    
    # Confirm the given dm_id exists in the database.
    check_valid_group_id(dm_id, 'dm')
    
    data = load_database() 
    dms = data['dms']

    token_user_id = extract_u_id(token)
    
    # Check that the user calling dm_remove is the owner of the dm they are removing
    if token_user_id not in [dm['dm_owner_ids'][0] for dm in dms if dm['dm_id'] == dm_id]:
        raise AccessError(description="Only a DM owner can remove a DM")
      
    # Remove a dm from the dms list if it has a DM ID of dm_id
    data['dms'] = [dm for dm in dms if dm['dm_id'] != dm_id]
    
    # Save changes to data.json file
    save_to_database(data)

    return {}





