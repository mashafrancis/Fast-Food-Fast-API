from flask import Blueprint, request
from flask.views import MethodView

import app.api.common.responses as MealError
from app.api.common.decorators import admin_required

from app.api.v2.models.meal import Meal
from app.api.common.responses import Response

meals = Blueprint('meals', __name__)


class MealsView(MethodView):
    """Contains GET and POST methods"""

    # @admin_required
    def get(self, menu_id):
        """Endpoint for fetching all meals."""
        results = []
        all_meals = Meal.list_all_meals()
        try:
            if all_meals:
                for meal in all_meals:
                    obj = Response.define_meal(meal)
                    results.append(obj)
                return Response.complete_request(results)
            else:
                raise MealError.NotFound('Sorry, No Meal found!')
        except MealError.NotFound as e:
            return e.message

    def post(self, menu_id):
        """Endpoint for adding a new order."""
        data = request.get_json(force=True)
        name = data['name']
        description = data['description']
        price = data['price']

        try:
            Meal.validate_meal_details(name, description, price)
            meal = Meal.find_by_name(name)
            if not meal:
                new_meal = Meal(name=name,
                                description=description,
                                price=price)
                new_meal.save()
                return Response.create_resource('A new meal has been offered.')
            raise MealError.Conflict('You can not add the same meal item twice. Do you want to update?')

        except MealError.Conflict as e:
            return e.message
        except MealError.BadRequest as e:
            return e.message

    def delete(self, menu_id):
        """Endpoint for deleting all orders."""
        try:
            if not Meal.find_one_entry():
                raise MealError.NotFound('There is no meal here!')
            else:
                Meal.delete_all()
                return Response.complete_request('Meals have been successfully deleted!')
        except MealError.NotFound as e:
            return e.message


# Define API resource
meals_view = MealsView.as_view('meals_view')

meals.add_url_rule('menu/<int:menu_id>/meals',
                   view_func=meals_view,
                   methods=['POST', 'GET', 'DELETE'])
