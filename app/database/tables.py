"""
Create database tables
"""
import os

import psycopg2
import psycopg2.extras
from flask import current_app


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


def create_tables():
    """
    Create tables for the database
    """
    queries = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY NOT NULL,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(80) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            date_registered TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::date NOT NULL,
            user_role VARCHAR(80) DEFAULT 'User'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS blacklist (
            token_id INT NOT NULL,
            tokens CHARACTER VARYING(200) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(80) NOT NULL,
            quantity INT NOT NULL,
            price INT NOT NULL,
            date_created TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::date NOT NULL,
            status VARCHAR(80) DEFAULT 'New'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS meals (
            meal_id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(80) NOT NULL,
            description VARCHAR(200) NOT NULL,
            price INT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS menu (
            menu_id SERIAL PRIMARY KEY NOT NULL,
            name VARCHAR(80) NOT NULL,
            description VARCHAR(1000) NOT NULL
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
