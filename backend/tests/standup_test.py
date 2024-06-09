from src.helper_func import extract_current_time
from src.other import clear_v1
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.common import extract_messages_from_group, invite_to_group
from src.error import AccessError, InputError
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
import pytest
import threading

###-------------###
### Test Set Up ###
###-------------###

ONE_SECOND = 1 #seconds
NOT_AN_INT = 1.5 #seconds
VALID_MESSAGE = "AERO: Message"
LONGEST_VALID_MESSAGE = 'a' * 1000
MESSAGE_TOO_LONG = 'a' * 1001

@pytest.fixture
def register_users():
    clear_v1()
    user_global_owner = auth_register_v2("address0@email.com", "onetwothree", "User0", "GlobalOwner")
    user_owner = auth_register_v2("address1@email.com", "onetwothree", "User1", "Owner")
    user_member = auth_register_v2("address2@email.com", "onetwothree", "User2", "Member")
    user_not_member = auth_register_v2("address3@email.com", "onetwothree", "User3", "NotMember1")
    unregistered_user = {'token': 5, 'auth_user_id': 5}

    return user_global_owner, user_owner, user_member, user_not_member, unregistered_user

@pytest.fixture
def create_channel(register_users):
    user_global_owner,user_owner,user_member,_,_ = register_users
    channel = channels_create_v2(user_owner['token'], "Channel", True)

    invite_to_group(user_owner['token'], channel['channel_id'], user_global_owner['auth_user_id'], 'channel')

    invite_to_group(user_owner['token'], channel['channel_id'], user_member['auth_user_id'], 'channel')

    nonexistent_channel = {'channel_id': 2}
    
    return channel, nonexistent_channel

def join_active_threads():
    for thread in threading.enumerate():
        if thread.name != 'MainThread':
            thread.join()

###--------------------------------------------------------------------------------------------------------------###
###                                         standup_start Function Tests                                         ###
###--------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

# token invalid
def test_standup_start_invalid_token(register_users, create_channel):
    _,_,_,_,unregistered_user = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_start_v1(unregistered_user['token'], channel['channel_id'], ONE_SECOND)

# token not in channel
def test_standup_start_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_start_v1(not_member['token'], channel['channel_id'], ONE_SECOND)

# invalid channel_id
def test_standup_start_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel

    with pytest.raises(InputError):
        standup_start_v1(member['token'], nonexistent_channel['channel_id'], ONE_SECOND)

# invalid length
def test_standup_start_invalid_length(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    with pytest.raises(InputError):
        standup_start_v1(member['token'], channel['channel_id'], NOT_AN_INT)

# standup already active in channel
def test_standup_start_startup_already_active(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    standup_start_v1(member['token'], channel['channel_id'], ONE_SECOND,)

    with pytest.raises(InputError):
        standup_start_v1(member['token'], channel['channel_id'], ONE_SECOND)

    join_active_threads()

# none input
def test_standup_start_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_start_v1(None, None, None)
    with pytest.raises(AccessError):
        standup_start_v1(None, channel['channel_id'], ONE_SECOND)
    with pytest.raises(InputError):
        standup_start_v1(member['token'], None, ONE_SECOND)
    with pytest.raises(InputError):
        standup_start_v1(member['token'], channel['channel_id'], None)

###------------------------###
### Output/Action Checking ###
###------------------------###

# check time - channel owner starts
def test_standup_start_owner_begins(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(owner['token'], channel['channel_id'], ONE_SECOND)
    time_start = extract_current_time()

    #check that the standup is active
    channel_activity = standup_active_v1(owner['token'], channel['channel_id'])
    assert channel_activity['is_active'] == True
    
    #check that finish matches expected finish ??
    assert ret['time_finish'] >= time_start
    assert ret['time_finish'] <= time_start + 2

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(owner['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False
    
# check time - channel global-owner starts
def test_standup_start_global_owner_begins(register_users, create_channel):
    global_owner,_,_,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(global_owner['token'], channel['channel_id'], ONE_SECOND)
    time_start = extract_current_time()
    
    #check that the standup is active
    channel_activity = standup_active_v1(global_owner['token'], channel['channel_id'])
    assert channel_activity['is_active'] == True
    
    #check that finish matches expected finish
    assert ret['time_finish'] >= time_start
    assert ret['time_finish'] <= time_start + 2

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(global_owner['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == global_owner['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False

# check time - channel member starts
def test_standup_start_member_begins(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(member['token'], channel['channel_id'], ONE_SECOND)
    time_start = extract_current_time()

    #check that the standup is active
    channel_activity = standup_active_v1(member['token'], channel['channel_id'])
    assert channel_activity['is_active'] == True
    
    #check that finish matches expected finish
    assert ret['time_finish'] >= time_start
    assert ret['time_finish'] <= time_start + 2

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(member['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == member['auth_user_id']
    assert most_recent_message['message'] == '[No messages were sent during this standup]'
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False
    
###--------------------------------------------------------------------------------------------------------------###
###                                         standup_active Function Tests                                        ###
###--------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

# not a valid token
def test_standup_active_invalid_token(register_users, create_channel):
    _,_,_,_,unregistered_user = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_active_v1(unregistered_user['token'], channel['channel_id'])

# token not in channel
def test_standup_active_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_active_v1(not_member['token'], channel['channel_id'])

# invalid channel_id
def test_standup_active_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel

    with pytest.raises(InputError):
        standup_active_v1(member['token'], nonexistent_channel['channel_id'])

# none input
def test_standup_active_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_active_v1(None, None)
    with pytest.raises(AccessError):
        standup_active_v1(None, channel['channel_id'])
    with pytest.raises(InputError):
        standup_active_v1(member['token'], None)

###------------------------###
### Output/Action Checking ###
###------------------------###

# check when standup is active
def test_standup_active_is_active(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(owner['token'], channel['channel_id'], ONE_SECOND)
    
    #check that the standup is active
    channel_activity = standup_active_v1(owner['token'], channel['channel_id'])
    assert channel_activity['is_active'] == True
    
    #check that finish matches expected finish
    assert channel_activity['time_finish'] == ret['time_finish']

    join_active_threads()

# check when standup is not active
def test_standup_active_not_active(register_users, create_channel):
    _,owner,_,_,_ = register_users
    channel, _ = create_channel

    #check that the standup is active
    channel_activity = standup_active_v1(owner['token'], channel['channel_id'])
    assert channel_activity['is_active'] == False
    
    #check that finish matches expected finish
    assert channel_activity['time_finish'] == None

###--------------------------------------------------------------------------------------------------------------###
###                                         standup_send Function Tests                                          ###
###--------------------------------------------------------------------------------------------------------------###

###----------------###
### Error Checking ###
###----------------###

# not a valid token
def test_standup_send_invalid_token(register_users, create_channel):
    _,_,_,_,unregistered_user = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_send_v1(unregistered_user['token'], channel['channel_id'], VALID_MESSAGE)

# token not in channel
def test_standup_send_token_not_member(register_users, create_channel):
    _,_,_,not_member,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_send_v1(not_member['token'], channel['channel_id'], VALID_MESSAGE)

# invalid channel_id
def test_standup_send_invalid_channel_id(register_users, create_channel):
    _,_,member,_,_ = register_users
    _, nonexistent_channel = create_channel

    with pytest.raises(InputError):
        standup_send_v1(member['token'], nonexistent_channel['channel_id'], VALID_MESSAGE)

# standup is not currently active in channel
def test_standup_send_startup_not_active(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    with pytest.raises(InputError):
        standup_send_v1(member['token'], channel['channel_id'], VALID_MESSAGE)

# when message is more than 1000 characters (not including the username and colon)
def test_standup_send_group_message_too_long(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    standup_start_v1(member['token'], channel['channel_id'], ONE_SECOND,)

    with pytest.raises(InputError):
        standup_send_v1(member['token'], channel['channel_id'], MESSAGE_TOO_LONG)
    
    join_active_threads()

# none input
def test_standup_send_none_input(register_users, create_channel):
    _,_,member,_,_ = register_users
    channel, _ = create_channel

    with pytest.raises(AccessError):
        standup_send_v1(None, None, None)
    with pytest.raises(AccessError):
        standup_send_v1(None, channel['channel_id'], VALID_MESSAGE)
    with pytest.raises(InputError):
        standup_send_v1(member['token'], None, VALID_MESSAGE)
    with pytest.raises(InputError):
        standup_send_v1(member['token'], channel['channel_id'], None)

###------------------------###
### Output/Action Checking ###
###------------------------###

def test_standup_send_one_message(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(owner['token'], channel['channel_id'], ONE_SECOND,)

    standup_send_v1(member['token'], channel['channel_id'], "Hello!")

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(owner['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: Hello!'
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False

# test message size limits
def test_standup_send_message_upper_limit(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(owner['token'], channel['channel_id'], ONE_SECOND,)

    standup_send_v1(member['token'], channel['channel_id'], LONGEST_VALID_MESSAGE,)

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(owner['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: ' + LONGEST_VALID_MESSAGE
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False

# test sending multiple messages to the queue
def test_standup_send_multiple_messages(register_users, create_channel):
    _,owner,member,_,_ = register_users
    channel, _ = create_channel

    ret = standup_start_v1(owner['token'], channel['channel_id'], ONE_SECOND,)

    standup_send_v1(member['token'], channel['channel_id'], "Hello!")

    standup_send_v1(owner['token'], channel['channel_id'], "Hey there")

    join_active_threads()

    # get channel messages
    most_recent_message = extract_messages_from_group(owner['token'], channel['channel_id'], 0, 'channel')['messages'][0]

    # assert that the message is correct
    assert most_recent_message['u_id'] == owner['auth_user_id']
    assert most_recent_message['message'] == 'user2member: Hello!\nuser1owner: Hey there'
    assert most_recent_message['time_created'] == ret['time_finish']
    assert most_recent_message['is_pinned'] == False
    