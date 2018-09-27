from datetime import datetime, timedelta

import jwt
from flask import current_app

import app.api.common.responses as UserErrors

from app.api.common.utils import Savable, Utils
from app.database.tables import dbconn


class User(Savable):
    collection = 'users'

    def __init__(self, username, email, password):
        super().__init__()
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
        return f'<User {self.email}'

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }

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

    def add_user(self):
        """Adds user to the list"""
        user = User(self.username,
                    self.email,
                    Utils.hash_password(self.password))
        user.save_user()

    def save(self):
        connection = dbconn()
        cursor = connection.cursor()

        data = [self.username, self.email, self.password, 'now']
        query = """INSERT INTO users (username, email, password_hash, date_registered) 
                    VALUES (%s, %s, %s, %s) RETURNING user_id"""
        cursor.execute(query, data)

        user_id = cursor.fetchone()[0]
        cursor.close()
        connection.commit()
        connection.close()

        return int(user_id)

    @staticmethod
    def list_all_users():
        pass

    @classmethod
    def get_by_email(cls, email):
        """
        :param email:
        :return: user with the given email
        """
        connection = dbconn()
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
        :param email:
        :return: user with the given email
        """
        connection = dbconn()
        cursor = connection.cursor()

        query = """SELECT password_hash FROM users WHERE email = %(email)s"""
        cursor.execute(query, {'email': email})

        password_hash = cursor.fetchone()
        cursor.close()
        connection.close()

        return password_hash

    @classmethod
    def get_user_id(cls, email):
        """
        :param email:
        :return: username for the given id
        """
        connection = dbconn()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = %(email)s",
                       {'email': email})

        user_id = cursor.fetchone()
        cursor.close()
        connection.close()

        return user_id

    @classmethod
    def find_by_email(cls, email):
        """
        :param email:
        :return: user with the given email
        """
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %(email)s",
                       {'email': email})

        rows = cursor.fetchone()
        cursor.close()
        connection.close()

        return rows is not None

    @classmethod
    def find_by_id(cls, email):
        """
        :param email:
        :return: username for the given id
        """
        connection = dbconn()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = %(user_id)s",
                       {'email': email})
        rows = cursor.fetchone()
        user_id = rows[0]
        cursor.close()
        connection.close()

        return user_id

    @classmethod
    def find_by_username(cls, username):
        connection = dbconn()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %(username)s",
                       {'username': username})
        rows = cursor.fetchone()
        cursor.close()
        connection.close()

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
