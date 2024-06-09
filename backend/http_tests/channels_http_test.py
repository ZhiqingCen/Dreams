import requests
import json
from src import config
from src.error import ACCESS_ERROR, INPUT_ERROR, OK

one = {
    'email': 'address@email1.com',
    'password': 'UserOne111',
    'name_first': 'User',
    'name_last': 'One',
}
two = {
    'email': 'address@email2.com',
    'password': 'UserTwo222',
    'name_first': 'User',
    'name_last': 'Two',
}

three = {
    'email': 'address@email3.com',
    'password': 'UserThree333',
    'name_first': 'User',
    'name_last': 'Three',
}

###------------------------------------------------###
### channels_listall_v2(token) return { channels } ###
###------------------------------------------------###

### ----input checking---- ###
# invalid parameter empty string input auth_user_id for function channels_listall_v1
def test_channels_listall_empty_token():
    requests.delete(config.url + 'clear/v1')
    resp = requests.get(config.url + 'channels/listall/v2', params = {'token': ''})
    assert resp.status_code == ACCESS_ERROR


# invalid parameter string input auth_user_id for function channels_listall_v1
def test_channels_listall_invalid_token_type():
    requests.delete(config.url + 'clear/v1')
    resp = requests.get(config.url + 'channels/listall/v2', params={'token': 123456789})
    assert resp.status_code == ACCESS_ERROR

# input of none existing auth_user_id for function channels_listall_v1
def test_channels_listall_token_not_exist():
    requests.delete(config.url + 'clear/v1')
    resp = requests.get(config.url + 'channels/listall/v2', params={'token': 'an_invalid_token'})
    assert resp.status_code == ACCESS_ERROR

### ----output checking---- ###
def test_channels_listall_return():
    '''
    Check the channels/listall/v2 output structure and contents.
    '''
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(config.url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    user3 = requests.post(config.url + 'auth/register/v2', json = three)
    user_three = json.loads(user3.text)
    
    requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json = {'token': user_two['token'], 'name': 'channelTWO', 'is_public': False})
    requests.post(config.url + 'channels/create/v2', json = {'token': user_three['token'], 'name': 'channelTHREE', 'is_public': True})
    
    resp = requests.get(config.url + 'channels/listall/v2', params = {'token': user_one['token']})
    all_channels = resp.json()['channels']
    
    # Check output keywords and types are correct
    assert all(isinstance(channel['channel_id'], int) for channel in all_channels)
    assert all(isinstance(channel['name'], str) for channel in all_channels)
    
    # Check channel names are listed
    assert 'channelONE' and 'channelTWO' and 'channelTHREE' in [channel['name'] for channel in all_channels]

# check when there is no channels, channels_listall return channels as empty list
def test_channels_listall_empty():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.get(config.url + 'channels/listall/v2', params = {'token': user_one['token']})
    assert json.loads(resp.text) == {'channels': []}


def test_channels_listall_user_not_in_channels():
    '''
    Check when there are channels, but auth_user_id not in all channels, 
    channels/listall/v2 should still return all channels.
    '''
    requests.delete(config.url + 'clear/v1')
    
    # Register users
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    user2 = requests.post(config.url + 'auth/register/v2', json = two)
    user_two = json.loads(user2.text)
    
    # Create channels 
    requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'channelONE', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json = {'token': user_two['token'], 'name': 'channelTWO', 'is_public': False})
    
    
    # Check all channels are listed, including channels the user is not a member of.
    resp = requests.get(config.url + 'channels/listall/v2', params = {'token': user_one['token']}) 
    all_channels = resp.json()['channels']
    assert 'channelONE' in [channel['name'] for channel in all_channels]
    assert 'channelTWO' in [channel['name'] for channel in all_channels]

###------------------------------------------------------------------###
### channels_create_v2(token, name, is_public) return { channel_id } ###
###------------------------------------------------------------------###

### ----input checking---- ###
# invalid parameter input auth_user_id for function channels_create_v1
def test_channels_create_empty_token():
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': '', 'name': 'name', 'is_public': True,})
    assert resp.status_code == ACCESS_ERROR

def test_channels_create_invalid_token_type():
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': 123456789, 'name': 'name', 'is_public': True,})
    assert resp.status_code == ACCESS_ERROR

# invalid parameter input auth_user_id with not existing id for function channels_create_v1
def test_channels_create_token_not_exist():
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': 'an_invalid_token', 'name': 'name', 'is_public': True,})
    assert resp.status_code == ACCESS_ERROR
    
# invalid parameter empty string input name for function channels_create_v1
def test_channels_create_empty_name():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': '', 'is_public': True,})
    assert resp.status_code == INPUT_ERROR

def test_channels_create_exceed_length_limit_name():
    '''
    Check that a channel can be created with a name of 20 characters, but no more.
    '''
    MAX_NAME_LEN = 20
    
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    
    # Create a channel with a name of 20 characters and check the action succeeds 
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'a' * MAX_NAME_LEN, 'is_public': True,})
    assert resp.status_code == OK
    
    # Check that a channel with name > 20 characters returns an input error
    resp = requests.post(config.url + 'channels/create/v2', json = {'token': user_one['token'], 'name': 'a' * (MAX_NAME_LEN + 1), 'is_public': True,})
    assert resp.status_code == INPUT_ERROR


### ----output checking---- ###
def test_channels_create_return():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_one['token'],
        'name': 'channelONE',
        'is_public': True,})
    
    # Check that the channel was successfully added and that it returns a 
    # dictionary with the keyword 'channel_id' to store an integer.
    assert resp.status_code == OK
    assert isinstance(resp.json()['channel_id'], int)

def test_channels_create_functionality():
    '''
    Test that a channel is successfully added to the database by attempting to 
    send message to the added channel with the channel_id
    '''   
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = one)
    user_one = json.loads(user1.text)
    resp = requests.post(config.url + 'channels/create/v2', json = {
        'token': user_one['token'],
        'name': 'channelONE',
        'is_public': True,})
    channel1 = resp.json()
    
    # Assert channel_id is valid by checking the new channel can have a message sent to it
    resp = requests.post(config.url + 'message/send/v2', json = {
        'token': user_one['token'],
        'channel_id': channel1['channel_id'],
        'message': 'message'
    })
    assert resp.status_code == OK