import json
import os
import sys  # Fix import errors
import unittest

import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.tables import drop_tables, create_tables
from app import create_app


class BaseTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.connection = psycopg2.connect(os.getenv('DATABASE_TEST_URL'))
        self.cursor = self.connection.cursor()

        with self.app.app_context():
            create_tables()

            self.order = json.dumps({
                'name': 'Burger',
                'quantity': '10',
                'price': '1000',
                'created_by': 'Test'
            })

            self.order2 = json.dumps({
                'name': 'Burger-2',
                'quantity': '20',
                'price': '2000',
                'created_by': 'Test',
                'status': 'Accepted'
            })

            self.menu = json.dumps({
                'name': 'Drinks',
                'description': 'Get your drinks!'
            })

            self.menu2 = json.dumps({
                'name': 'Drinks-2',
                'description': 'Get your drinks-2!'
            })

    def register_user(self, username, email, password, confirm_password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v2/auth/register',
            content_type='application/json',
            data=json.dumps(dict(username=username, email=email,
                                 password=password, confirm_password=confirm_password)))

    def register_user_wrong_content(self, username, email, password, confirm_password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v2/auth/register',
            content_type='wrong',
            data=json.dumps(dict(username=username, email=email,
                                 password=password, confirm_password=confirm_password)))

    def login_user(self, email, password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def user_register_login(self):
        """Method for registration and login"""
        # Register user
        response = self.register_user('moonpie', 'moonpie@gmail.com', 'test1234', 'test1234')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'User Created')
        self.assertTrue(data['message'] == u"User moonpie@gmail.com successfully registered.")
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

        # Login user
        response2 = self.login_user('moonpie@gmail.com', 'test1234')
        data2 = json.loads(response2.data.decode())
        self.assertTrue(data2['status'] == 'OK')
        self.assertTrue(data2['message'] == 'You have logged in successfully!')
        self.assertTrue(response2.content_type == 'application/json')
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(data2['access_token'])

        return data2

    def user_logout(self, token):
        """Method to logout a user"""
        response = self.client().post(
            '/api/v2/auth/logout',
            headers=dict(Authorization='Bearer ' + token))
        return response

    def get_user_token(self):
        """Get user token"""
        auth_response = self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
        return json.loads(auth_response.data.decode())['access_token']

    def create_order(self, token):
        """Create a dummy order"""
        response = self.client().post(
            '/api/v2/orders',
            data=self.order,
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertIn('Burger', str(response.data))
        self.assertTrue(data['message'] == u"Order has been added successfully.")
        self.assertEqual(response.status_code, 201)

    def user_token_get(self):
        self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
        data = self.login_user('test@gmail.com', 'test1234')
        access_token = json.loads(data.data.decode())['access_token']
        return access_token

    def tearDown(self):
        with self.app.app_context():
            drop_tables()
