from .database_connection import DatabaseConnection


class Database:

    @staticmethod
    def insert(query, data):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            row = cursor.fetchone()[0]
            cursor.close()
        return int(row)

    @staticmethod
    def remove_all(query):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            cursor.close()

    @staticmethod
    def remove_one(query, data):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            cursor.close()
        return True

    @staticmethod
    def find_one(query, data):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            row = cursor.fetchone()
            cursor.close()
        return row

    @staticmethod
    def find_all(query):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
        return rows

    @staticmethod
    def update(query, data):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            cursor.close()
        return True

    @staticmethod
    def check_entry(query):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            cursor.close()
        return rows
