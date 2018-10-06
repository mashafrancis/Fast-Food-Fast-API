import re

from werkzeug.security import generate_password_hash, check_password_hash


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
        # name_checker = re.match(r"(?=^.{4,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", name)
        name_checker = re.match(r"^.{3,}[a-zA-Z_]+$", name)
        return True if name_checker else False

    @staticmethod
    def description_checker(name):
        # name_checker = re.match(r"(?=^.{4,}$)(?=.*[a-z])^[A-Za-z0-9_-]+( +[A-Za-z0-9_-]+)*$", name)
        name_checker = re.match(r"^.{3,}$", name)
        return True if name_checker else False

    @staticmethod
    def hash_password(password):
        """
        Hashes the password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return generate_password_hash(password)

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

    @staticmethod
    def url_id_valid(url_id):
        """Check url id parameter to be a valid number"""
        url_id_checker = re.match(r"^[1-9][0-9]*$", url_id)
        return True if url_id_checker else False

    @staticmethod
    def valid_string_inputs(field):
        return re.match("^[a-zA-Z0-9-\._@ `]+$", field)

    @staticmethod
    def valid_positive_integers(field):
        integer_checker = field <= 0
        return True if integer_checker else False

