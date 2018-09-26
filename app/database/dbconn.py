"""
Database configuration
"""
import psycopg2
from flask import current_app


def dbconn():
    """
    Connection to the database
    :return: db connector
    """
    try:
        connection = psycopg2.connect(current_app.config['DATABASE'])

        return connection
    except psycopg2.DatabaseError as e:
        return {'error': str(e)}
