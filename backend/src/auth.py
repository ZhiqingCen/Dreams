import re
import hashlib
import jwt
import smtplib
import random
from json import dumps, loads
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.error import InputError, AccessError
from src.helper_func import check_valid_user_id, load_database, save_to_database, check_valid_token

session_id = 10000
SECRET = 'COMP1531AERO'

def auth_login_v2(email, password):
    '''
    Given an existing email and matching password the function returns the user's id

    Arguments:
        email(str) - the email of the user
        password(str) - the password of the user

    Exceptions:
        InputError - Occurs when input parameters are not valid credentials

    Return Value:
        return {'auth_user_id': user['u_id']}
        dictionary containing the user's id under the key 'auth_user_id'
    '''

    data = load_database()
    users = data['users']

    # regex check for email validity
    val_email(email)

    email_user = next((user for user in users if user['email'] == email), None)

    if email_user == None:
        raise InputError(description='Email not found')

    check_valid_user_id(email_user['u_id'])
    
    if hashs(password) != email_user['password']:
        raise InputError(description='Incorrect password')

    token = generate_token(email_user['u_id'])
    email_user['token'].append(token)

    save_to_database(data)

    return {'token': token,'auth_user_id': email_user['u_id']} 

def auth_register_v2(email, password, name_first, name_last):
    '''
    Given a new users email, password, first name and last name, if the inputs are valid
    create a new user dictionary containing all of this information along with a unique user
    id and handle. The function then returns the user's id upon the completetion of the other
    functionality

    Arguments:
        email(str) - the email of the user
        password(str) - the password of the user
        name_first(str) - the first name of the user
        name_last(str) - the last name of the user

    Exceptions:
        InputError - Occurs when input parameters are not valid for
        reasons contained in the specifications

    Return Value:
        return {'auth_user_id': user['u_id']}
        dictionary containing the user's id under the key 'auth_user_id'
    '''
    data = load_database()
    users = data["users"]

    new_user = {}

    # Uses a helper function to see if the data meets the requirements for a valid user
    if not val_user(email, password, name_first, name_last):
        raise InputError(description='Issue with provided credentials')
    
    # Checks if the email is already stored in the data of another user
    # if the email is already in use provide an InputError
    if email_in_use(email):
        raise InputError('Email already in use')

    new_user['email'] = email
    new_user['password'] = hashs(password)
    new_user['name_first'] = name_first
    new_user['name_last'] = name_last

    # Converts the inputs to lowercase to create the handle
    name_first = name_first.lower()
    name_last = name_last.lower()
    handle = name_first + name_last

    # Truncates the handle to 20 characters
    if len(handle) > 20:   
        handle = handle[:20]

    # Check there are no white spaces or @ symbols, if there are remove them
    i = 0
    while i < len(handle):
        if handle[i] == "@" or handle[i] == " ":
            handle = handle[: i] + handle[i + 1:]
            i = i - 1       
        i += 1
    
    # Checks that this handle does not appear in the user data under another user
    # if so add a number (starting at 0) and check again
    num = 0
    for user in users:
        if user['handle_str'] == handle:
            if handle[-1].isdigit():
                handle = handle[:-1]
            handle += str(num)
            num += 1

    new_user['handle_str'] = handle

    # Checks that this user_id does not appear in the user data under another user
    # if it does add 1 and check again
    u_id = 0
    for user in users:
        if user['u_id'] == u_id:
            u_id += 1

    new_user['u_id'] = u_id
    
    # If a user is the first user to register they obtain the global owner flag
    if new_user['u_id'] == 0:
        new_user['global_owner'] = True
    else:
        new_user['global_owner'] = False

    # Generate a new token for the registered user and adds it to a list of currently valid tokens
    token = generate_token(u_id)
    new_user['token'] = []
    new_user['token'].append(token)

    # Add default profile picture
    new_user['profile_img_url'] = 'imgurl/default.jpg'

    # Append this user to the list of users in the data file
    users.append(new_user)
    
    # Save changes to data.json file
    save_to_database(data)

    return {'token': token,'auth_user_id': u_id}

def auth_logout_v1(token):
    data = load_database()
    users = data["users"]

    user = [user for user in users if token in user['token']]

    if not user:
        return {'is_success': False}

    user = user[0]

    if f"{user['name_first'] + user['name_last']}" == "Removed user":
        raise AccessError(description = 'A removed user cannot log out')
    
    user['token'] = []
    
    save_to_database(data)

    return {'is_success': True}

def auth_passwordreset_request_v1(email):
    data = load_database()
    users = data["users"]

    if not email_in_use(email):
        raise InputError('Email already in use')
    
    reset_code = random.randint(10000,99999)
    for user in users:
        if user['email'] == email:
            user['reset_code'] = reset_code

    save_to_database(data)

    sender = 'UNSWDREAMS@gmail.com'
    receiver = email

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = ('Reset Code')
    message = MIMEText(f'Your password reset code is {reset_code}')
    msg.attach(message)

    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(sender, 'AEROCOMP1531')
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()

    return{}

def auth_passwordreset_reset_v1(reset_code, new_password):
    data = load_database()
    users = data["users"]

    if len(new_password) < 6:
        raise InputError('New password is too short')
    for user in users:
        if user['reset_code'] == reset_code:
            user['password'] = hashs(new_password)
            user.pop('reset_code')
            save_to_database(data)
            return {}
    raise InputError('Invalid reset code')

#------------------------------------#
#          Helper Functions          #
#------------------------------------#

def new_session():
    global session_id
    session_id += 1
    return session_id

def hashs(password):
    '''
    Given a password return a hashed version of it using SHA256

    Arguments:
        password(str) - the password of the user

    Return Value:
        return hashlib.sha256(string.encode()).hexdigest()
        hashed version of the given password
    '''
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(u_id):
    session_id = new_session()
    # not functioning method to generate a JWT token
    return jwt.encode({'u_id': u_id, 'session_id': session_id}, SECRET, algorithm='HS256')

def email_in_use(email):
    data = load_database()
    users = data['users']

    for user in users:
        if user['email'] == email:
            return True
    return False

def val_user(email, password, name_first, name_last):
    '''
    Given a set of user credentials determine whether they meet the basic requirements

    Arguments:
        email(str) - the email of the user
        password(str) - the password of the user
        name_first(str) - the first name of the user
        name_last(str) - the last name of the user

    Exceptions:
        InputError - Occurs when input parameters are not valid for
        reasons contained in the specifications

    Return Value:
        return True
        returns boolean True if the set of input credentials meet the requirements
    '''
    # regex check for email validity
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'

    if name_first == 'Removed' and name_last == 'user':
        raise InputError(description='Invalid first or last name, cannot use the name Removed User')
    if not re.search(regex, email):
        raise InputError(description='Invalid email')
    if len(password) < 6: # check that the password is at least 6 characters
        raise InputError(description='Password is too short')
    if len(name_first) < 1: # check if name_first is less than 1
        raise InputError(description='Please enter a first name')
    if len(name_first) > 50: # check if name_first is more than 50 characters
        raise InputError(description='First name is too long')
    if len(name_last) < 1: # check if name_first is less than 1
        raise InputError(description='Please enter a last name')
    if len(name_last) > 50: # check if name_first is more than 50 characters
        raise InputError(description='Last name is too long')

    return True

def val_email(email):
    regex = '^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
    if not re.search(regex, email):
        raise InputError(description='Invalid email')
    return True