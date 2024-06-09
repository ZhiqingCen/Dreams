from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'

ACCESS_ERROR = 403
INPUT_ERROR = 400
OK = 200
