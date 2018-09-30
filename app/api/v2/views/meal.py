from flask import Blueprint
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


# Define API resource
meals_view = MealsView.as_view('meals_view')

meals.add_url_rule('menu/<int:menu_id>/meals',
                   view_func=meals_view,
                   methods=['POST', 'GET', 'DELETE'])
