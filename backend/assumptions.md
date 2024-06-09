# Assumptions

## 1. auth.py

### 1.1 auth_login
* Assumes existing emails and passwords can be extracted from users list of dictionaries with the keys 'email' and 'password' respectively.

### 1.2 auth_register
* Assumes that the user's first and last name are to be stored as inputted (rather than in lowercase or using .capitalise)
* Assumes that user_id's of varying integer lengths are valid (e.g. 1, 23, 344 are all different lengths)
* Assumes that u_id/auth_user_id can begin at index 0 and sequentially increase and that the u_id/auth_user_id does not need to be randomly generated or of a specific length
* Assume if a whitespace or '@' symbol are present in a users name_first or name_last string that these symbols will be removed from the handle string (as opposed to being replaced by another permitted character)

### 1.3 auth_passwordreset_request
* InputError when the email is not in use
* The generated reset_code is a random 5 digit number (e.g. 21319)
* The emails come from our own email address UNSWDREAMS@gmail.com
* The email is basic and simply contains the line ‘Your password reset code is ‘reset_code’

### 1.4 auth_passwordreset_reset
* A user can only have one active reset code
* Reset codes do not expire
* Old reset codes are removed after use

## 2. channel.py

### 2.1 channel_invite
* It is an InputError if the user being invited is already in the channel
* Assumes u_id/auth_user_id begins at index 0 and sequentially increases
* Assumes channel_id begins at index 0 and sequentially increases
* Assumes auth_register logs in by default
* Assumes all members of a channel can invite users to a channel, not just the owner
* Assumes it is an InputError if there is 'None' input for a parameter


### 2.2 channel_details
* Assumes u_id/auth_user_id begins at index 0 and sequentially increases
* Assumes channel_id begins at index 1 and sequentially increases
* Assumes auth_register logs in by default
* Assumes it is an InputError if there is 'None' input for a parameter
* Assumes all members of a channel can view the details of the channel, not just the owner
* Assumes owner members are part of channels['all_members']
* There has to be at least one owner (and hence one member) of a channel.


### 2.3 channel_messages
* Assumes it will be able to access the lists users, channels and messages from data.py
* Assumes users will contain a 'u_id' key
* Assumes channels will contain  'channel_id' and 'channel_member_ids' keys:
* Assumes messages will contain these keys 'channel_id', 'message_id', 'u_id', 'message' and 'time_created'

### 2.4 channel_join
* channel_id is always a positive number
* channel_id is unique for all users

### 2.5 channel_addowner
* global owners cannot add a user if they are not in the channel
* if a user is not in the channel, they are automatically added

### 2.6 channel_removeowner
* global owners cannot remove a user if they are not in the channel

### 2.7 channel_leave
* AccessError when token is not a valid user

## 3. channels.py

### 3.1 channels_list
* Program quit with error message when none or wrong number of parameters pass in
* All users will be added to channels['channel_member_id'] even if they are channels owner
* auth_register logs in by default
* When auth_user_id does not belong to a member in any channels, no error will raise, return {'channels': []} instead


### 3.2 channels_listall
* Program quit with error message when no or wrong number of parameters pass in
* All users will be added to channels['channel_member_id'] even if they are channels owner
* auth_register logs in by default
* When there is no channels, no error will raise, return {'channels': []} instead


### 3.3 channels_create
* Program quit with error message when no or wrong number of parameters pass in
* Add all users to as channels_member even if they are channels owner
* auth_user_id passed in as parameter will automatically be the owner of channel
* auth_register logs in by default
* Different channels can have the same name and is_public setting
* channel_id generate by increment from the number of existing channels, start from 1 and increment by 1 each time


## 4. admin.py

### 4.1 admin_user_remove
* it is valid for an owner to remove themselves
* it is valid to remove a channel owner as the global owner is an owner of all channels
* it is an imput error if u_id has already been removed
* it is an access error if token has already been removed
* Removed Users is a reserved name for the system - no user can register with any variation of "Removed user"

### 4.2 admin_userpermissions_change
* does nothing if permissions are already set to whatever they are desiring to change it to
* it is valid to change your own permissions
* nothing happens when you try to change the user's permissions to they permissions they already have
* input error if trying to change permissions to member of the only owner

## 5. dm.py

### 5.1 dm_details
* Assumes u_id/auth_user_id begins at index 0 and sequentially increases
* Assumes dm_id begins at index 0 and sequentially increases
* Assumes auth_register logs in by default
* Assumes it is an InputError if there is 'None' input for a parameter
* Assumes all members of a dm can view the details of the dm, not just the owner
* Assumes owner members are part of channels['all_members']
* There has to be at least one owner (and hence one member) of a dm.
* list all members (including person who called the function and owner)

### 5.2 dm_create
* can create a dm where you are the only member
* can create multiple chats with same people
* owner is included in members

### 5.2 dm_list
* Program quit with error message when none or wrong number of parameters pass in
* All users will be added to dms['dm_member_id'] even if they are dms owner
* auth_register logs in by default
* When auth_user_id does not belong to a member in any dms, no error will raise, return {'dms': []} instead

### 5.3 dm_create
* can create a dm where you are the only member
* can create multiple chats with same people
* owner is included in members

### 5.4 dm_invite
* It is an InputError if the user being invited is already in the channel
* Assumes u_id/auth_user_id begins at index 0 and sequentially increases
* Assumes dm_id begins at index 0 and sequentially increases
* Assumes auth_register logs in by default
* Assumes all members of a dm can invite users to a dm, not just the owner
* Assumes it is an InputError if there is 'None' input for a parameter

### 5.5 dm_leave
* AccessError when token is not a valid user

### 5.6 dm_messages
* Assumes it will be able to access the lists users, dms and messages from data.py
* Assumes users will contain a 'u_id' key
* Assumes dms will contain  'dm_id' and 'dm_member_ids' keys:
* Assumes messages will contain these keys 'dm_id', 'message_id', 'u_id', 'message' and 'time_created'


## 6. message.py

### 6.1 message_send
* Program quit with error message when no or wrong number of parameters pass in
* message cannot be empty
* Access error is given if invalid dm id is given

### 6.2 message_edit
* Program quit with error message when no or wrong number of parameters pass in
* channel_id stored in messages is always valid
* dm_id stored in messages is always valid

### 6.3 message_remove
* Program quit with error message when no or wrong number of parameters pass in
* channel_id stored in messages is always valid
* dm_id stored in messages is always valid

### 6.4 message_share
* Program quit with error message when no or wrong number of parameters pass in
* shared_message cannot exceed 1000 characters
    * in total, shared_message + original message cannot exceed 2000 characters

### 6.5 message_senddm
* Access error is given if invalid dm id is given

### 6.6 message_react
* Program quit with error message when no or wrong number of parameters pass in
* user can react to their own message

### 6.7 message_unreact
* Program quit with error message when no or wrong number of parameters pass in
* user can unreact to their own message

### 6.8 message_sendlater
* input error is given if invalid dm id is given

### 6.9 message_sendlaterdm
* input error is given if invalid dm id is given

## 7. notifications.py

### 7.1 notificaitons_get
* Program quit with error message when no or wrong number of parameters pass in
* users cannot tag themselves
* user will receive notification for repeated actions
    * for example, when user react to a message, he/she receive one notification, when user unreact the same message and then react again, he/she will receive a new notification

## 8. user.py

### 8.1 user_profile
* If the user calling the function’ token is invalid than it returns an Access Error

### 8.2 user_profile_setname
* If the user calling the function’ token is invalid than it returns an Access Error

### 8.3 user_profile_setemail
* If the user calling the function’ token is invalid than it returns an Access Error

### 8.4 user_profile_sethandle
* If the user calling the function’ token is invalid than it returns an Access Error

### 8.5 users_all
* If the user calling the function’ token is invalid than it returns an Access Error
* Any user can call this function.
* Returns u_id, email, first name, last name and handle but no passwords or tokens since any user can call this function.

### 8.6 user_stats
* Program quit with error message when no or wrong number of parameters pass in
* time_stamp refers to the time when function is called

### 8.7 users_stats
* Program quit with error message when no or wrong number of parameters pass in
* time_stamp refers to the time when function is called

### 8.8 user_profile_uploadphoto
* Access Error when the token is not a valid user
* The image is given a randomly generated 6 digit number as a file name (e.g. 929123.jpg) when uploaded
* The function only saves the image and creates a file in src/imgurl
* Another route is made in server.py to access the files using the image urls
* If the photo source URL is invalid an error is provided by the requests library 

## 9. standup.py

### 9.1 standup_start
* Access Error when the token is not a valid user
* Input Error when length is not an integer
* Assumed that the function shouldn’t wait for the thread to join before returning

### 9.2 standup_active
* Access Error when the token is not a valid user
* Access Error when the token is not a member of the channel

### 9.3 standup_send
* AccessError when the token is not a valid user
* Still sends a summary message at the end of every startup
* If no messages were sent during the startup, fills the message content with '[No messages were sent during this standup]'

## 10. extra_features.py

### 10.1 channel_rename
* only channel owner can rename a channel, otherwise raise AccessError
* channel name cannot exceed 20 characters

### 10.2 dm_rename
* only dm owner can rename a channel, otherwise raise AccessError
* dm name cannot exceed 20 characters
