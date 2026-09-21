# Event Registration System
### RDBMS Lab Module 5 — Python + Flask + MySQL

A complete, database-driven **Event Registration System** that demonstrates full
CRUD operations against a MySQL relational database using Python Flask.

---

## Project Objective

To build a small database-driven application using Python Flask connected to a MySQL RDBMS,
and to perform complete **Create, Read, Update, and Delete** (CRUD) operations through a web interface.

---

## Problem Statement

Managing event registrations manually is error-prone and inefficient.
This application provides a simple web-based system to:
- Record and manage college events
- Register participants for events
- Track registration statuses
- Demonstrate Python ↔ MySQL database connectivity

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Main programming language |
| Flask | Web framework — routes, logic, templates |
| MySQL | Relational Database Management System |
| mysql-connector-python | Python to MySQL connection driver |
| python-dotenv | Load database credentials from .env file |
| Jinja2 (via Flask) | HTML templating |
| HTML5 | Template structure |
| CSS3 | Styling |
| JavaScript | Delete confirmation, auto-dismiss alerts |

---

## System Requirements

- Python 3.8 or higher
- MySQL 8.0 or higher (or XAMPP/WAMP with MySQL)
- A web browser (Chrome, Firefox, or Edge)

---

## Running the Application

### First-time setup
To run the system for the very first time, follow these one-time steps:

1. **Install Prerequisites**: Ensure Python 3.8+ and MySQL (or XAMPP/WAMP) are installed on your system.
2. **Import Database**: Import `database.sql` into MySQL Workbench or via terminal (`mysql -u root -p < database.sql`) to create the database and tables.
3. **Configure Database Credentials**: Copy `.env.example` to `.env` and set your `DB_PASSWORD` and other variables if necessary.
4. **Create Virtual Environment**: Open a terminal in the project folder and run `python -m venv venv`.
5. **Install Requirements**: Activate the environment (`venv\Scripts\activate`) and run `python -m pip install -r requirements.txt`.
6. **Launch the System**: Double-click `run.bat`.

### Every subsequent run

After the initial setup is complete, launching the application is extremely simple:

1. Make sure MySQL is running.
2. Double-click `run.bat`.
3. Chrome opens automatically and the application runs.

You do not need to remember any terminal commands. To stop the server, simply double-click `stop.bat` or close the "EventReg Server" window that opens.

---

## Project Structure

```
ERS/
│
├── app.py                   ← Flask app: all routes and logic
├── database.py              ← MySQL connection and query executor
├── database.sql             ← Database schema + sample data
├── requirements.txt         ← Python dependencies
├── .env                     ← Your database credentials (do NOT share)
├── .env.example             ← Credential template for other students
├── README.md                ← This file
├── PROJECT_DOCUMENTATION.md ← Full academic documentation
│
├── templates/               ← Jinja2 HTML templates (rendered by Flask)
│   ├── base.html            ← Common layout: navbar, flash messages, footer
│   ├── dashboard.html       ← Home page with summary counts
│   ├── events.html          ← Events list (READ)
│   ├── event_form.html      ← Add/Edit event form (CREATE/UPDATE)
│   ├── participants.html    ← Participants list (READ)
│   ├── participant_form.html← Add/Edit participant form (CREATE/UPDATE)
│   ├── registrations.html   ← Registrations list with JOIN (READ)
│   └── registration_form.html ← Register/Edit form (CREATE/UPDATE)
│
└── static/
    └── style.css            ← CSS styling for all pages
```

---

## Database Structure

### Tables and Relationships

```
events (event_id PK, event_name, event_date, venue, description)
    │
    │  FK: registrations.event_id → events.event_id
    ▼
registrations (registration_id PK, event_id FK, participant_id FK,
               registration_date, status)
    ▲
    │  FK: registrations.participant_id → participants.participant_id
    │
participants (participant_id PK, name, email UNIQUE, phone)
```

### Constraints Used
- `PRIMARY KEY` — unique identifier for every table
- `FOREIGN KEY` — links registrations to events and participants
- `NOT NULL` — required fields cannot be empty
- `UNIQUE` — prevents duplicate emails and duplicate registrations
- `ENUM` — status field only allows: Confirmed, Pending, Cancelled

---

## CRUD Operations — Where to Find Them

| Operation | Entity | Flask Route | SQL Type |
|---|---|---|---|
| **CREATE** | Event | `POST /events/add` | `INSERT INTO events` |
| **CREATE** | Participant | `POST /participants/add` | `INSERT INTO participants` |
| **CREATE** | Registration | `POST /registrations/add` | `INSERT INTO registrations` |
| **READ** | Events | `GET /events` | `SELECT * FROM events` |
| **READ** | Participants | `GET /participants` | `SELECT * FROM participants` |
| **READ** | Registrations | `GET /registrations` | `SELECT ... JOIN ...` |
| **UPDATE** | Event | `POST /events/edit/<id>` | `UPDATE events SET ...` |
| **UPDATE** | Participant | `POST /participants/edit/<id>` | `UPDATE participants SET ...` |
| **UPDATE** | Registration | `POST /registrations/edit/<id>` | `UPDATE registrations SET ...` |
| **DELETE** | Event | `POST /events/delete/<id>` | `DELETE FROM events` |
| **DELETE** | Participant | `POST /participants/delete/<id>` | `DELETE FROM participants` |
| **DELETE** | Registration | `POST /registrations/delete/<id>` | `DELETE FROM registrations` |

---

## SQL JOIN Explanation

The **Registrations** page uses a 3-table JOIN:

```sql
SELECT
    r.registration_id,
    p.name       AS participant_name,
    e.event_name,
    r.registration_date,
    r.status
FROM   registrations r
JOIN   participants  p ON r.participant_id = p.participant_id
JOIN   events        e ON r.event_id       = e.event_id
ORDER  BY r.registration_date DESC
```

**Why is this needed?**
The `registrations` table only stores `event_id` and `participant_id` (foreign keys).
To display readable names instead of ID numbers, we JOIN the three tables together.
This is the core advantage of a relational database.

---

## Testing

| Test | Steps | Expected Result |
|---|---|---|
| Create Event | Events → Add Event → Fill form → Submit | New event appears in the table |
| Create Participant | Participants → Add Participant → Fill form → Submit | New participant appears |
| Register Participant | Registrations → Register → Select participant & event → Submit | Registration appears in the list |
| Update Event | Events → Edit (✏️) → Change values → Submit | Updated values saved in MySQL |
| Update Registration Status | Registrations → Edit → Change status → Submit | Status updated in MySQL |
| Delete Registration | Registrations → Delete (🗑️) → Confirm | Record removed from database |
| Duplicate Email | Add participant with existing email | Error: "A participant with this email already exists" |
| Delete Event with Registrations | Try to delete event that has registrations | Error message — deletion blocked |
| Duplicate Registration | Register same participant for same event twice | Error: "This participant is already registered" |

---

## Troubleshooting

### "Can't connect to MySQL server"
- Make sure MySQL is running
- **Windows:** Search "Services" → start `MySQL80`
- **XAMPP:** Start Apache and MySQL in XAMPP Control Panel

### "Access denied for user 'root'@'localhost'"
- Your password in `.env` is wrong
- Verify with: `mysql -u root -p` in a terminal

### "Unknown database 'event_registration_db'"
- You haven't run `database.sql` yet
- Run: `mysql -u root -p < database.sql`

### "ModuleNotFoundError: No module named 'flask'"
- Virtual environment not activated, or dependencies not installed
- Run: `python -m pip install -r requirements.txt`

### Port 5000 already in use
- Change the port at the bottom of `app.py`:
  `app.run(debug=True, port=5001)`
- Or on Mac: disable AirPlay Receiver in System Preferences

---

## Lab Demonstration Flow

1. Open http://127.0.0.1:5000 → Dashboard
2. Show MySQL Workbench with the three tables
3. Show `database.py` — the Python ↔ MySQL connection
4. Go to **Events** → Add a new event (**CREATE**)
5. Go to **Participants** → Add a new participant (**CREATE**)
6. Go to **Registrations** → Register that participant (**CREATE**)
7. View the Registration list — observe the JOIN query result (**READ**)
8. Edit the registration status → change to "Pending" (**UPDATE**)
9. Show the updated record in MySQL Workbench
10. Delete the registration (**DELETE**)
11. Confirm the record is removed from the database
