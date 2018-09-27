import datetime

from flask import request, jsonify, Blueprint
from flask.views import MethodView

import app.api.common.responses as OrderError

from app.api.v2.models.order import Orders
from app.api.common.responses import Response

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
                raise OrderError.NotFound('Sorry, No orders for you!')
        except OrderError.NotFound as e:
            return e.message

    def post(self):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        name = data['name']
        quantity = data['quantity']
        price = data['price']

        order = Orders(name=name,
                       quantity=quantity,
                       price=price)
        order.save()
        return Response.create_resource('Order has been added successfully.')

    def delete(self):
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

    def get(self, order_id):
        """Endpoint for fetching a particular order."""
        try:
            order = Orders.find_by_id(order_id)
            if not order:
                raise OrderError.NotFound("Sorry, Order No {} does't exist!".format(order_id))
            data = {order[0]: {"name": order[1],
                               "quantity": order[2],
                               "price": order[3],
                               "date_created": order[4],
                               "status": order[5]}}
            return Response.complete_request(data)
        except OrderError.NotFound as e:
            return e.message

    def put(self, order_id):
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


# Define API resource
orders_view = OrdersView.as_view('orders_view')
order_view = OrderView.as_view('order_view')

orders.add_url_rule('orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])

orders.add_url_rule('orders/<int:order_id>',
                    view_func=order_view,
                    methods=['PUT', 'GET', 'PATCH', 'DELETE'])
