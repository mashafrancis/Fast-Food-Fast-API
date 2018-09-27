from datetime import datetime, timedelta

import jwt
from flask import current_app

import app.api.common.responses as UserErrors

from app.api.common.utils import Utils
from app.database.database import Database
from ....database.database_connection import DatabaseConnection


class User:
    collection = 'users'

    def __init__(self, username, email, password):
        # self.user_id = self.find_by_id(email)
        self.username = username
        self.email = email
        self.password = Utils.hash_password(password)
        # self.date_registered = datetime.now()
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
        data = [self.username, self.email, self.password, 'now']
        query = """INSERT INTO users (username, email, password_hash, date_registered) 
                    VALUES (%s, %s, %s, %s) RETURNING id"""
        Database.insert(query, data)

    @staticmethod
    def list_all_users():
        pass

    @classmethod
    def fetch_by_email(cls, email):
        """
        :param email:
        :return: user with the given email
        """
        with DatabaseConnection() as connection:
            cursor = connection.cursor()

            cursor.execute("""SELECT * FROM users WHERE email = %(email)s""",
                           {'email': email})

            rows = cursor.fetchone()
            cursor.close()
            connection.close()
        return rows

    @classmethod
    def get_password(cls, email):
        """
        Get the user's password using their email
        :param email:
        :return: user with the given email
        """
        with DatabaseConnection() as connection:
            cursor = connection.cursor()

            query = """SELECT password_hash FROM users WHERE email = %(email)s"""
            cursor.execute(query, {'email': email})

            password_hash = cursor.fetchone()
            cursor.close()
        return password_hash

    @classmethod
    def get_user_id(cls, email):
        """
        Get the user's id using their email
        :param email:
        :return: username for the given id
        """
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %(email)s",
                           {'email': email})

            user_id = cursor.fetchone()
            cursor.close()
        return user_id

    @classmethod
    def find_by_email(cls, email):
        """
        :param email:
        :return: user with the given email
        """
        with DatabaseConnection() as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE email = %(email)s",
                           {'email': email})

            rows = cursor.fetchone()
            cursor.close()
        return rows is not None

    @classmethod
    def find_by_id(cls, email):
        """
        :param email:
        :return: username for the given id
        """
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT id FROM users WHERE id = %(user_id)s""",
                           {'email': email})
            rows = cursor.fetchone()
            user_id = rows[0]
            cursor.close()
        return user_id

    @classmethod
    def find_by_username(cls, username):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %(username)s",
                           {'username': username})
            rows = cursor.fetchone()
            cursor.close()
        return rows is not None

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
