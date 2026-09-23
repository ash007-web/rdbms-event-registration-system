# Event Registration System (CLI Version)

A simple, terminal-based Python application that uses MySQL for managing events, participants, and registrations.

This project is specifically designed for educational purposes to demonstrate how Python interacts with a Relational Database Management System (RDBMS) using `mysql-connector-python`. It focuses on keeping the code extremely simple and easy to understand for beginners.

## Objective
The primary goal is to teach:
1. Connecting Python to a MySQL database.
2. Performing CRUD (Create, Read, Update, Delete) operations.
3. Using SQL queries within Python scripts.
4. Implementing SQL JOINs to combine data from multiple tables.

## Technologies
- **Python 3.x**
- **MySQL Server**
- **mysql-connector-python** library

## Requirements
Before running the application, you must have:
- MySQL Server installed and running.
- Python 3 installed.
- The `mysql-connector-python` library.

---

## Setup Instructions

### 1. Database Setup
First, you need to create the database and tables, and insert the sample data.

1. Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or the MySQL command line).
2. Copy the contents of `database.sql` or import the file directly into your MySQL server.
3. This will create a database named `event_registration_db`, along with three tables (`events`, `participants`, `registrations`), and populate them with sample data.

### 2. Install Python Dependency
Open your terminal or command prompt in this project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Configure MySQL Password
Open `database.py` in your text editor.
Find the `get_connection()` function:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", # IMPORTANT: Change this!
    database="event_registration_db"
)
```
Update the `password` field with your actual MySQL root password.

### 4. Running the Application

## Running the Project

Double-click:

`run.bat`

The CLI application will open automatically.

No manual Python command is required.

---

## Application Structure

The application consists of a main menu that allows you to manage different entities:

1. **Manage Events**: Add, view, update, and delete events.
2. **Manage Participants**: Add, view, update, and delete participants.
3. **Manage Registrations**: Register participants for events and manage their status.
4. **View Event-wise Registrations**: Uses a SQL JOIN to show all participants registered for a specific event.

---

## Beginner Teaching Section: How Python Connects to MySQL

This section explains the core concepts used in this project. When demonstrating this in class, you can map these steps directly to the code in `app.py`.

### The 6 Steps of Database Interaction

Every time we interact with the database, we follow this sequence:

1. **Import mysql.connector** (Done at the top of the file)
2. **Connect to MySQL**
3. **Create Cursor**
4. **Execute SQL**
5. **Fetch Results / Commit Changes**
6. **Close Connection**

Here is exactly how it looks in the code:

#### Connection
We call our helper function from `database.py` to get the connection object:
```python
connection = get_connection()
```

#### Cursor
The cursor is the object that actually sends instructions to MySQL:
```python
cursor = connection.cursor()
```

#### Execute SQL
We write our SQL query and tell the cursor to execute it:
```python
query = "SELECT * FROM events"
cursor.execute(query)
```

#### Read Results (For SELECT)
If we asked for data, we fetch it and loop through it:
```python
rows = cursor.fetchall()
for row in rows:
    print(row)
```

#### Save Changes (For INSERT, UPDATE, DELETE)
If we modified data, we MUST commit the changes to save them permanently:
```python
connection.commit()
```

---

## CRUD OPERATIONS

CREATE
Python executes INSERT and commits the transaction.

READ
Python executes SELECT and retrieves records using fetchone() or fetchall().

UPDATE
Python executes UPDATE and commits the transaction.

DELETE
Python executes DELETE and commits the transaction.

Also briefly explaining how Python -> mysql.connector -> MySQL Database works:
Python uses the `mysql.connector` module as a bridge. We call `connect()` to establish a network connection to the MySQL Database. Once connected, we create a `cursor` object, which allows us to send SQL queries to the database using `cursor.execute()`. For reading data, we fetch the results back into Python. For modifying data (Create, Update, Delete), we must call `connection.commit()` so that MySQL permanently saves the changes.

---

## Understanding SQL JOINs

In a relational database, data is split across multiple tables. For example, the `registrations` table only knows the `event_id` and `participant_id`, but it doesn't know the actual names.

To display meaningful data to the user, we use a SQL JOIN to combine these tables.

Look at the `view_registrations()` function:
```sql
SELECT 
    registrations.registration_id,
    participants.name, 
    participants.email, 
    events.event_name
FROM registrations
JOIN participants ON registrations.participant_id = participants.participant_id
JOIN events ON registrations.event_id = events.event_id;
```
This tells MySQL: "Get the registration, find the participant with the matching ID, find the event with the matching ID, and return all their names together."

---

## Common Errors
- **Database connection error: Access denied for user...**: Your MySQL password in `database.py` is incorrect.
- **Table doesn't exist**: You forgot to run the `database.sql` script to create the tables.
- **ModuleNotFoundError: No module named 'mysql'**: You forgot to install the dependency using `pip install -r requirements.txt`.
