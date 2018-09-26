"""
Create database tables
"""
import psycopg2

queries = (
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY NOT NULL,
        username VARCHAR(80) NOT NULL UNIQUE,
        email VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        date_created TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::date NOT NULL,
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


def create_tables(db_url):
    """
    Create tables for the database
    """
    try:
        connection = psycopg2.connect(db_url)

        cursor = connection.cursor()
        # create tables
        for command in queries:
            cursor.execute(command)

        cursor.close()

        connection.commit()

        connection.close()
    except psycopg2.DatabaseError as error:
        print(error)
