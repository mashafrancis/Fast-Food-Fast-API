from datetime import datetime

from app.data import Database
from app.api.v1.common.utils import Savable


class BlackList(Savable):
    """Creates a model to handle token blacklist"""
    collection = 'blacklist'

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
        blacklist = BlackList(self.token)
        blacklist.save_blacklist()
        return self.to_dict()

    @staticmethod
    def check_token(token):
        """Check if token exists"""
        finder = (lambda x: x['token'] == token)
        response = Database.find_one(BlackList.collection, finder)
        if response:
            return True
        else:
            return False
