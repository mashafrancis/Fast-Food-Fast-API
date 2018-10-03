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
        data = [self.token, 'now']
        query = """INSERT INTO blacklist (tokens, blacklisted_date) 
                                VALUES (%s, %s) RETURNING id"""
        return Database.insert(query, data)

    def check_token(self):
        """Check if token exists"""
        # data = [self.token]
        # query = """SELECT tokens::int FROM blacklist"""
        query = """SELECT tokens FROM blacklist WHERE tokens = '%s'""" % self.token
        response = Database.return_one(query)
        if response:
            return True
        return False
