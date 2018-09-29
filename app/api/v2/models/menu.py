from app.api.common.utils import Utils
from app.database.database import Database

import app.api.common.responses as MenuError


class Menu:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Category {self.name}'

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description
        }

    def save(self):
        """Method to add a new category"""
        data = [self.name, self.description]
        query = """INSERT INTO menu (name, description) VALUES (%s, %s) RETURNING id"""
        return Database.insert(query, data)

    @staticmethod
    def list_all_menu():
        """Method lists all available menu in a table"""
        query = """SELECT * FROM menu"""
        return Database.find_all(query)

    @classmethod
    def find_by_id(cls, menu_id):
        """Method finds an order by it's menu_id"""
        query = """SELECT * FROM menu WHERE id = %(id)s"""
        data = {'id': menu_id}
        return Database.find_one(query, data)

    @classmethod
    def find_by_name(cls, name):
        """Method finds an order by it's menu_id"""
        query = """SELECT * FROM menu WHERE name = %(name)s"""
        data = {'name': name}
        return Database.find_one(query, data)

    @staticmethod
    def delete(menu_id):
        """Method deletes a single menu by it's id"""
        query = """DELETE FROM menu WHERE id = %(id)s"""
        data = {'id': menu_id}
        return Database.remove_one(query, data)

    @staticmethod
    def delete_all():
        """Method deletes all data from the menu table"""
        query = """TRUNCATE TABLE menu"""
        Database.remove_all(query)

    @staticmethod
    def find_one_entry():
        """Method finds if one entry exists"""
        query = """SELECT * FROM menu LIMIT 1"""
        return Database.check_entry(query)

    @staticmethod
    def validate_menu_details(name, description):
        """
        This method validates the menu input details
        :param description:
        :param name:
        :return: True if valid, or False otherwise
        """
        if name and description:
            if not Utils.name_checker(name):
                raise MenuError.BadRequest('Invalid name!')

        else:
            if not name:
                raise MenuError.BadRequest('Please provide name!')
            if not description:
                raise MenuError.BadRequest('Please provide some description!')
        return True
