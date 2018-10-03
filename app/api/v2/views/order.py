from flask import request, jsonify, Blueprint
from flask.views import MethodView

import app.api.common.responses as OrderError
from app.api.common.decorators import user_required, admin_required
from app.api.v2.models.meal import Meal

from app.api.v2.models.order import Orders
from app.api.common.responses import Response
from app.api.v2.models.user import User

orders = Blueprint('order', __name__)


class OrdersView(MethodView):
    """Contains GET and POST methods"""

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
                raise OrderError.NotFound('Sorry, No customer has placed an order today!')
        except OrderError.NotFound as e:
            return e.message

    # @user_required
    # def post(self, user_id):
    #     """Endpoint for adding a new order."""
    #     data = request.get_json(force=True)
    #     meal_id = data['meal_id']
    #     # name = data['name']
    #     quantity = data['quantity']
    #     # price = data['price']
    #
    #     meal = Meal.find_by_id(meal_id)
    #     if not meal:
    #         return OrderError.NotFound('Meal not available')
    #     else:
    #         name = meal[2]
    #         price = meal[4]
    #
    #     order = Orders(user_id=user_id[0],
    #                    name=name,
    #                    quantity=quantity,
    #                    price=price)
    #     order.save()
    #     return Response.create_resource('Order has been placed successfully.')

    @admin_required
    def delete(self, user_id):
        """Endpoint for deleting all orders."""
        try:
            if not Orders.find_one_entry():
                raise OrderError.NotFound('No orders available!')
            else:
                Orders.delete_all()
                return Response.complete_request('All orders have been successfully deleted!')
        except OrderError.NotFound as e:
            return e.message


class OrderView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""

    @user_required
    def get(self, order_id, user_id):
        """Endpoint for fetching a particular order."""
        try:
            all_meals = []
            order = Orders.find_by_id(order_id)
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} does't exist!".format(order_id))
            user_id = user_id[0]
            username = User.fetch_username_by_id(user_id)
            meals = Orders.find_orders_by_user_id(user_id)
            if not meals:
                return OrderError.NotFound('No orders placed by {}'.format(username))
            else:
                for meal in meals:
                    single_meal = {'meal_id': meal[1],
                                   'name': meal[4],
                                   'quantity': meal[5],
                                   'price': meal[6],
                                   'meal_total': int(meal[5]) * int(meal[6])}

                    all_meals.append(single_meal)
                    meal_totals = single_meal.get('meal_total')

            obj = {'Order No {}:'.format(order[0]): {"user_id": user_id,
                                                     "ordered_by": username[0],
                                                     "date_created": order[3],
                                                     "status": order[4],
                                                     "meals_ordered": all_meals,
                                                     "subtotal": meal_totals,
                                                     "delivery_fee": 50,
                                                     "TOTAL": order[6]}}
            # data = Response.define_orders(order)
            return Response.complete_request(obj)
        except OrderError.NotFound as e:
            return e.message

    @admin_required
    def put(self, order_id, user_id):
        """Endpoint for updating a particular order."""
        order = Orders.find_by_id(order_id)
        data = request.get_json(force=True)
        try:
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
            else:
                status = data['status']

                Orders.update_order(order_id, status)
                return jsonify({'order': 'Updated'}, 200)
        except OrderError.NotFound as e:
            return e.message

    @user_required
    def delete(self, order_id, user_id):
        """Endpoint for deleting a particular order."""
        order = Orders.find_by_id(order_id)
        try:
            if order:
                Orders.delete(order_id)
                response = "Order No {} has been deleted!".format(order_id)
                return Response.complete_request(response)
            else:
                raise OrderError.NotFound("Order No {} does not exist!".format(order_id))
        except OrderError.NotFound as e:
            return e.message


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('orders/<int:order_id>',
                    view_func=order_view,
                    methods=['PUT', 'GET', 'PATCH', 'DELETE'])
