import mysql.connector

def get_connection():
    """
    Establish a connection to the MySQL database.
    This function is used by all CRUD operations in the application.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", # IMPORTANT: Change this to your actual MySQL root password
            database="event_registration_db"
        )
        return connection
    except mysql.connector.Error as error:
        print("Database connection error:", error)
        return None
