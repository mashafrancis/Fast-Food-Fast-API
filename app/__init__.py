from flask import Flask
from flask_cors import CORS

from app.database.tables import create_tables
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app_config[config_name].init_app(app)

    with app.app_context():
        create_tables()

    CORS(app)

    return app
