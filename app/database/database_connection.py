import psycopg2
import psycopg2.extras

from flask import current_app


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(current_app.config['DATABASE_URL'])
            return self.connection
        except psycopg2.DatabaseError as e:
            return {'error': str(e)}

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        For the connection not to be left in an inconsistent state
        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception traceback
        """
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
