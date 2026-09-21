"""
database.py — MySQL Connection Layer
Event Registration System | RDBMS Lab Module 5

This module is responsible for:
  1. Reading database credentials from the .env file
  2. Creating a MySQL connection
  3. Providing a reusable execute_query() helper

All Flask routes import and call execute_query() from this file.
The connection is opened and closed for every query (simple, safe, beginner-friendly).
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load credentials from the .env file into environment variables
load_dotenv()


def get_connection():
    """
    Creates and returns a MySQL database connection.

    Reads the following environment variables (set in .env):
      DB_HOST     — usually 'localhost'
      DB_USER     — usually 'root'
      DB_PASSWORD — your MySQL password
      DB_NAME     — 'event_registration_db'

    Returns:
        A mysql.connector connection object, or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "event_registration_db")
        )
        return connection

    except Error as e:
        # Print a clear error message — helps students debug connection issues
        print(f"\n[DATABASE ERROR] Could not connect to MySQL.")
        print(f"  Reason  : {e}")
        print(f"  Check   : Is MySQL running? Are the credentials in .env correct?\n")
        return None


def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Executes a SQL query against the MySQL database.

    This function is the central point through which Flask routes
    communicate with MySQL. It demonstrates the Python → MySQL workflow:

        Flask route → execute_query() → MySQL → result → Flask template

    Parameters:
        query     (str)   : SQL query string. Use %s as placeholder for values.
        params    (tuple) : Values that replace %s placeholders (prevents SQL injection).
        fetch     (bool)  : Set True to retrieve ALL matching rows (for SELECT).
        fetch_one (bool)  : Set True to retrieve ONLY THE FIRST matching row.

    Returns:
        list of dict — if fetch=True  (each row is a dictionary)
        dict         — if fetch_one=True
        int          — last inserted row ID (for INSERT queries)
        None         — if an error occurs or connection fails

    SQL operations supported:
        SELECT  → use fetch=True or fetch_one=True
        INSERT  → returns last inserted ID
        UPDATE  → commits the change
        DELETE  → commits the change
    """
    connection = get_connection()

    # If connection failed, return None (Flask route will handle the None gracefully)
    if not connection:
        return None

    # dictionary=True makes cursor return rows as dicts instead of tuples
    # This lets templates access columns by name: {{ row.event_name }}
    cursor = connection.cursor(dictionary=True)
    result = None

    try:
        # Execute the query — params are substituted safely by the connector
        # This is parameterized query execution (prevents SQL injection)
        cursor.execute(query, params or ())

        if fetch:
            # Retrieve ALL matching rows → returns a list of dicts
            result = cursor.fetchall()

        elif fetch_one:
            # Retrieve ONLY the first matching row → returns a single dict
            result = cursor.fetchone()

        else:
            # For INSERT, UPDATE, DELETE — commit the transaction
            connection.commit()
            # lastrowid is useful after INSERT (returns the new record's ID)
            result = cursor.lastrowid

    except Error as e:
        # Log the error, roll back any uncommitted changes, and re-raise
        print(f"[QUERY ERROR] {e}")
        print(f"  Query : {query}")
        print(f"  Params: {params}")
        connection.rollback()
        raise e  # re-raise so the Flask route can catch it and show an error message

    finally:
        # Always close the cursor and connection — even if an error occurred
        cursor.close()
        connection.close()

    return result
