from datetime import datetime


class Orders:
    table = 'orders'

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date_created = datetime.now()
        self.status = 'Pending'

    def __repr__(self):
        return f'<Order {self.name}'

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

    @staticmethod
    def list_all_orders():
        pass

    @classmethod
    def find_by_id(cls, order_id):
        pass

    @staticmethod
    def delete(order_id):
        pass

    @staticmethod
    def delete_all():
        pass
