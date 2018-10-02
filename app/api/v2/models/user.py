from datetime import datetime, timedelta

import jwt
from flask import current_app

import app.api.common.responses as UserErrors

from app.api.common.utils import Utils
from app.database.database import Database


class User:

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = Utils.hash_password(password)
        if self.email == current_app.config['FAST_FOOD_ADMIN']:
            self.role = 'admin'
        else:
            self.role = 'user'

    def __repr__(self):
        return '<User {}'.format(self.email)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }

    def save(self):
        """
        Save a new user to the database
        :return: user_id
        """
        data = [self.username, self.email, self.password, 'now', self.role]
        query = """INSERT INTO users (username, email, password_hash, date_registered, user_role) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING id"""
        Database.insert(query, data)

    @staticmethod
    def list_all_users():
        pass

    @staticmethod
    def fetch_email(email):
        """Method to search with user email"""
        query = """SELECT email FROM users WHERE email = %(email)s"""
        data = {'email': email}
        return Database.find_one(query, data)

    @staticmethod
    def fetch_password(email):
        """Method returns a user's password"""
        query = """SELECT password_hash FROM users WHERE email = %(email)s"""
        data = {'email': email}
        return Database.find_one(query, data)

    @staticmethod
    def fetch_user_id(email):
        """Method returns the user's id by querying the email"""
        query = """SELECT id FROM users WHERE email = %(email)s"""
        data = {'email': email}
        return Database.find_one(query, data)

    @staticmethod
    def fetch_role(email):
        """Method to return the user's role"""
        query = """SELECT user_role::varchar(80) FROM users"""
        data = (email,)
        # query = """SELECT user_role FROM users WHERE email = %s"""
        # data = (email,)
        return Database.find_one(query, data)

    @staticmethod
    def find_by_username(username):
        """Method returns the user's username"""
        query = """SELECT * FROM users WHERE username = %(username)s"""
        data = {'username': username}
        return Database.find_one(query, data)

    @staticmethod
    def find_by_id(user_id):
        """Method to return user's id"""
        # query = """SELECT * FROM users WHERE id = %(id)s"""
        query = """SELECT id::int FROM users"""
        data = {'id': user_id}
        if Database.find_one(query, data):
            return True
        return False

    @staticmethod
    def delete(user_id):
        pass

    @staticmethod
    def generate_token(user_id):
        """
        Generates authentication token.
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create byte string token using payload and secret key
            jwt_string = jwt.encode(
                payload,
                current_app.config['SECRET'],
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(access_token):
        """
        Decode the access token from the authorization.
        :param access_token:
        :return: integer or string
        """
        try:
            payload = jwt.decode(access_token, current_app.config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature Expired. Please login!"
        except jwt.InvalidTokenError:
            return "Invalid Token. Please Register or Login"

    @staticmethod
    def validate_register_details(email, username, password, confirm_password):
        """
        This method register a user using email and password.
        The password already comes hashed as sha-512
        :param confirm_password: User has to confirm password
        :param username: User's username
        :param email: User's email (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise
        """
        if email and username and password and confirm_password:
            if not Utils.email_is_valid(email):
                raise UserErrors.BadRequest("Your email is invalid! "
                                            "Kindly provide use with the right email address format")
            if not Utils.username_checker(username):
                raise UserErrors.BadRequest("Username must contain at least letter; "
                                            "plus other letters or digits and with a min length of 3")
            if User.find_by_username(username):
                raise UserErrors.Conflict('Username already exists! Kindly choose another.')
            if not Utils.password_checker(password):
                raise UserErrors.BadRequest("Password must contain: "
                                            "lowercase letters, atleast a digit, and a min-length of 6")
            if confirm_password != password:
                raise UserErrors.BadRequest('Your password must match!')

        else:
            if not username:
                raise UserErrors.BadRequest('Please provide username!')
            if not email:
                raise UserErrors.BadRequest('Please provide email!')
            if not password:
                raise UserErrors.BadRequest('Please provide password!')
            if not confirm_password:
                raise UserErrors.BadRequest('Please confirm password!')

        return True
