from app.api.common.utils import Utils
from app.database.database import Database

import app.api.common.responses as MealError


class Menu:
    def __init__(self, name, description, price=0):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return f'<Meal {self.name}'

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price
        }

    def save(self):
        """Method to add a new meal"""
        data = [self.name, self.description, self.price]
        query = """INSERT INTO meals (name, description, price) VALUES (%s, %s, %s) RETURNING id"""
        return Database.insert(query, data)

    @staticmethod
    def list_all_menu():
        """Method lists all available menu in a table"""
        query = """SELECT * FROM meals"""
        return Database.find_all(query)

    @staticmethod
    def update_menu(meal_id, name, description, price):
        """Methods updates the status of an order"""

        query = """UPDATE meals SET name = %(data1)s, description = %(data2)s, price = %(data3)s WHERE id = %(id)s"""
        data = {'id': meal_id, 'data1': name, 'data2': description, 'data3': price}
        return Database.update(query, data)

    @classmethod
    def find_by_id(cls, meal_id):
        """Method finds an order by it's menu_id"""
        query = """SELECT * FROM meals WHERE id = %(id)s"""
        data = {'id': meal_id}
        return Database.find_one(query, data)

    @classmethod
    def find_by_name(cls, name):
        """Method finds an order by it's menu_id"""
        query = """SELECT * FROM meals WHERE name = %(name)s"""
        data = {'name': name}
        return Database.find_one(query, data)

    @staticmethod
    def delete(meal_id):
        """Method deletes a single menu by it's id"""
        query = """DELETE FROM meals WHERE id = %(id)s"""
        data = {'id': meal_id}
        return Database.remove_one(query, data)

    @staticmethod
    def delete_all():
        """Method deletes all data from the menu table"""
        query = """TRUNCATE TABLE meals"""
        Database.remove_all(query)

    @staticmethod
    def find_one_entry():
        """Method finds if one entry exists"""
        query = """SELECT * FROM meals LIMIT 1"""
        return Database.check_entry(query)

    @staticmethod
    def validate_meal_details(name, description, price):
        """
        This method validates the menu input details
        :param price:
        :param description:
        :param name:
        :return: True if valid, or False otherwise
        """
        if name and description:
            if not Utils.name_checker(name):
                raise MealError.BadRequest('Invalid name!')

        else:
            if not name:
                raise MealError.BadRequest('Please provide name!')
            if not description:
                raise MealError.BadRequest('Please provide some description!')
            if not price:
                raise MealError.BadRequest('Please provide the price of meal!')
        return True
