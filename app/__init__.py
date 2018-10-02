from flask import Flask

from app.database.tables import create_tables
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app_config[config_name].init_app(app)

    with app.app_context():
        create_tables()

    from app.api.v2.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v2/')

    from app.api.v2.views.order import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/api/v2/')

    from app.api.v2.views.menu import menu as menu_blueprint
    app.register_blueprint(menu_blueprint, url_prefix='/api/v2')

    from app.api.v2.views.meal import meals as meals_blueprint
    app.register_blueprint(meals_blueprint, url_prefix='/api/v2')

    return app
