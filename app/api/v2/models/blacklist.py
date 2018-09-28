from datetime import datetime

from app.database.database import Database


class BlackList:
    """Creates a model to handle token blacklist"""

    def __init__(self, token):
        self.token = token
        self.blacklisted_date = datetime.now()

    def __repr__(self):
        return '<token: {}'.format(self.token)

    def to_dict(self):
        return {
            'token': self.token,
            'blacklisted_date': self.blacklisted_date
        }

    def save(self):
        data = [self.token]
        query = """INSERT INTO blacklist (tokens) VALUES (%s) RETURNING id"""
        return Database.insert(query, data)

    @staticmethod
    def check_token(tokens):
        """Check if token exists"""
        query = """SELECT * FROM blacklist WHERE tokens = (tokens)"""
        response = Database.check_entry(query)
        if response:
            return True
        else:
            return False
