import re
import time

from werkzeug.security import generate_password_hash, check_password_hash
import app.api.common.responses as Errors


class Utils:
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def password_checker(password):
        password_checker = re.match(r"^(?=.*[a-z])(?=.*[0-9]){6}", password)
        return True if password_checker else False

    @staticmethod
    def username_checker(username):
        username_checker = re.match(r"(?=^.{3,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", username)
        return True if username_checker else False

    @staticmethod
    def name_checker(name):
        name_checker = re.match(r"(?=^.{4,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", name)
        return True if name_checker else False

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checked that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at the stage
        :param password: sha512-ashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return check_password_hash(hashed_password, password)
