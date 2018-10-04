"""
Create database tables
"""
import os

import psycopg2
import psycopg2.extras
from flask import current_app

from app.api.v2.models.user import User


def dbconn():
    """
    Connection to the database
    :return: db connector
    """
    try:
        connection = psycopg2.connect(current_app.config['DATABASE_URL'])
        return connection
    except psycopg2.DatabaseError as e:
        return {'error': str(e)}


def test_dbconn():
    """
    Connection to the database
    :return: db connector
    """
    try:
        connection = psycopg2.connect(current_app.config['DATABASE_TEST_URL'])
        return connection
    except psycopg2.DatabaseError as e:
        return {'error': str(e)}


def create_tables():
    """
    Create tables for the database
    """
    queries = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(80) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            date_registered TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::date NOT NULL,
            user_role VARCHAR(80)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS blacklist (
            id SERIAL PRIMARY KEY NOT NULL,
            tokens CHARACTER VARYING(255) NOT NULL,
            blacklisted_date TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::date NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS menu (
            id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(80) NOT NULL,
            description VARCHAR(1000) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS meals (
            id SERIAL PRIMARY KEY NOT NULL,
            menu_id INTEGER NULL REFERENCES menu(id) ON DELETE CASCADE,
            name VARCHAR(80) NOT NULL,
            description VARCHAR(200) NOT NULL,
            price INT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY NOT NULL,
            order_id INTEGER NOT NULL,
            meal_id INTEGER NULL REFERENCES meals(id) ON DELETE CASCADE,
            user_id INTEGER NULL REFERENCES users(id) ON DELETE CASCADE,
            date_created TIMESTAMP WITH TIME ZONE,
            name VARCHAR(80) NOT NULL,
            quantity INT NOT NULL,
            price INT NOT NULL,
            meal_total INT NOT NULL,
            status VARCHAR(80) DEFAULT 'New'
            -- sub_total INT NOT NULL,
            -- total INT NOT NULL
        )
        """
    )

    try:
        connection = dbconn()
        cursor = connection.cursor()
        # create tables
        for query in queries:
            cursor.execute(query)

        cursor.close()
        connection.commit()
        connection.close()

        admin = User(username=os.getenv('ADMIN_USERNAME'),
                     email=os.getenv('ADMIN_EMAIL'),
                     password=os.getenv('ADMIN_PASSWORD'))
        admin.save()
    except psycopg2.DatabaseError as e:
        print(e)


def drop_tables():
    db_test_url = os.getenv('DATABASE_TEST_URL')
    connection = psycopg2.connect(db_test_url)
    cursor = connection.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    blacklist = "DROP TABLE IF EXISTS blacklist CASCADE"
    orders = "DROP TABLE IF EXISTS orders CASCADE"
    meals = "DROP TABLE IF EXISTS meals CASCADE"
    menu = "DROP TABLE IF EXISTS menu CASCADE"

    queries = [users, blacklist, orders, meals, menu]
    try:
        for query in queries:
            cursor.execute(query)

        connection.commit()
    except psycopg2.DatabaseError as e:
        print(e)
