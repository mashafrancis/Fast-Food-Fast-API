from flask import request, Blueprint, jsonify, make_response
from flask.views import MethodView

import app.api.common.responses as MenuError
from app.api.common.decorators import admin_required
from app.api.common.responses import Response
from app.api.v2.models.menu import Menu

menu = Blueprint('menu', __name__)


class MenuView(MethodView):
    """Contains GET and POST methods"""

    @admin_required
    def post(self, user_id):
        """Endpoint for adding a new menu category."""
        try:
            data = request.get_json(force=True)
            name = data['name']
            description = data['description']

            Menu.validate_menu_details(name, description)
            menu_name = Menu.find_by_name(name)
            if not menu_name:
                new_menu = Menu(name=name,
                                description=description)
                new_menu.save()
                return Response.create_resource('A new menu has been added successfully.')
            raise MenuError.Conflict('The menu name already exists. Should you update?')

        except MenuError.Conflict as e:
            return e.message
        except MenuError.BadRequest as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)

    def get(self):
        """Endpoint for fetching all menu categories."""
        results = []
        all_menu = Menu.list_all_menu()
        try:
            if all_menu:
                for _menu in all_menu:
                    obj = Response.define_menu(_menu)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise MenuError.NotFound('Sorry, No Menu found! Create one.')
        except MenuError.NotFound as e:
            return e.message

    @admin_required
    def delete(self, user_id):
        """Endpoint for deleting all menu categories."""
        try:
            if not Menu.find_one_entry():
                raise MenuError.NotFound('There is no menu here!')
            else:
                Menu.delete_all()
                return Response.complete_request('All menu has been successfully deleted!')
        except MenuError.NotFound as e:
            return e.message


class MenuIdView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""

    def get(self, menu_id):
        """Endpoint for fetching a particular order."""
        try:
            # if Utils.valid_positive_integers(menu_id):
            #     raise MenuError.BadRequest('You cannot have a negative or null menu_id!')
            menu_name = Menu.find_by_id(menu_id)
            if not menu_name:
                raise MenuError.NotFound("Sorry, Menu does't exist!")
            data = Response.define_menu(menu_name)
            return Response.complete_request(data)
        except MenuError.NotFound as e:
            return e.message

    @admin_required
    def put(self, menu_id, user_id):
        """Endpoint for updating a particular order."""
        try:
            menu_name = Menu.find_by_id(menu_id)
            if not menu_name:
                raise MenuError.BadRequest('Menu Name not posted!')
            data = request.get_json(force=True)
            if not menu_name:
                raise MenuError.NotFound("Sorry, Menu does't exist! Create one?")
            else:
                menu_name = data['name']
                description = data['description']

                Menu.validate_menu_details(menu_name, description)
                Menu.update_menu(menu_id, name=menu_name, description=description)
                return jsonify({'order': 'Updated'}, 200)
        except MenuError.NotFound as e:
            return e.message
        except MenuError.BadRequest as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for the missing field. Missing field: " + str(error)}), 400)

    @admin_required
    def delete(self, menu_id, user_id):
        """Endpoint for deleting a particular order."""
        menu_name = Menu.find_by_id(menu_id)
        try:
            if menu_name:
                Menu.delete(menu_id)
                response = "Menu has been deleted!"
                return Response.complete_request(response)
            else:
                raise MenuError.NotFound("Sorry, No Menu found! Create one.")
        except MenuError.NotFound as e:
            return e.message


# Define API resource
menu_view = MenuView.as_view('menu_view')
menu_id_view = MenuIdView.as_view('menu_id_view')

menu.add_url_rule('menu',
                  view_func=menu_view,
                  methods=['POST', 'GET', 'DELETE'])

menu.add_url_rule('menu/<int:menu_id>',
                  view_func=menu_id_view,
                  methods=['PUT', 'GET', 'DELETE'])
