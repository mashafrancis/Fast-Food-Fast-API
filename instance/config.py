import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET') or 'you-will-never-guess-me'
    FAST_FOOD_ADMIN = os.environ.get('ADMIN_EMAIL')
    DATABASE_URL = os.getenv("DATABASE_URL")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Configurations for Productions."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
