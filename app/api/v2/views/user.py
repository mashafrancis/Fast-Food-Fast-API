from flask import Blueprint
from flask.views import MethodView

from app.api.common.decorators import user_required, admin_required
from app.api.common.responses import Response
from app.api.v2.models.user import User

import app.api.common.responses as UserErrors

user = Blueprint('user', __name__)


class UsersView(MethodView):
    """This class-based view handles user login and access token generation"""

    @admin_required
    def get(self):
        """API GET Requests for this view. Url ---> /v1/auth/users"""
        try:
            results = []
            users = User.list_all_users()
            if users:
                for users in users:
                    obj = Response.define_users(users)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise UserErrors.NotFound('No users to display!')
        except UserErrors.NotFound as e:
            return e.message


class UserView(MethodView):

    def get(self, user_id):
        """Endpoint for fetching a particular order."""
        try:
            _user = User.find_by_id(user_id)
            if _user:
                return Response.complete_request(_user)
            raise UserErrors.NotFound("Sorry, User ID No {} does't exist!".format(user_id))
        except UserErrors.NotFound as e:
            return e.message


users_view = UsersView.as_view('users_view')
user_view = UserView.as_view('user_view')

user.add_url_rule('users',
                  view_func=users_view,
                  methods=['GET'])

user.add_url_rule('users/<int:user_id>',
                  view_func=user_view,
                  methods=['GET'])
