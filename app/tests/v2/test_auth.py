import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class AuthTest(BaseTests):
    """Tests functionality of user endpoints."""

    def test_user_registration_and_login(self):
        """Test successful user registration and login."""
        with self.client():
            response = self.register_user(username='tester',
                                          email='test@gmail.com',
                                          password='test1234',
                                          confirm_password='test1234')
            data = json.loads(response.data.decode())
            self.assertIn('test@gmail.com', str(response.data))
            # self.assertIsNotNone(User.find_by_email('test@gmail.com'))
            # self.assertIsNotNone(User.find_by_id(1))
            self.assertTrue(data['status'] == 'User Created')
            self.assertTrue(data['message'] == u"User test@gmail.com successfully registered.")
            self.assertFalse(data['message'] == u"User successfully registered")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertNotEqual(response.status_code, 200)

    def test_user_duplicate_registration(self):
        """Test unsuccessful registration due to duplicate email."""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.register_user('tester1', 'test@gmail.com', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Conflict')
            self.assertEqual(data['message'], u'User already exists! Please login.')
            self.assertEqual(response.status_code, 409)

    def test_duplicate_username(self):
        """Test unsuccessful registration due to duplicate username."""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.register_user('tester', 'test1@gmail.com', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Conflict')
            self.assertTrue(data['message'] == u'Username already exists! Kindly choose another.')
            self.assertEqual(response.status_code, 409)

    def test_user_login(self):
        """Test user successful login"""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.login_user('test@gmail.com', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'OK')
            self.assertTrue(data['message'] == 'You have logged in successfully!')
            self.assertTrue(data['access_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_invalid_login_password(self):
        """Test unsuccessful registration due to invalid login password."""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.login_user('test@gmail.com', 'test')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Wrong Password!')

    def test_missing_password(self):
        """Test unsuccessful registration due to missing password"""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.login_user('test@gmail.com', '')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your password is missing!')

    def test_missing_email(self):
        """Test unsuccessful registration due to missing email"""
        with self.client():
            self.register_user('tester', 'test@gmail.com', 'test1234', 'test1234')
            response = self.login_user('', 'test1234')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your email is missing!')

    def test_user_registration_fails_if_content_type_not_json(self):
        """Test the content type is application/json"""
        with self.client():
            response = self.register_user_wrong_content('tester', 'test@gmail.com', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Content-Type must be JSON.')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_email(self):
        """Test unsuccessful registration due to missing email"""
        with self.client():
            response = self.register_user('tester2', '', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please provide email!')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_username(self):
        """Test unsuccessful registration due to missing username"""
        with self.client():
            response = self.register_user('', 'test@gmail.com', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please provide username!')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_password(self):
        """Test unsuccessful registration due to missing password"""
        with self.client():
            response = self.register_user('tester3', 'test@gmail.com', '', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please provide password!')
            self.assertEqual(response.status_code, 400)

    def test_user_registration_missing_confirmation_password(self):
        """Test unsuccessful registration due to missing confirmation password"""
        with self.client():
            response = self.register_user('tester4', 'test@gmail.com', 'test1234', '')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Please confirm password!')
            self.assertEqual(response.status_code, 400)

    def test_user_email_validity(self):
        """Test unsuccessful registration due to invalid email"""
        with self.client():
            response = self.register_user('tester5', 'test', 'test1234', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your email is invalid! '
                                               'Kindly provide use with the right email address format')
            self.assertEqual(response.status_code, 400)

    def test_user_invalid_password(self):
        """Test unsuccessful registration due to short password"""
        with self.client():
            response = self.register_user('tester6', 'test@gmail.com', 'tes', 'tes')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Password must contain: '
                                               'lowercase letters, atleast a digit, and a min-length of 6')
            self.assertEqual(response.status_code, 400)

    def test_user_invalid_username(self):
        """Test unsuccessful registration due to invalid username"""
        with self.client():
            response = self.register_user('1', 'test@gmail.com', 'test123', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Username must contain at least letter; '
                                               'plus other letters or digits and with a min length of 3')
            self.assertEqual(response.status_code, 400)

    def test_user_mismatch_password(self):
        """Test unsuccessful registration due to password mismatch"""
        with self.client():
            response = self.register_user('tester7', 'test@gmail.com', 'test1234', 'test4321')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Bad Request')
            self.assertTrue(data['message'] == 'Your password must match!')
            self.assertEqual(response.status_code, 400)

    def test_login_non_registered(self):
        """Test login for non-registered user"""
        with self.client():
            response = self.login_user('test@gmail.com', 'test1234')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertTrue(data['message'] == 'User does not exist. Kindly register!')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_login_has_correct_email(self):
        """Test login email has the correct format"""
        with self.client():
            response = self.login_user('test.com', 'test1234')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type == 'application/json')
            self.assertTrue(data['status'] == 'Unauthorized')
            self.assertTrue(data['message'] == 'Your email is invalid! Kindly recheck your email.')

    # def test_user_logout(self):
    #     """Test a user can logout through the POST request"""
    #     with self.client():
    #
    #         logout = self.user_logout(access_token)
    #         self.assertTrue(logout.status_code, 200)
    #         logout_again = self.user_logout(access_token)
    #         self.assertTrue(logout_again.status_code, 401)

    def test_get_all_users(self):
        """Tests API can get all users (GET)"""
        with self.client():
            access_token = self.get_admin_token()

            # Test for users found.
            self.user_register_login()
            response = self.client().get('/api/v2/users',
                                         headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 200)

            # Test API can get a single user by ID
            # response = self.client().get('/api/v2/users/1',
            #                              headers=dict(Authorization="Bearer " + access_token))
            # self.assertEqual(response.status_code, 200)

            # # Test API cannot get a non existent user
            # response = self.client().get('/api/v2/users/10',
            #                              headers=dict(Authorization="Bearer " + access_token))
            # data = json.loads(response.data.decode())
            # self.assertEqual(response.status_code, 404)
            # self.assertTrue(data['status'] == 'Not Found')
            # self.assertEqual(data['message'], u"Sorry, User ID No 10 does't exist!")


if __name__ == '__main__':
    unittest.main()
