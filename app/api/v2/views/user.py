from flask import Blueprint, request
from flask.views import MethodView

from app.api.common.decorators import user_required, admin_required
from app.api.common.responses import Response
from app.api.v2.models.order import Orders
from app.api.v2.models.user import User

import app.api.common.responses as Error

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
                raise Error.NotFound('No users to display!')
        except Error.NotFound as e:
            return e.message


class UserView(MethodView):

    def get(self, user_id):
        """Endpoint for fetching a particular order."""
        try:
            _user = User.find_by_id(user_id)
            if _user:
                return Response.complete_request(_user)
            raise Error.NotFound("Sorry, User ID No {} does't exist!".format(user_id))
        except Error.NotFound as e:
            return e.message


class UserOrdersView(MethodView):
    """Contains GET and POST methods"""

    @admin_required
    def get(self):
        """Endpoint for fetching all orders."""
        results = []
        all_orders = Orders.list_all_orders()
        try:
            if all_orders:
                for order in all_orders:
                    obj = Response.define_orders(order)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise Error.NotFound('Sorry, No customer has placed an order today!')
        except Error.NotFound as e:
            return e.message

    @user_required
    def post(self):
        """Endpoint for placing a new order."""
        data = request.get_json(force=True)
        name = data['name']
        quantity = data['quantity']
        price = data['price']

        order = Orders(name=name,
                       quantity=quantity,
                       price=price)
        order.save()
        return Response.create_resource('Order has been placed successfully.')

    @admin_required
    def delete(self):
        """Endpoint for deleting all orders."""
        try:
            if not Orders.find_one_entry():
                raise Error.NotFound('No orders available!')
            else:
                Orders.delete_all()
                return Response.complete_request('All orders have been successfully deleted!')
        except Error.NotFound as e:
            return e.message


users_view = UsersView.as_view('users_view')
user_view = UserView.as_view('user_view')

user.add_url_rule('users',
                  view_func=users_view,
                  methods=['GET'])

user.add_url_rule('users/<int:user_id>',
                  view_func=user_view,
                  methods=['GET'])
