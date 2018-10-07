from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

import app.api.common.responses as MealError
from app.api.common.decorators import admin_required
from app.api.common.utils import Utils

from app.api.v2.models.meal import Meal
from app.api.common.responses import Response
from app.api.v2.models.menu import Menu

meals = Blueprint('meals', __name__)


class MealsView(MethodView):
    """Contains GET and POST methods"""

    def get(self, menu_id):
        """Endpoint for fetching all meals."""
        results = []
        # if not menu_id == int(menu_id):
        #     # if Utils.url_id_valid(menu_id):
        #     raise MealError.BadRequest('Invalid menu_id format! This should be an integer.')
        all_meals = Meal.list_all_meals()
        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist yet! Create one?")

            if all_meals:
                for meal in all_meals:
                    obj = Response.define_meal(meal)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise MealError.NotFound('Sorry, No Meal found!')
        except MealError.NotFound as e:
            return e.message

    @admin_required
    def post(self, menu_id, user_id):
        """Endpoint for adding a new meal."""
        data = request.get_json(force=True)
        name = data['name']
        description = data['description']
        price = data['price']

        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist yet! Create one?")

            Meal.validate_meal_details(name, description, price)
            meal = Meal.find_by_name(name)
            if not meal:
                new_meal = Meal(name=name,
                                description=description,
                                price=price)
                new_meal.save(menu_id)
                return Response.create_resource('A new meal has been offered.')
            raise MealError.Conflict('You can not add the same meal item twice. Do you want to update?')

        except MealError.Conflict as e:
            return e.message
        except MealError.BadRequest as e:
            return e.message
        except MealError.NotFound as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)

    @admin_required
    def delete(self, menu_id, user_id):
        """Endpoint for deleting all meals."""
        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist! You cannot delete from an empty menu!")

            if not Meal.find_one_entry():
                raise MealError.NotFound('There is no meal here!')
            else:
                Meal.delete_all()
                return Response.complete_request('Meals have been successfully deleted!')
        except MealError.NotFound as e:
            return e.message


class MealView(MethodView):
    """Contains GET, PUT and DELETE methods for manipulating a single meal"""

    def get(self, menu_id, meal_id):
        """Endpoint for fetching a particular order."""
        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist yet! Create one?")
            else:
                meal = Meal.find_by_id(meal_id)
            if not meal:
                raise MealError.NotFound("Sorry, Meal does't exist! Create one?")
            data = Response.define_meal(meal)
            return Response.complete_request(data)
        except MealError.NotFound as e:
            return e.message

    @admin_required
    def put(self, menu_id, meal_id, user_id):
        """Endpoint for updating a particular meal."""
        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist yet! Create one?")

            data = request.get_json(force=True)
            meal = Meal.find_by_id(meal_id)
            if not meal:
                raise MealError.NotFound("Meal does not exist yet! Create one?")
            else:
                name = data['name']
                description = data['description']
                price = data['price']

                Meal.update_meal(meal_id, name=name, description=description, price=price)
                updated_meal = Meal.find_by_id(meal_id)
                obj = Response.define_meal(updated_meal)
                return Response.complete_request(obj)
        except MealError.NotFound as e:
            return e.message
        except Exception as error:
            return make_response(jsonify(
                {"error": "Please provide for all the fields. Missing field: " + str(error)}), 400)

    @admin_required
    def delete(self, menu_id, meal_id, user_id):
        """Endpoint for deleting a particular order."""
        try:
            menu = Menu.find_by_id(menu_id)
            if not menu:
                raise MealError.NotFound("Menu does not exist yet! Create one?")

            meal = Meal.find_by_id(meal_id)
            if meal:
                Menu.delete(meal_id)
                response = "Meal has been deleted!"
                return Response.complete_request(response)
            else:
                raise MealError.NotFound("Sorry, No Meal found!")
        except MealError.NotFound as e:
            return e.message


# Define API resource
meals_view = MealsView.as_view('meals_view')
meal_view = MealView.as_view('meal_view')

meals.add_url_rule('menu/<int:menu_id>/meals',
                   view_func=meals_view,
                   methods=['POST', 'GET', 'DELETE'])

meals.add_url_rule('menu/<int:menu_id>/meals/<int:meal_id>',
                   view_func=meal_view,
                   methods=['PUT', 'GET', 'DELETE'])
