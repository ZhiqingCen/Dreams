from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.error import InputError
from src import config
from src.admin import admin_change_user_permissions_v1, admin_remove_user_v1
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.channels import channels_create_v2, channels_listall_v2
from src.channel import channel_addowner_v1, channel_removeowner_v1, channel_join_v2
from src.common import invite_to_group, group_details, leave_group, send_group_message, list_groups, extract_messages_from_group
from src.dm import dm_create_v1, dm_remove_v1
from src.notifications import notifications_get_v1
from src.message import message_edit_v2, message_share_v1, message_remove_v1, message_pinning, message_sendlater, message_react_v1, message_unreact_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.user import user_profile_v2, user_profile_setemail_v2, user_profile_sethandle_v1, user_profile_setname_v2, users_all_v1, user_stats_v1, users_stats_v1, user_profile_uploadphoto_v1
from src.other import search_v2, clear_v1
from src.extra_features import group_rename

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError('Cannot echo "echo"') #removed (description='') to pass pylint
    return dumps({
        'data': data
    })

###------------------------------------------###
###                  Admin                   ###
###------------------------------------------###

@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def admin_remove():
    data = request.get_json()
    return dumps(admin_remove_user_v1(data['token'], data['u_id']))

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def admin_user_permission_change():
    data = request.get_json()
    return dumps(admin_change_user_permissions_v1(data['token'], data['u_id'], data['permission_id']))

###------------------------------------------###
###                   Auth                   ###
###------------------------------------------###

@APP.route('/auth/login/v2', methods=['POST'])
def auth_login():
    data = request.get_json()
    return dumps(auth_login_v2(data['email'], data['password']))

@APP.route('/auth/register/v2', methods=['POST'])
def auth_register():
    data = request.get_json()
    return dumps(auth_register_v2(data['email'], data['password'], data['name_first'], data['name_last']))

@APP.route('/auth/logout/v1', methods=['POST'])
def auth_logout():
    data = request.get_json()
    return dumps(auth_logout_v1(data['token']))

@APP.route('/auth/passwordreset/request/v1', methods=['POST'])
def auth_passwordreset_request():
    data = request.get_json()
    return dumps(auth_passwordreset_request_v1(data['email']))

@APP.route('/auth/passwordreset/reset/v1', methods=['POST'])
def auth_passwordreset_reset():
    data = request.get_json()
    return dumps(auth_passwordreset_reset_v1(data['reset_code'], data['new_password']))


###------------------------------------------###
###                 Channel                  ###
###------------------------------------------###

@APP.route('/channel/invite/v2', methods=['POST'])
def channel_invite():
    data = request.get_json()
    return dumps(invite_to_group(data['token'], data['channel_id'], data['u_id'], 'channel'))

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    channel_id = channel_id if channel_id == None else int(channel_id)

    return dumps(group_details(token, channel_id, 'channel'))

@APP.route('/channel/messages/v2', methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    channel_id = None if channel_id == None else int(channel_id)

    start = None if start == None else int(start)

    return dumps(extract_messages_from_group(token, channel_id, start, 'channel'))

@APP.route('/channel/join/v2', methods=['POST'])
def channel_join():
    data = request.get_json()
    return dumps(channel_join_v2(data['token'], data['channel_id']))

@APP.route('/channel/addowner/v1', methods=['POST'])
def channel_addowner():
    data = request.get_json()
    return dumps(channel_addowner_v1(data['token'], data['channel_id'], data['u_id']))

@APP.route('/channel/removeowner/v1', methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    return dumps(channel_removeowner_v1(data['token'], data['channel_id'], data['u_id']))

@APP.route('/channel/leave/v1', methods=['POST'])
def channel_leave():
    data = request.get_json()
    return dumps(leave_group(data['token'], data['channel_id'], 'channel'))

###------------------------------------------###
###                 Channels                 ###
###------------------------------------------###

@APP.route("/channels/list/v2", methods = ['GET'])
def channels_list():
    token = request.args.get('token')
    return dumps(list_groups(token, 'channel'))

@APP.route("/channels/listall/v2", methods = ['GET'])
def channels_listall():
    token = request.args.get('token')
    return dumps(channels_listall_v2(token))

@APP.route("/channels/create/v2", methods = ['POST'])
def channels_create():
    data = request.get_json()
    return dumps(channels_create_v2(data['token'], data['name'], data['is_public']))

###------------------------------------------###
###                   Dm                     ###
###------------------------------------------###

@APP.route('/dm/details/v1', methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')

    dm_id = None if dm_id == None else int(dm_id)

    return dumps(group_details(token, dm_id, 'dm'))

@APP.route('/dm/list/v1', methods=['GET'])
def dm_list():
    token = request.args.get('token')
    return dumps(list_groups(token, 'dm'))

@APP.route("/dm/create/v1", methods = ['POST'])
def dm_create():
    data = request.get_json()
    return dumps(dm_create_v1(data['token'], data['u_ids']))

@APP.route("/dm/remove/v1", methods = ['DELETE'])
def dm_remove():
    data = request.get_json()
    return dumps(dm_remove_v1(data['token'], data['dm_id']))

@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite():
    data = request.get_json()
    return dumps(invite_to_group(data['token'], data['dm_id'], data['u_id'], 'dm'))

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    data = request.get_json()
    return dumps(leave_group(data['token'], data['dm_id'], 'dm'))

@APP.route('/dm/messages/v1', methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')

    dm_id = None if dm_id == None else int(dm_id)

    start = None if start == None else int(start)

    return dumps(extract_messages_from_group(token, dm_id, start, 'dm'))

###------------------------------------------###
###                 Message                  ###
###------------------------------------------###

@APP.route('/message/send/v2', methods=['POST'])
def message_send():
    data = request.get_json()
    return dumps(send_group_message(data['token'], data['channel_id'], data['message'], 'channel'))

@APP.route('/message/senddm/v1', methods=['POST'])
def message_senddm():
    data = request.get_json()
    return dumps(send_group_message(data['token'], data['dm_id'], data['message'], 'dm'))

@APP.route('/message/edit/v2', methods=['PUT'])
def message_edit():
    data = request.get_json()
    return dumps(message_edit_v2(data['token'], data['message_id'], data['message']))

@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    data = request.get_json()
    return dumps(message_remove_v1(data['token'], data['message_id']))

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    data = request.get_json()
    return dumps(message_share_v1(data['token'], data['og_message_id'], data['message'], data['channel_id'], data['dm_id']))

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    data = request.get_json()
    ret = message_react_v1(data['token'], data['message_id'], data['react_id'])
    return dumps(ret)

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    data = request.get_json()
    ret = message_unreact_v1(data['token'], data['message_id'], data['react_id'])
    return dumps(ret)

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    data = request.get_json()
    return dumps(message_pinning(data['token'], data['message_id'], True))

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    data = request.get_json()
    return dumps(message_pinning(data['token'], data['message_id'], False))
    
@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater_channel():
    data = request.get_json()
    return dumps(message_sendlater(data['token'], data['channel_id'], data['message'], data['time_sent'], "channel"))

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlater_dm():
    data = request.get_json()
    return dumps(message_sendlater(data['token'], data['dm_id'], data['message'], data['time_sent'], "dm"))

###---------------------------------------------###
###                   Standup                   ###
###---------------------------------------------###

@APP.route("/standup/start/v1", methods=['POST'])
def standup_start():
    data = request.get_json()
    return dumps(standup_start_v1(data['token'], data['channel_id'], data['length']))

@APP.route("/standup/active/v1", methods=['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    
    channel_id = None if channel_id == None else int(channel_id)

    return dumps(standup_active_v1(token, channel_id))

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send():
    data = request.get_json()
    return dumps(standup_send_v1(data['token'], data['channel_id'], data['message']))

###------------------------------------------###
###                   User                   ###
###------------------------------------------###

@APP.route('/user/profile/v2', methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')

    u_id = None if u_id == None else int(u_id)

    return dumps(user_profile_v2(token, u_id))

@APP.route('/user/profile/setname/v2', methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    return dumps(user_profile_setname_v2(data['token'], data['name_first'], data['name_last']))

@APP.route('/user/profile/setemail/v2', methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    return dumps(user_profile_setemail_v2(data['token'], data['email']))

@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def user_profile_setehandle():
    data = request.get_json()
    return dumps(user_profile_sethandle_v1(data['token'], data['handle_str']))
    
@APP.route('/user/profile/uploadphoto/v1', methods=['POST'])
def user_profile_uploadphoto():
    data = request.get_json()
    return dumps(user_profile_uploadphoto_v1(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end']))

@APP.route('/imgurl/<path:path>')
def send_image(path):
    return send_from_directory('', f"imgurl/{path}")

@APP.route('/users/all/v1', methods=['GET'])
def users_all():
    token = request.args.get('token')
    return dumps(users_all_v1(token))

@APP.route('/user/stats/v1', methods=['GET'])
def user_stats():
    token = request.args.get('token')
    return dumps(user_stats_v1(token))

@APP.route('/users/stats/v1', methods=['GET'])
def users_stats():
    token = request.args.get('token')
    return dumps(users_stats_v1(token))

###------------------------------------------###
###                  Other                   ###
###------------------------------------------###

@APP.route('/search/v2', methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')

    return dumps(search_v2(token, query_str))

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    return dumps(clear_v1())


# notifications/get/v1
@APP.route('/notifications/get/v1', methods=['GET'])
def get_notifications():
    data = request.args.get('token')
    # ret = notifications_get_v1(data)
    return dumps(notifications_get_v1(data))

###------------------------------------------###
###              Extra Features              ###
###------------------------------------------###
@APP.route('/channel/rename/v1', methods=['POST'])
def channel_rename():
    data = request.get_json()
    return dumps(group_rename(data['token'], data['name'], data['channel_id'], "channel"))

@APP.route('/dm/rename/v1', methods=['POST'])
def dm_rename():
    data = request.get_json()
    return dumps(group_rename(data['token'], data['name'], data['dm_id'], "dm"))

###------------------------------------------###
###                   Main                   ###
###------------------------------------------###

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port