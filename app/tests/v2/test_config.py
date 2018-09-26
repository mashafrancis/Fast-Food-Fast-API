import unittest

from app import create_app


class ConfigTestCase(unittest.TestCase):
    def test_app_environment_variables_production(self):
        """Test production environment"""
        self.app = create_app(config_name="production")
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(self.app.config['TESTING'] is False)
        self.assertFalse(self.app.config['SECRET_KEY'] is 'you-will-never-guess-me')

    def test_app_environment_variables_development(self):
        """Test development environment"""
        self.app = create_app(config_name="development")
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is False)
        self.assertFalse(self.app.config['SECRET_KEY'] is 'you-will-never-guess-me')

    def test_app_environment_variables_test(self):
        """Test testing environment"""
        self.app = create_app(config_name="testing")
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is True)
        self.assertFalse(self.app.config['SECRET_KEY'] is 'you-will-never-guess-me')

    def test_app_environment_variables_staging(self):
        """Test staging environment"""
        self.app = create_app(config_name="production")
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(self.app.config['TESTING'] is False)
        self.assertFalse(self.app.config['SECRET_KEY'] is 'you-will-never-guess-me')


if __name__ == '__main__':
    unittest.main()
