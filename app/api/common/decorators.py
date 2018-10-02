from functools import wraps

from flask import request, make_response, jsonify

from app.api.v2.models.user import User


def admin_required(f):
    """Checks for valid token for a registered user in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        header_auth = request.headers.get('Authorization', None)
        if not header_auth:
            return make_response(jsonify({
                'error': 'Login or Register to get authorized. If you had logged in, your session expired.'}), 401)
        else:
            token = header_auth.split("Bearer ")
            access_token = token[1]
            access_token = access_token.encode()
            if access_token:
                response = User.decode_token(access_token)
                if isinstance(response, str):
                    user_email = User.fetch_email_by_id(user_id=1)[0]
                    role = User.fetch_role(email=user_email)[0]
                    if role != "admin":
                        return make_response(jsonify({
                            'message': 'Only admins are required to perform this function'}), 401)
            else:
                return make_response(jsonify({'error': 'No access token!'}), 401)
        return f(*args, **kwargs)
    return decorated


def user_required(f):
    """Checks for valid token for a registered user in the header."""
    @wraps(f)
    def decorated(*args, **kwargs):
        header_auth = request.headers.get('Authorization', None)
        if not header_auth:
            return make_response(jsonify({
                'error': 'Login or Register to get authorized. If you had logged in, your session expired.'}), 401)
        else:
            token = header_auth.split("Bearer ")
            access_token = token[1]
            access_token = access_token.encode()
            if access_token:
                response = User.decode_token(access_token)
                if not isinstance(response, str):
                    user_id = response
                else:
                    return make_response(jsonify({'message': response}), 201)
            else:
                return make_response(jsonify({'error': 'No access token!'}), 401)
        return f(*args, **kwargs)
    return decorated
