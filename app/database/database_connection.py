import psycopg2
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
        # For the connection not to be left in an inconsistent state
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
