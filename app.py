"""
app.py — Main Flask Application
Event Registration System | RDBMS Lab Module 5

This file contains ALL Flask routes for the application.
Every route follows this pattern:

    Browser Request
         ↓
    Flask Route  (app.py)
         ↓
    execute_query()  (database.py)
         ↓
    MySQL  (event_registration_db)
         ↓
    Result → Jinja2 Template → HTML Response

Routes:
  GET  /                            → Dashboard
  GET  /events                      → List all events
  GET  /events/add                  → Add event form
  POST /events/add                  → Submit new event
  GET  /events/edit/<id>            → Edit event form (pre-filled)
  POST /events/edit/<id>            → Submit updated event
  POST /events/delete/<id>          → Delete event
  GET  /participants                → List all participants
  GET  /participants/add            → Add participant form
  POST /participants/add            → Submit new participant
  GET  /participants/edit/<id>      → Edit participant form
  POST /participants/edit/<id>      → Submit updated participant
  POST /participants/delete/<id>    → Delete participant
  GET  /registrations               → List all registrations (JOIN)
  GET  /registrations/add           → Register participant form
  POST /registrations/add           → Submit new registration
  GET  /registrations/edit/<id>     → Edit registration form
  POST /registrations/edit/<id>     → Submit updated registration
  POST /registrations/delete/<id>   → Delete registration
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import Error
import os
from dotenv import load_dotenv
from database import execute_query

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Flask Application Setup
# ─────────────────────────────────────────────────────────────
app = Flask(__name__)
# Secret key is required for Flask flash messages (session handling)
app.secret_key = os.getenv("SECRET_KEY", "ers-lab-module5-secret")


# =============================================================
#  DASHBOARD  —  GET /
# =============================================================

@app.route("/")
def dashboard():
    """
    Home page.
    Displays summary counts: Total Events, Participants, Registrations.
    Numbers are fetched LIVE from MySQL — not hard-coded.

    SQL used: SELECT COUNT(*) — three times.
    """

    # READ: Count total events from MySQL
    total_events = execute_query(
        "SELECT COUNT(*) AS cnt FROM events",
        fetch_one=True
    )

    # READ: Count total participants from MySQL
    total_participants = execute_query(
        "SELECT COUNT(*) AS cnt FROM participants",
        fetch_one=True
    )

    # READ: Count total registrations from MySQL
    total_registrations = execute_query(
        "SELECT COUNT(*) AS cnt FROM registrations",
        fetch_one=True
    )

    # Build a simple dictionary to pass to the template
    counts = {
        "events":        total_events["cnt"]        if total_events        else 0,
        "participants":  total_participants["cnt"]  if total_participants  else 0,
        "registrations": total_registrations["cnt"] if total_registrations else 0,
    }

    # READ: Fetch recent registrations for the dashboard preview
    # This query uses JOIN to combine data from three tables
    recent_sql = """
        SELECT r.registration_id,
               p.name       AS participant_name,
               e.event_name,
               r.registration_date,
               r.status
        FROM   registrations r
        JOIN   participants  p ON r.participant_id = p.participant_id
        JOIN   events        e ON r.event_id       = e.event_id
        ORDER  BY r.registration_date DESC
        LIMIT  5
    """
    recent_registrations = execute_query(recent_sql, fetch=True) or []

    # Render the dashboard template, passing data as variables
    return render_template(
        "dashboard.html",
        counts=counts,
        recent_registrations=recent_registrations
    )


# =============================================================
#  EVENTS — CRUD
#  Table: events
# =============================================================

@app.route("/events")
def events():
    """
    READ: Retrieve and display all events from MySQL, including registration counts.
    SQL: SELECT e.*, COUNT(r.registration_id) FROM events LEFT JOIN registrations GROUP BY e.event_id
    """
    sql = """
        SELECT e.*, COUNT(r.registration_id) AS reg_count
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id
        ORDER BY e.event_date
    """
    rows = execute_query(sql, fetch=True) or []
    return render_template("events.html", events=rows)

@app.route("/events/<int:event_id>/registrations")
def event_registrations(event_id):
    """
    READ: Display participants registered for a specific event.
    """
    event = execute_query(
        "SELECT * FROM events WHERE event_id = %s",
        (event_id,), fetch_one=True
    )
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("events"))

    sql = """
        SELECT
            r.registration_id,
            p.participant_id,
            p.name          AS participant_name,
            p.email,
            p.phone,
            r.registration_date,
            r.status,
            r.event_id
        FROM participants p
        JOIN registrations r ON p.participant_id = r.participant_id
        WHERE r.event_id = %s
        ORDER BY r.registration_date DESC
    """
    registrations = execute_query(sql, (event_id,), fetch=True) or []
    
    events_list = execute_query("SELECT event_id, event_name FROM events ORDER BY event_name", fetch=True) or []

    return render_template("event_registrations.html", event=event, registrations=registrations, all_events=events_list)


@app.route("/events/add", methods=["GET", "POST"])
def add_event():
    """
    CREATE: Display the add-event form (GET) and insert a new event (POST).
    SQL: INSERT INTO events (event_name, event_date, venue, description) VALUES (...)
    """
    if request.method == "POST":

        # Read form values submitted by the user
        name        = request.form.get("event_name", "").strip()
        event_date  = request.form.get("event_date", "").strip()
        venue       = request.form.get("venue", "").strip()
        description = request.form.get("description", "").strip()

        # --- Server-side Validation ---
        errors = []
        if not name:       errors.append("Event name is required.")
        if not event_date: errors.append("Event date is required.")
        if not venue:      errors.append("Venue is required.")

        if errors:
            # Flash each error message and re-show the form with entered data
            for err in errors:
                flash(err, "error")
            return render_template("event_form.html", action="add",
                                   form_data=request.form)

        # --- INSERT query (parameterized — safe from SQL injection) ---
        sql = """
            INSERT INTO events (event_name, event_date, venue, description)
            VALUES (%s, %s, %s, %s)
        """
        try:
            execute_query(sql, (name, event_date, venue, description))
            flash(f'Event "{name}" was added successfully!', "success")
            return redirect(url_for("events"))
        except Error as e:
            flash(f"Database error: {e}", "error")
            return render_template("event_form.html", action="add",
                                   form_data=request.form)

    # GET request: show empty form
    return render_template("event_form.html", action="add", form_data={})


@app.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    """
    UPDATE: Display an edit form pre-filled with the event's current data (GET),
    and save the changes to MySQL (POST).
    SQL: UPDATE events SET event_name=..., ... WHERE event_id=...
    """

    # Fetch the current record to pre-fill the form
    event = execute_query(
        "SELECT * FROM events WHERE event_id = %s",
        (event_id,),
        fetch_one=True
    )
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("events"))

    if request.method == "POST":

        name        = request.form.get("event_name", "").strip()
        event_date  = request.form.get("event_date", "").strip()
        venue       = request.form.get("venue", "").strip()
        description = request.form.get("description", "").strip()

        errors = []
        if not name:       errors.append("Event name is required.")
        if not event_date: errors.append("Event date is required.")
        if not venue:      errors.append("Venue is required.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("event_form.html", action="edit",
                                   form_data=request.form, event_id=event_id)

        # --- UPDATE query ---
        sql = """
            UPDATE events
            SET event_name=%s, event_date=%s, venue=%s, description=%s
            WHERE event_id=%s
        """
        try:
            execute_query(sql, (name, event_date, venue, description, event_id))
            flash(f'Event "{name}" was updated successfully!', "success")
            return redirect(url_for("events"))
        except Error as e:
            flash(f"Database error: {e}", "error")

    # GET request: show form pre-filled with existing event data
    return render_template("event_form.html", action="edit",
                           form_data=event, event_id=event_id)


@app.route("/events/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    """
    DELETE: Remove an event from MySQL.
    Safety: Blocked if the event has existing registrations (foreign key protection).
    SQL: DELETE FROM events WHERE event_id = ...
    """

    # Safety check — count registrations linked to this event
    reg_count = execute_query(
        "SELECT COUNT(*) AS cnt FROM registrations WHERE event_id = %s",
        (event_id,),
        fetch_one=True
    )
    if reg_count and reg_count["cnt"] > 0:
        flash(
            "Cannot delete this event — it has existing registrations. "
            "Please delete those registrations first.",
            "error"
        )
        return redirect(url_for("events"))

    # Fetch the event name for the success message
    event = execute_query(
        "SELECT event_name FROM events WHERE event_id = %s",
        (event_id,),
        fetch_one=True
    )
    try:
        # --- DELETE query ---
        execute_query("DELETE FROM events WHERE event_id = %s", (event_id,))
        name = event["event_name"] if event else str(event_id)
        flash(f'Event "{name}" was deleted successfully.', "success")
    except Error as e:
        flash(f"Database error: {e}", "error")

    return redirect(url_for("events"))


# =============================================================
#  PARTICIPANTS — CRUD
#  Table: participants
# =============================================================

@app.route("/participants")
def participants():
    """
    READ: Retrieve and display all participants from MySQL.
    SQL: SELECT * FROM participants ORDER BY name
    """
    rows = execute_query(
        "SELECT * FROM participants ORDER BY name",
        fetch=True
    ) or []
    return render_template("participants.html", participants=rows)


@app.route("/participants/add", methods=["GET", "POST"])
def add_participant():
    """
    CREATE: Display the add-participant form (GET) and insert a new participant (POST).
    SQL: INSERT INTO participants (name, email, phone) VALUES (...)
    """
    if request.method == "POST":

        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        # --- Server-side Validation ---
        errors = []
        if not name:  errors.append("Name is required.")
        if not email: errors.append("Email address is required.")
        if not phone: errors.append("Phone number is required.")

        if email and "@" not in email:
            errors.append("Please enter a valid email address (must contain @).")

        digits = [c for c in phone if c.isdigit()]
        if phone and (len(digits) < 7 or len(digits) > 15):
            errors.append("Phone number must contain between 7 and 15 digits.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("participant_form.html", action="add",
                                   form_data=request.form)

        # --- INSERT query ---
        sql = """
            INSERT INTO participants (name, email, phone)
            VALUES (%s, %s, %s)
        """
        try:
            execute_query(sql, (name, email, phone))
            flash(f'Participant "{name}" was added successfully!', "success")
            return redirect(url_for("participants"))
        except Error as e:
            if "Duplicate entry" in str(e):
                flash("A participant with this email already exists.", "error")
            else:
                flash(f"Database error: {e}", "error")
            return render_template("participant_form.html", action="add",
                                   form_data=request.form)

    # GET request: show empty form
    return render_template("participant_form.html", action="add", form_data={})


@app.route("/participants/edit/<int:participant_id>", methods=["GET", "POST"])
def edit_participant(participant_id):
    """
    UPDATE: Show edit form pre-filled with participant data (GET),
    and save changes to MySQL (POST).
    SQL: UPDATE participants SET name=..., email=..., phone=... WHERE participant_id=...
    """

    participant = execute_query(
        "SELECT * FROM participants WHERE participant_id = %s",
        (participant_id,),
        fetch_one=True
    )
    if not participant:
        flash("Participant not found.", "error")
        return redirect(url_for("participants"))

    if request.method == "POST":

        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        errors = []
        if not name:  errors.append("Name is required.")
        if not email: errors.append("Email address is required.")
        if not phone: errors.append("Phone number is required.")
        if email and "@" not in email:
            errors.append("Please enter a valid email address.")
        digits = [c for c in phone if c.isdigit()]
        if phone and (len(digits) < 7 or len(digits) > 15):
            errors.append("Phone number must contain between 7 and 15 digits.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("participant_form.html", action="edit",
                                   form_data=request.form,
                                   participant_id=participant_id)

        # --- UPDATE query ---
        sql = """
            UPDATE participants
            SET name=%s, email=%s, phone=%s
            WHERE participant_id=%s
        """
        try:
            execute_query(sql, (name, email, phone, participant_id))
            flash(f'Participant "{name}" was updated successfully!', "success")
            return redirect(url_for("participants"))
        except Error as e:
            if "Duplicate entry" in str(e):
                flash("A participant with this email already exists.", "error")
            else:
                flash(f"Database error: {e}", "error")

    # GET request: show form pre-filled with participant data
    return render_template("participant_form.html", action="edit",
                           form_data=participant, participant_id=participant_id)


@app.route("/participants/delete/<int:participant_id>", methods=["POST"])
def delete_participant(participant_id):
    """
    DELETE: Remove a participant from MySQL.
    Safety: Blocked if participant has existing registrations.
    SQL: DELETE FROM participants WHERE participant_id = ...
    """

    reg_count = execute_query(
        "SELECT COUNT(*) AS cnt FROM registrations WHERE participant_id = %s",
        (participant_id,),
        fetch_one=True
    )
    if reg_count and reg_count["cnt"] > 0:
        flash(
            "Cannot delete this participant — they have existing registrations. "
            "Please delete those registrations first.",
            "error"
        )
        return redirect(url_for("participants"))

    p = execute_query(
        "SELECT name FROM participants WHERE participant_id = %s",
        (participant_id,),
        fetch_one=True
    )
    try:
        # --- DELETE query ---
        execute_query(
            "DELETE FROM participants WHERE participant_id = %s",
            (participant_id,)
        )
        name = p["name"] if p else str(participant_id)
        flash(f'Participant "{name}" was deleted successfully.', "success")
    except Error as e:
        flash(f"Database error: {e}", "error")

    return redirect(url_for("participants"))


# =============================================================
#  REGISTRATIONS — CRUD
#  Table: registrations (uses JOIN with events + participants)
# =============================================================

@app.route("/registrations")
def registrations():
    """
    READ: Display all registrations, with optional event filtering.
    """
    event_id_filter = request.args.get("event_id")
    
    sql = """
        SELECT
            r.registration_id,
            p.name          AS participant_name,
            e.event_name,
            e.event_date,
            e.venue,
            r.registration_date,
            r.status,
            r.event_id,
            r.participant_id
        FROM   registrations r
        JOIN   participants  p ON r.participant_id = p.participant_id
        JOIN   events        e ON r.event_id       = e.event_id
    """
    
    params = []
    if event_id_filter and event_id_filter.isdigit():
        sql += " WHERE r.event_id = %s"
        params.append(int(event_id_filter))
        
    sql += " ORDER BY r.registration_date DESC"
    
    rows = execute_query(sql, tuple(params) if params else None, fetch=True) or []
    
    events_list = execute_query("SELECT event_id, event_name FROM events ORDER BY event_name", fetch=True) or []
    
    return render_template("registrations.html", registrations=rows, events=events_list, selected_event=event_id_filter)


@app.route("/registrations/add", methods=["GET", "POST"])
def add_registration():
    """
    CREATE: Display the registration form with dropdowns (GET),
    and insert a new registration into MySQL (POST).
    SQL: INSERT INTO registrations (event_id, participant_id, ...) VALUES (...)
    """

    # Fetch dropdown data from MySQL (events and participants lists)
    events_list = execute_query(
        "SELECT event_id, event_name, event_date FROM events ORDER BY event_name",
        fetch=True
    ) or []
    participants_list = execute_query(
        "SELECT participant_id, name FROM participants ORDER BY name",
        fetch=True
    ) or []

    if request.method == "POST":

        event_id       = request.form.get("event_id", "").strip()
        participant_id = request.form.get("participant_id", "").strip()
        reg_date       = request.form.get("registration_date", "").strip()
        status         = request.form.get("status", "Registered").strip()

        errors = []
        if not event_id:       errors.append("Please select an event.")
        if not participant_id: errors.append("Please select a participant.")
        if not reg_date:       errors.append("Registration date is required.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("registration_form.html", action="add",
                                   events=events_list,
                                   participants=participants_list,
                                   form_data=request.form)

        # --- INSERT query ---
        sql = """
            INSERT INTO registrations (event_id, participant_id, registration_date, status)
            VALUES (%s, %s, %s, %s)
        """
        try:
            execute_query(sql, (event_id, participant_id, reg_date, status))
            flash("Registration was added successfully!", "success")
            return redirect(url_for("registrations"))
        except Error as e:
            if "Duplicate entry" in str(e):
                flash("This participant is already registered for that event.", "error")
            else:
                flash(f"Database error: {e}", "error")
            return render_template("registration_form.html", action="add",
                                   events=events_list,
                                   participants=participants_list,
                                   form_data=request.form)

    # GET request: show empty form with dropdowns
    preselected_event = request.args.get("event_id", "")
    return render_template("registration_form.html", action="add",
                           events=events_list,
                           participants=participants_list,
                           form_data={"event_id": preselected_event})


@app.route("/registrations/edit/<int:registration_id>", methods=["GET", "POST"])
def edit_registration(registration_id):
    """
    UPDATE: Show the edit form pre-filled with current registration data (GET),
    and save changes to MySQL (POST).
    SQL: UPDATE registrations SET ... WHERE registration_id=...
    """

    # Fetch the current registration record
    reg = execute_query(
        "SELECT * FROM registrations WHERE registration_id = %s",
        (registration_id,),
        fetch_one=True
    )
    if not reg:
        flash("Registration not found.", "error")
        return redirect(url_for("registrations"))

    # Dropdown data
    events_list = execute_query(
        "SELECT event_id, event_name, event_date FROM events ORDER BY event_name",
        fetch=True
    ) or []
    participants_list = execute_query(
        "SELECT participant_id, name FROM participants ORDER BY name",
        fetch=True
    ) or []

    if request.method == "POST":

        event_id       = request.form.get("event_id", "").strip()
        participant_id = request.form.get("participant_id", "").strip()
        reg_date       = request.form.get("registration_date", "").strip()
        status         = request.form.get("status", "Registered").strip()

        errors = []
        if not event_id:       errors.append("Please select an event.")
        if not participant_id: errors.append("Please select a participant.")
        if not reg_date:       errors.append("Registration date is required.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("registration_form.html", action="edit",
                                   events=events_list,
                                   participants=participants_list,
                                   form_data=request.form,
                                   registration_id=registration_id)

        # --- UPDATE query ---
        sql = """
            UPDATE registrations
            SET event_id=%s, participant_id=%s, registration_date=%s, status=%s
            WHERE registration_id=%s
        """
        try:
            execute_query(
                sql,
                (event_id, participant_id, reg_date, status, registration_id)
            )
            flash("Registration was updated successfully!", "success")
            return redirect(url_for("registrations"))
        except Error as e:
            if "Duplicate entry" in str(e):
                flash("This participant is already registered for that event.", "error")
            else:
                flash(f"Database error: {e}", "error")

    # GET request: show form pre-filled with existing registration data
    return render_template("registration_form.html", action="edit",
                           events=events_list,
                           participants=participants_list,
                           form_data=reg,
                           registration_id=registration_id)


@app.route("/registrations/delete/<int:registration_id>", methods=["POST"])
def delete_registration(registration_id):
    """
    DELETE: Remove a registration from MySQL.
    No foreign-key dependency issue here — registrations table is the leaf.
    SQL: DELETE FROM registrations WHERE registration_id = ...
    """
    try:
        execute_query(
            "DELETE FROM registrations WHERE registration_id = %s",
            (registration_id,)
        )
        flash("Registration was deleted successfully.", "success")
    except Error as e:
        flash(f"Database error: {e}", "error")

    return redirect(url_for("registrations"))


# =============================================================
#  Application Entry Point
# =============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Event Registration System — RDBMS Lab Module 5")
    print("  Flask + Python + MySQL")
    print("  Open your browser: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=False, host='127.0.0.1', port=5000)
