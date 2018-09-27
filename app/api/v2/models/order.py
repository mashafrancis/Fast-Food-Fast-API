from datetime import datetime

from app.database.tables import dbconn


class Orders:
    table = 'orders'

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

    def add_order(self):
        """Adds user to the list"""
        order = Orders(self.name,
                       self.quantity,
                       self.price)
        pass

    def save(self):
        connection = dbconn()
        cursor = connection.cursor()

        data = [self.name, self.quantity, self.price, 'now']
        query = """INSERT INTO orders (name, quantity, price, date_created) 
                    VALUES (%s, %s, %s, %s) RETURNING order_id"""
        cursor.execute(query, data)

        order_id = cursor.fetchone()[0]
        cursor.close()
        connection.commit()
        connection.close()

        return int(order_id)

    @staticmethod
    def list_all_orders():
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM orders""")

        orders = cursor.fetchall()
        cursor.close()
        connection.close()

        return orders

    @classmethod
    def find_by_id(cls, order_id):
        pass

    @staticmethod
    def delete(order_id):
        pass

    @staticmethod
    def delete_all():
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("""TRUNCATE TABLE orders""")

        cursor.close()
        connection.close()

    @staticmethod
    def find_one_entry():
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM orders LIMIT 1""")

        rows = cursor.fetchone()
        cursor.close()
        connection.close()

        return rows

