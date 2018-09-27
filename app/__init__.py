from flask import Flask
from flask_cors import CORS

from app.database.tables import create_tables
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app_config[config_name].init_app(app)
    CORS(app)

    with app.app_context():
        create_tables()

    from app.api.v2.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v2/')

    return app
