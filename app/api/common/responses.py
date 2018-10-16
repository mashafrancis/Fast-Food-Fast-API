from flask import jsonify, make_response


class Response:
    """API Responses customized"""

    @staticmethod
    def define_orders(order):
        """Return a dictionary of the orders object"""
        obj = {order[0]: {"menu_id": order[2],
                          "user_id": order[3],
                          "name": order[5],
                          "quantity": order[6],
                          "price": order[7],
                          "meal_total": order[8],
                          "date_created": order[4],
                          "status": order[9]}}
        # obj = {order[0]: {"user_id": order[2],
        #                   "name": order[3],
        #                   "quantity": order[4],
        #                   "price": order[5],
        #                   "date_created": order[6],
        #                   "status": order[7]}}
        return obj

    @staticmethod
    def define_users(user):
        """Return a dictionary of the users object"""
        obj = {user[0]: {"username": user[1],
                         "email": user[2],
                         "date_registered": user[4],
                         "role": user[5]}}
        # obj = {
        #     'user_id': user['user_id'],
        #     'username': user['username'],
        #     'email': user['email'],
        #     'password': user['password'],
        #     'role': user['role'],
        #     'date_registered': user['date_registered']
        # }
        return obj

    @staticmethod
    def define_menu(menu):
        """Return a dictionary of the menu object"""
        obj = {menu[0]: {"name": menu[1],
                         "description": menu[2]}}
        return obj

    @staticmethod
    def define_meal(meal):
        """Return a dictionary of the meal object"""
        obj = {meal[0]: {"menu_id": meal[1],
                         "name": meal[2],
                         "description": meal[3],
                         "price": meal[4]}}
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


class ForbiddenAction(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Forbidden Action",
                                              "message": message}), 403)


class NotFound(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Not Found",
                                              "message": message}), 404)


class Conflict(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Conflict",
                                              "message": message}), 409)


class InternalServerError(Exception):
    def __init__(self, message):
        self.message = make_response(jsonify({"status": "Internal Server Error",
                                             "message": message}), 500)
