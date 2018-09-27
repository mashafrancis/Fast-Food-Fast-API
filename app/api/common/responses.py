from flask import jsonify, make_response


class Response:
    """API Responses customized"""

    @staticmethod
    def define_orders(order):
        """Return a dictionary of the orders object"""
        obj = {
            'order_id': order['order_id'],
            'name': order['name'],
            'quantity': order['quantity'],
            'price': order['price'],
            'date_created': order['date_created'],
            'created_by': order['created_by'],
            'status': order['status']
        }
        return obj

    @staticmethod
    def define_users(user):
        """Return a dictionary of the users object"""
        obj = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'password': user['password'],
            'role': user['role'],
            'date_registered': user['date_registered']
        }
        return obj

    @staticmethod
    def define_category(category):
        """Return a dictionary of the orders object"""
        obj = {
            'category_id': category['category_id'],
            'name': category['name'],
            'description': category['description'],
            'date_created': category['date_created']
        }
        return obj

    @staticmethod
    def complete_request(message):
        """For a successful request"""
        response = jsonify({"status": "OK",
                            "message": message})
        return make_response(response), 200

    @staticmethod
    def create_resource(message):
        """Creation of any resource"""
        response = jsonify({"status": "Created",
                            "message": message})
        return make_response(response), 201


class AuthResponse:
    """For authentication with token"""

    @staticmethod
    def create_user(message, token):
        response = jsonify({"status": "User Created",
                            "message": message,
                            "access_token": token})
        return make_response(response), 201

    @staticmethod
    def complete_request(message, token):
        response = jsonify({"status": "OK",
                            "message": message,
                            "access_token": token})
        return make_response(response), 200


class BadRequest(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Bad Request",
                                              "message": message}), 400)


class Unauthorized(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Unauthorized",
                                              "message": message}), 401)


class NotFound(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Not Found",
                                              "message": message}), 404)


class Conflict(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Conflict",
                                              "message": message}), 409)
