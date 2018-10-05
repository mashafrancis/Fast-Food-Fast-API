from flask import Blueprint, request
from flask.views import MethodView

from app.api.common.decorators import user_required, admin_required
from app.api.common.responses import Response
from app.api.v2.models.meal import Meal
from app.api.v2.models.order import Orders
from app.api.v2.models.user import User

import app.api.common.responses as Error

user = Blueprint('user', __name__)


class UsersView(MethodView):
    """This class-based view handles user login and access token generation"""

    @admin_required
    def get(self, user_id):
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
            _user = User.fetch_username_by_id(user_id)
            if _user:
                return Response.complete_request("Username of ID {} is {}".format(user_id, _user[0]))
            raise Error.NotFound("Sorry, User ID No {} does't exist!".format(user_id))
        except Error.NotFound as e:
            return e.message


class UserOrdersView(MethodView):
    """Contains GET and POST methods"""

    @user_required
    def get(self, user_id):
        """Endpoint for fetching all the users."""
        results = []
        all_orders = Orders.list_all_orders()
        try:
            if all_orders:
                for order in all_orders:
                    obj = Response.define_orders(order)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise Error.NotFound('You have not ordered any meal for a while. Place an order now?')
        except Error.NotFound as e:
            return e.message

    @user_required
    def post(self, user_id):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        meal_id = data['meal_id']
        quantity = data['quantity']

        meal = Meal.find_by_id(meal_id)
        ordered_meal = Orders.find_meal_by_its_id(meal_id)
        try:
            if not meal:
                raise Error.NotFound('Meal not available')
            elif ordered_meal:
                raise Error.Conflict('Meal already exists. Do you want to update the meal item quantity?')
            else:
                name = meal[2]
                price = meal[4]
                if ordered_meal is True:
                    Orders.find_orders_by_user_id(user_id)

            order = Orders(user_id=user_id[0],
                           name=name,
                           quantity=quantity,
                           price=price)

            order.save()
            return Response.create_resource('Order has been placed successfully.')
        except Error.Conflict as e:
            return e.message
        except Error.NotFound as e:
            return e.message

    @user_required
    def delete(self, user_id):
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
user_order_view = UserOrdersView.as_view('user_orders_view')

user.add_url_rule('users',
                  view_func=users_view,
                  methods=['GET'])

user.add_url_rule('users/<int:user_id>',
                  view_func=user_view,
                  methods=['GET'])

user.add_url_rule('users/orders',
                  view_func=user_order_view,
                  methods=['GET', 'POST', 'DELETE'])
