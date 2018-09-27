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
            if Orders.find_one_entry():
                raise OrderError.NotFound('No orders available!')
            else:
                Orders.delete_all()
                return Response.complete_request('All orders have been successfully deleted!')
        except OrderError.NotFound as e:
            return e.message


# Define API resource
orders_view = OrdersView.as_view('orders_view')

orders.add_url_rule('orders',
                    view_func=orders_view,
                    methods=['POST', 'GET', 'DELETE'])
