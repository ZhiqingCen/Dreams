'''
extra features for Dreams
'''
from src.error import AccessError, InputError
from src.helper_func import check_valid_token, check_valid_user_id, load_database, save_to_database, extract_u_id, check_valid_channel_owner, check_valid_dm_owner, check_valid_channel_id, check_valid_dm_id
from json import dumps, loads

def group_rename(token, name, group_id, group_type):
    check_valid_token(token)
    data = load_database()
    channels = data["channels"]
    dms = data["dms"]

    auth_user_id = extract_u_id(token)

    if name == None or name == "" or not isinstance(name, str):
        raise InputError(description = "please enter a valid name")
    if len(name) > 20:
        raise InputError(description = "name cannot exceed 20 characters")
    if group_id == None or not isinstance(group_id, int):
        raise InputError(description = "invalid channel/dm id")

    if group_type == "channel":
        if not check_valid_channel_id(group_id):
            raise InputError(description = "invalid channel id")
        if not check_valid_channel_owner(auth_user_id, group_id):
            raise AccessError(description = "only channel owner have permission to change channel name")
        for channel in channels:
            if channel["channel_id"] == group_id:
                channel["name"] = name
    elif group_type == "dm":
        if not check_valid_dm_id(group_id):
            raise InputError(description = "invalid dm id")
        if not check_valid_dm_owner(auth_user_id, group_id):
            raise AccessError(description = "only dm owner have permission to change dm name")
        for dm in dms:
            if dm["dm_id"] == group_id:
                dm["name"] = name
    else:
        raise InputError(description = "invalid group type")

    save_to_database(data)

    return {}