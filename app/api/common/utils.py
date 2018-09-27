import re
import time

from abc import abstractmethod, ABCMeta
from passlib.handlers.pbkdf2 import pbkdf2_sha512


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
    def timestamp():
        """Return the current timestamp as an integer."""
        return int(time.time())

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checked that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at the stage
        :param password: sha512-ashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)


class Savable(metaclass=ABCMeta):
    def save_user(self):
        collection = 'users'
        Database.insert(collection, self.to_dict())

    def save_order(self):
        collection = 'orders'
        Database.insert(collection, self.to_dict())

    def save_blacklist(self):
        collection = 'blacklist'
        Database.insert(collection, self.to_dict())

    def save_role(self):
        collection = 'role'
        Database.insert(collection, self.to_dict())

    def save_category(self):
        collection = 'category'
        Database.insert(collection, self.to_dict())

    @abstractmethod
    def to_dict(self):
        pass
