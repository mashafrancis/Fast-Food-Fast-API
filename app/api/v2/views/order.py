from flask import request, jsonify, Blueprint, make_response
from flask.views import MethodView

import app.api.common.responses as Error
from app.api.common.decorators import admin_required
from app.api.common.responses import Response
from app.api.v2.models.order import Orders
from app.api.v2.models.user import User

orders = Blueprint('order', __name__)


class OrdersView(MethodView):
    """Contains GET and POST methods"""

    @admin_required
    def get(self, user_id):
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

    # def post(self):
    #     """Endpoint for adding a new order."""
    #     data = request.get_json(force=True)
    #     meal_id = data['meal_id']
    #     quantity = data['quantity']
    #
    #     meal = Meal.find_by_id(meal_id)
    #     ordered_meal = Orders.find_meal_by_its_id(meal_id)
    #     try:
    #         if not meal:
    #             raise Error.NotFound('Meal not available')
    #         elif ordered_meal:
    #             raise Error.Conflict('Meal already exists. Do you want to update the meal item quantity?')
    #         else:
    #             name = meal[2]
    #             price = meal[4]
    #             # if ordered_meal is True:
    #             #     Orders.find_orders_by_user_id(user_id)
    #
    #         order = Orders(user_id=0,
    #                        name=name,
    #                        quantity=quantity,
    #                        price=price)
    #
    #         order.save()
    #         return Response.create_resource('Order has been placed successfully.')
    #     except Error.Conflict as e:
    #         return e.message
    #     except Error.NotFound as e:
    #         return e.message

    @admin_required
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


class OrderView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""

    @admin_required
    def get(self, order_id, user_id):
        """Endpoint for fetching a particular order."""
        try:
            all_meals = []
            # if not Utils.url_id_valid(order_id):
            #     raise Error.BadRequest('Invalid input parameter. Only integers are allowed.')
            order = Orders.find_by_id(order_id)
            if order:
                order_user = order[3]
            # if not order:
                username = User.fetch_username_by_id(order_user)
                meals = Orders.find_orders_by_user_id(order_user)
                if not meals:
                    raise Error.NotFound('No orders placed by {}'.format(username))
                else:
                    for order in meals:
                        single_meal = {'meal_id': order[2],
                                       'name': order[5],
                                       'quantity': order[6],
                                       'price': order[7],
                                       'meal_total': int(order[6]) * int(order[7])}

                        all_meals.append(single_meal)
                        # meal_totals = single_meal.get('meal_total')

                obj = {'Order No {}:'.format(order[0]): {"user_id": user_id,
                                                         "ordered_by": username[0],
                                                         "date_created": order[4],
                                                         "status": order[9],
                                                         "meals_ordered": all_meals,
                                                         "subtotal": 10,
                                                         "delivery_fee": 50,
                                                         "TOTAL": order[8]}}
                # data = Response.define_orders(order)
                return Response.complete_request(obj)
            raise Error.NotFound("Sorry, Order No {} does't exist!".format(order_id))
        except Error.NotFound as e:
            return e.message
        except Error.BadRequest as e:
            return e.message

    @admin_required
    def put(self, order_id, user_id):
        """Endpoint for updating a particular order."""
        try:
            order = Orders.find_by_id(order_id)
            data = request.get_json(force=True)
            if not order:
                raise Error.NotFound("Sorry, Order No {} doesn't exist yet! Create one.".format(order_id))
            else:
                status = data['status']

                Orders.update_order(order_id, status)
                return jsonify({'order': 'Order has been updated'}, 200)
        except Error.NotFound as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for missing field: " + str(error)}), 400)

    @admin_required
    def delete(self, order_id, user_id):
        """Endpoint for deleting a particular order."""
        order = Orders.find_by_id(order_id)
        try:
            if order:
                Orders.delete(order_id)
                response = "Order No {} has been deleted!".format(order_id)
                return Response.complete_request(response)
            else:
                raise Error.NotFound("Order No {} does not exist!".format(order_id))
        except Error.NotFound as e:
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
