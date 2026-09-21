# Event Registration System
## PROJECT DOCUMENTATION
### RDBMS Lab Module 5 — Python Flask + MySQL

---

## 1. Introduction

This document is the complete academic documentation for the **Event Registration System**,
developed as an RDBMS Laboratory project (Module 5).

The project demonstrates how a **Python Flask web application** connects to and operates a
**MySQL relational database**, performing all four fundamental database operations:
**Create, Read, Update, and Delete (CRUD)**.

---

## 2. Objective

1. Design and implement a normalized relational database in MySQL.
2. Develop a Python Flask web application.
3. Connect Python to MySQL using `mysql-connector-python`.
4. Implement complete CRUD operations through Flask routes and Jinja2 templates.
5. Apply primary keys, foreign keys, constraints, and SQL JOINs in a real application.
6. Demonstrate the complete flow: **Browser → Flask → MySQL → Flask → Browser**.

---

## 3. Problem Statement

Educational institutions frequently organize workshops, seminars, and sports events.
Managing these events and participant registrations manually (paper or spreadsheets)
leads to data duplication, errors, and inefficiency.

**Solution:** A database-driven web application built with Python Flask and MySQL that
provides a centralized system for managing events, participants, and registrations through
a clean web interface.

---

## 4. Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Application programming language |
| Flask | 3.0.3 | Web framework (routes, templates, logic) |
| MySQL | 8.0+ | Relational Database Management System |
| mysql-connector-python | 8.4.0 | Python to MySQL database driver |
| python-dotenv | 1.0.1 | Environment variable management (.env) |
| Jinja2 | via Flask | HTML template engine |
| HTML5 | — | Template structure |
| CSS3 | — | Page styling |
| JavaScript | — | Client-side: delete confirm, auto-dismiss |

---

## 5. System Requirements

### Hardware
- Any modern computer (Windows, macOS, Linux)
- Minimum 2 GB RAM recommended

### Software
- Python 3.8 or higher
- MySQL 8.0 or higher
- Web browser (Chrome, Firefox, Edge)
- pip (Python package manager)

---

## 6. Database Design

### Database Name
`event_registration_db`

### Design Principles
- **Normalization:** Each table stores data for exactly one entity
- **Referential Integrity:** Foreign keys ensure registrations always point to real events and participants
- **No Redundancy:** Participant and event names are stored once; registrations reference them by ID
- **Constraints:** NOT NULL, UNIQUE, and ENUM prevent invalid data

---

## 7. ER Diagram Description

```
┌──────────────────┐         ┌───────────────────────────┐         ┌────────────────────┐
│     EVENTS       │         │       REGISTRATIONS        │         │    PARTICIPANTS     │
├──────────────────┤         ├───────────────────────────┤         ├────────────────────┤
│ PK event_id      │◄────────│ FK event_id               │─────────►│ PK participant_id  │
│    event_name    │  1   M  │ FK participant_id          │  M   1  │    name            │
│    event_date    │         │ PK registration_id         │         │    email (UNIQUE)  │
│    venue         │         │    registration_date       │         │    phone           │
│    description   │         │    status (ENUM)           │         └────────────────────┘
└──────────────────┘         └───────────────────────────┘

One EVENT     has MANY REGISTRATIONS   (1 to M)
One PARTICIPANT has MANY REGISTRATIONS (1 to M)
EVENTS and PARTICIPANTS have a Many-to-Many relationship
  → implemented through the REGISTRATIONS junction table
```

---

## 8. Table Structures

### Table: `events`

```sql
CREATE TABLE events (
    event_id      INT AUTO_INCREMENT PRIMARY KEY,
    event_name    VARCHAR(150) NOT NULL,
    event_date    DATE         NOT NULL,
    venue         VARCHAR(200) NOT NULL,
    description   TEXT
);
```

| Column | Type | Constraint | Description |
|---|---|---|---|
| event_id | INT | PK, AUTO_INCREMENT | Unique identifier |
| event_name | VARCHAR(150) | NOT NULL | Name of the event |
| event_date | DATE | NOT NULL | Date the event takes place |
| venue | VARCHAR(200) | NOT NULL | Location of the event |
| description | TEXT | Optional | Details about the event |

---

### Table: `participants`

```sql
CREATE TABLE participants (
    participant_id INT          AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    phone          VARCHAR(15)  NOT NULL
);
```

| Column | Type | Constraint | Description |
|---|---|---|---|
| participant_id | INT | PK, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Full name |
| email | VARCHAR(150) | NOT NULL, UNIQUE | Email (must be unique) |
| phone | VARCHAR(15) | NOT NULL | Contact number |

---

### Table: `registrations`

```sql
CREATE TABLE registrations (
    registration_id   INT  AUTO_INCREMENT PRIMARY KEY,
    event_id          INT  NOT NULL,
    participant_id    INT  NOT NULL,
    registration_date DATE NOT NULL,
    status            ENUM('Confirmed','Pending','Cancelled') NOT NULL DEFAULT 'Confirmed',
    FOREIGN KEY (event_id)       REFERENCES events(event_id),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
    UNIQUE (event_id, participant_id)
);
```

| Column | Type | Constraint | Description |
|---|---|---|---|
| registration_id | INT | PK, AUTO_INCREMENT | Unique identifier |
| event_id | INT | FK → events.event_id | Links to the event |
| participant_id | INT | FK → participants.participant_id | Links to the participant |
| registration_date | DATE | NOT NULL | Date of registration |
| status | ENUM | NOT NULL, DEFAULT 'Confirmed' | Current registration status |

---

## 9. Primary and Foreign Keys

### Primary Keys
| Table | Primary Key |
|---|---|
| events | event_id |
| participants | participant_id |
| registrations | registration_id |

### Foreign Keys
| Table | Column | References |
|---|---|---|
| registrations | event_id | events(event_id) |
| registrations | participant_id | participants(participant_id) |

### Unique Constraints
| Table | Column(s) | Purpose |
|---|---|---|
| participants | email | No two participants share an email |
| registrations | (event_id, participant_id) | No duplicate registrations for same event |

---

## 10. Flask Architecture and Database Connectivity

### Application Flow

```
  Browser
     │
     ▼
  Flask Route (app.py)
     │  — reads form data (POST) or URL params (GET)
     │  — calls execute_query()
     ▼
  execute_query() (database.py)
     │  — calls get_connection()
     │  — executes parameterized SQL query
     │  — commits / fetches result
     ▼
  MySQL (event_registration_db)
     │  — tables: events, participants, registrations
     ▼
  Result (rows as Python dictionaries)
     │
     ▼
  Flask passes data to Jinja2 template
     │  — render_template("page.html", data=result)
     ▼
  HTML page displayed in browser
```

### Database Connection Module (database.py)

```python
# Step 1: Read credentials from .env
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Step 2: Execute a parameterized query
cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))

# Step 3: Fetch the result
result = cursor.fetchall()   # for SELECT (multiple rows)
result = cursor.fetchone()   # for SELECT (single row)
connection.commit()          # for INSERT / UPDATE / DELETE
```

**Parameterized Queries:** Using `%s` placeholders (never string concatenation)
prevents **SQL injection attacks**. The mysql-connector library safely substitutes values.

---

## 11. CRUD Implementation

### CREATE (INSERT)

```python
# Flask reads form data → calls execute_query() with INSERT
sql = "INSERT INTO events (event_name, event_date, venue, description) VALUES (%s, %s, %s, %s)"
execute_query(sql, (name, event_date, venue, description))
```

### READ (SELECT)

```python
# Simple SELECT
rows = execute_query("SELECT * FROM events ORDER BY event_date", fetch=True)

# SELECT with JOIN (3 tables)
sql = """
    SELECT r.registration_id, p.name AS participant_name,
           e.event_name, r.registration_date, r.status
    FROM   registrations r
    JOIN   participants  p ON r.participant_id = p.participant_id
    JOIN   events        e ON r.event_id       = e.event_id
"""
rows = execute_query(sql, fetch=True)
```

### UPDATE

```python
sql = "UPDATE events SET event_name=%s, event_date=%s, venue=%s, description=%s WHERE event_id=%s"
execute_query(sql, (name, event_date, venue, description, event_id))
```

### DELETE

```python
execute_query("DELETE FROM registrations WHERE registration_id = %s", (registration_id,))
```

---

## 12. SQL Queries Used

| Query Type | Example SQL |
|---|---|
| INSERT | `INSERT INTO events (event_name, event_date, venue, description) VALUES (%s, %s, %s, %s)` |
| SELECT (all) | `SELECT * FROM events ORDER BY event_date` |
| SELECT (one) | `SELECT * FROM events WHERE event_id = %s` |
| SELECT (JOIN) | `SELECT r.*, p.name, e.event_name FROM registrations r JOIN participants p ... JOIN events e ...` |
| SELECT COUNT | `SELECT COUNT(*) AS cnt FROM events` |
| UPDATE | `UPDATE events SET event_name=%s, event_date=%s WHERE event_id=%s` |
| DELETE | `DELETE FROM registrations WHERE registration_id = %s` |

---

## 13. Sample Data

### Events (5 rows)
| event_id | event_name | event_date | venue |
|---|---|---|---|
| 1 | Python Programming Workshop | 2026-10-05 | Computer Lab 1, Block A |
| 2 | Web Development Bootcamp | 2026-10-12 | Seminar Hall, Block B |
| 3 | AI & Machine Learning Seminar | 2026-10-20 | Auditorium, Main Block |
| 4 | College Sports Meet 2026 | 2026-11-02 | College Grounds |
| 5 | Cloud Computing Workshop | 2026-11-15 | Computer Lab 2, Block A |

### Participants (10 rows — first 5 shown)
| participant_id | name | email | phone |
|---|---|---|---|
| 1 | Aarav Sharma | aarav.sharma@college.edu | 9876543210 |
| 2 | Priya Mehta | priya.mehta@college.edu | 9876543211 |
| 3 | Rohan Verma | rohan.verma@college.edu | 9876543212 |
| ... | ... | ... | ... |

### Registrations (10 rows — sample)
| registration_id | event_id | participant_id | status |
|---|---|---|---|
| 1 | 1 | 1 | Confirmed |
| 2 | 1 | 2 | Confirmed |
| 3 | 1 | 3 | Pending |
| ... | ... | ... | ... |

---

## 14. Testing

| Test Case | Action | Expected Result | SQL Triggered |
|---|---|---|---|
| TC01 | Run `database.sql` | Database and tables created with sample data | CREATE DATABASE, CREATE TABLE, INSERT |
| TC02 | Open http://127.0.0.1:5000 | Dashboard shows counts: 5, 10, 10 | SELECT COUNT(*) × 3 |
| TC03 | Add new event | Event appears in events table | INSERT INTO events |
| TC04 | Add new participant | Participant appears in table | INSERT INTO participants |
| TC05 | Register participant for event | Registration appears in list | INSERT INTO registrations |
| TC06 | View registrations page | Table shows names (not IDs) | SELECT … JOIN … JOIN |
| TC07 | Edit event details | Updated values saved | UPDATE events SET … |
| TC08 | Change registration status | Status updated to Pending/Cancelled | UPDATE registrations SET status=… |
| TC09 | Delete a registration | Record removed | DELETE FROM registrations |
| TC10 | Try to delete event with registrations | Error message shown, record kept | (blocked by Python check before DELETE) |
| TC11 | Add duplicate email | Error: email already exists | INSERT fails — UNIQUE constraint |
| TC12 | Register duplicate (same event+participant) | Error: already registered | INSERT fails — UNIQUE constraint |
| TC13 | Submit empty form | Validation errors shown | No SQL executed |
| TC14 | Restart Flask server | Application reconnects to MySQL | get_connection() called again |

---

## 15. Screenshots

*(Add screenshots during your lab demonstration — suggested placeholders:)*

1. `[Screenshot 1]` — Dashboard with summary cards (5 events, 10 participants, 10 registrations)
2. `[Screenshot 2]` — Events list page
3. `[Screenshot 3]` — Add Event form with data entered
4. `[Screenshot 4]` — Success flash message after adding event
5. `[Screenshot 5]` — Participants list page
6. `[Screenshot 6]` — Registrations page (showing JOIN result with names)
7. `[Screenshot 7]` — Edit Registration form with status dropdown
8. `[Screenshot 8]` — Delete confirmation dialog
9. `[Screenshot 9]` — Error message when deleting event with registrations
10. `[Screenshot 10]` — MySQL Workbench showing the three tables

---

## 16. Results

The Event Registration System successfully demonstrated:

- ✅ Python Flask application connected to MySQL RDBMS
- ✅ All CRUD operations (INSERT, SELECT, UPDATE, DELETE) working correctly
- ✅ SQL JOIN query used to display registration data from three tables
- ✅ Primary keys, foreign keys, UNIQUE constraints, and ENUM enforced at database level
- ✅ Referential integrity preserved (cannot delete event/participant with active registrations)
- ✅ Duplicate prevention: duplicate emails and duplicate registrations rejected
- ✅ Parameterized queries used throughout (SQL injection prevention)
- ✅ Flask flash messages display success and error feedback
- ✅ Dashboard counts fetched live from MySQL (not hard-coded)
- ✅ Sample data works immediately after running `database.sql`

---

## 17. Conclusion

This project successfully implements a **Python Flask + MySQL Event Registration System**
for the RDBMS Laboratory Module 5.

Key concepts applied:
- **Database normalization** — three separate tables, no data redundancy
- **Relational integrity** — foreign keys linking registrations to events and participants
- **SQL CRUD** — all four operations (INSERT, SELECT, UPDATE, DELETE) demonstrated
- **SQL JOIN** — combining data from three related tables
- **Parameterized SQL** — security best practice against SQL injection
- **Flask routing** — handling GET and POST HTTP methods
- **Jinja2 templating** — rendering dynamic database content in HTML
- **Error handling** — database exceptions caught and displayed as user-friendly messages

The application is small enough for 19 students to divide responsibilities
(database design, routes, templates, testing, documentation) while clearly
demonstrating the complete **Python Flask ↔ RDBMS** workflow.

---

*RDBMS Lab Module 5 | Python 3 + Flask + MySQL + Jinja2 + HTML5 + CSS3*
