from functools import wraps

from flask import request, make_response, jsonify

from app.api.v2.models.blacklist import BlackList
from app.api.v2.models.user import User
import app.api.common.responses as Errors


def user_required(f):
    """Checks for valid token for a registered user in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            if 'Authorization' in request.headers:
                header_auth = request.headers.get('Authorization')
                access_token = header_auth.split(" ")[1]
            if not access_token:
                raise Errors.Unauthorized(
                    "Login to get authorized. If you had logged in, your session expired.")
            response = User.decode_token(access_token)
            user_id = response['user_id']
            print(user_id)
            if isinstance(user_id, str):
                raise Errors.ForbiddenAction("Token has been rejected")
        except Errors.ForbiddenAction as e:
            return e.message
        except Errors.Unauthorized as e:
            return e.message
        return f(user_id=user_id, *args, **kwargs)
    return decorated


def admin_required(f):
    """Checks for valid token for a registered user in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            if 'Authorization' in request.headers:
                header_auth = request.headers.get('Authorization')
                access_token = header_auth.split(" ")[1]
            if not access_token:
                raise Errors.Unauthorized(
                    'Login to get authorized. If you had logged in, your session expired.')
            response = User.decode_token(access_token)
            role = response['role']
            user_id = response['user_id']
            if role == 'user':
                raise Errors.Unauthorized('Only admins are required to perform this function')
            else:
                if isinstance(user_id, str):
                    raise Errors.ForbiddenAction("Token has been rejected")
        except Errors.ForbiddenAction as e:
            return e.message
        except Errors.Unauthorized as e:
            return e.message
        return f(*args, **kwargs, user_id=user_id[0])
    return decorated
