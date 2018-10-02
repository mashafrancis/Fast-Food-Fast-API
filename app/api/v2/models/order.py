from datetime import datetime

from app.database.database import Database


class Orders:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date_created = datetime.now()
        self.status = 'Pending'

    def __repr__(self):
        return repr(self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'date_created': self.date_created,
            'status': self.status
        }

    def save(self):
        """Method saves an order to the table"""

        data = [self.name, self.quantity, self.price, self.date_created]
        query = """INSERT INTO orders (name, quantity, price, date_created) 
                                VALUES (%s, %s, %s, %s) RETURNING id"""
        Database.insert(query, data)

    @staticmethod
    def list_all_orders():
        """Method lists all available orders in a table"""

        query = """SELECT * FROM orders"""
        return Database.find_all(query)

    @staticmethod
    def update_order(order_id, status):
        """Methods updates the status of an order"""

        query = """UPDATE orders SET status = %(data)s WHERE id = %(id)s"""
        data = {'id': order_id, 'data': status}
        return Database.update(query, data)

    @staticmethod
    def delete(order_id):
        """Method deletes a single order by it's id"""

        query = """DELETE FROM orders WHERE id = %(id)s"""
        data = {'id': order_id}
        return Database.remove_one(query, data)

    @staticmethod
    def delete_all():
        """Method deletes all data from the orders table"""

        query = """DELETE FROM orders"""
        Database.remove_all(query)

    @staticmethod
    def find_one_entry():
        """Method finds if one entry exists"""

        query = """SELECT * FROM orders LIMIT 1"""
        return Database.check_entry(query)

    @staticmethod
    def find_by_id(order_id):
        """Method finds an order by it's order_id"""

        query = """SELECT * FROM orders WHERE id = %(id)s"""
        data = {'id': order_id}
        return Database.find_one(query, data)
