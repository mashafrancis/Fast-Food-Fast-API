from flask import request, Blueprint, jsonify, make_response
from flask.views import MethodView

import app.api.common.responses as UserErrors
from app.api.common.responses import AuthResponse
from app.api.common.utils import Utils
from app.api.v2.models.user import User

auth = Blueprint('auth', __name__)


class RegistrationView(MethodView):
    """This class-based view registers a new user and fetches all user."""

    def post(self):
        """API POST Requests for this view. Url ---> /v2/auth/signup"""
        try:
            if request.content_type == 'application/json':
                data = request.get_json(force=True)
                username = str(data['username'])
                email = str(data['email']).lower()
                password = data['password']
                confirm_password = data['confirm_password']

                User.validate_register_details(email, username, password, confirm_password)
                user = User.fetch_email(email)
                if not user:
                    user = User(username=username, email=email, password=password)
                    user_id = user.save()
                    print(user_id)
                    # generate access_token for user
                    access_token = user.generate_token(user_id)
                    return AuthResponse().create_user(
                        'User {} successfully registered.'.format(user.email), access_token.decode())
                raise UserErrors.Conflict('User already exists! Please login.')
            raise UserErrors.BadRequest('Content-Type must be JSON.')

        except UserErrors.BadRequest as e:
            return e.message
        except UserErrors.Conflict as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)


class LoginView(MethodView):
    """This class-based view handles user login and access token generation"""

    def post(self):
        """API POST Requests for this view. Url ---> /v2/auth/login"""
        try:
            if request.content_type == 'application/json':
                data = request.get_json(force=True)
                password = data['password']
                email = data['email']

                if not email:
                    raise UserErrors.BadRequest('Your email is missing!')
                if not Utils.email_is_valid(email):
                    raise UserErrors.Unauthorized('Your email is invalid! Kindly recheck your email.')

                user = User.fetch_email(email)
                user_id = User.fetch_user_id(user)
                if not user:
                    raise UserErrors.NotFound('User does not exist. Kindly register!')
                else:
                    if email and password:
                        password_hash = User.fetch_password(email)[0]
                        if Utils.check_hashed_password(password, password_hash):
                            access_token = User.generate_token(user_id)
                            if access_token:
                                return AuthResponse.complete_request(
                                    'You have logged in successfully!', access_token.decode())
                        else:
                            raise UserErrors.BadRequest('Wrong Password!')
                    else:
                        if not password:
                            raise UserErrors.BadRequest('Your password is missing!')
            raise UserErrors.BadRequest('Content-Type must be JSON.')

        except UserErrors.BadRequest as e:
            return e.message
        except UserErrors.NotFound as e:
            return e.message
        except UserErrors.Unauthorized as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)


class LogoutView(MethodView):
    """This class based view handles the user logout view"""
    pass


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')

auth.add_url_rule('auth/signup',
                  view_func=registration_view,
                  methods=['POST'])

auth.add_url_rule('auth/login',
                  view_func=login_view,
                  methods=['POST'])

auth.add_url_rule('auth/logout',
                  view_func=login_view,
                  methods=['POST'])
