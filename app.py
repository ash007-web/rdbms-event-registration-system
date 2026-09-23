from database import get_connection
import mysql.connector

# ==================================================
# EVENT MANAGEMENT FUNCTIONS
# ==================================================

def add_event():
    print("\n--- Add Event ---")
    name = input("Enter event name: ")
    event_date = input("Enter event date (YYYY-MM-DD): ")
    venue = input("Enter venue: ")
    description = input("Enter description: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO events (event_name, event_date, venue, description) VALUES (%s, %s, %s, %s)"
            values = (name, event_date, venue, description)
            cursor.execute(query, values)
            connection.commit()
            print("Event added successfully!")
        except Exception as e:
            print("Error adding event:", e)
        finally:
            cursor.close()
            connection.close()

def view_events():
    print("\n==================================================")
    print("EVENTS")
    print("==================================================")
    
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
            
            # Simple terminal table
            print(f"{'ID':<5} | {'Name':<30} | {'Date':<12} | {'Venue':<20}")
            print("-" * 75)
            for row in rows:
                print(f"{row[0]:<5} | {row[1]:<30} | {str(row[2]):<12} | {row[3]:<20}")
        except Exception as e:
            print("Error viewing events:", e)
        finally:
            cursor.close()
            connection.close()

def update_event():
    print("\n--- Update Event ---")
    event_id = input("Enter Event ID to update: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if event exists
            cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
            event = cursor.fetchone()
            
            if not event:
                print("Event not found!")
                return
                
            name = input(f"Enter new event name ({event[1]}): ") or event[1]
            event_date = input(f"Enter new event date ({event[2]}): ") or event[2]
            venue = input(f"Enter new venue ({event[3]}): ") or event[3]
            description = input(f"Enter new description ({event[4]}): ") or event[4]

            query = "UPDATE events SET event_name=%s, event_date=%s, venue=%s, description=%s WHERE event_id=%s"
            values = (name, event_date, venue, description, event_id)
            cursor.execute(query, values)
            connection.commit()
            print("Event updated successfully!")
        except Exception as e:
            print("Error updating event:", e)
        finally:
            cursor.close()
            connection.close()

def delete_event():
    print("\n--- Delete Event ---")
    event_id = input("Enter Event ID to delete: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if event exists
            cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
            event = cursor.fetchone()
            
            if not event:
                print("Event not found!")
                return
                
            # Show the event before deleting
            print("\nEvent Details:")
            print(f"Name: {event[1]}")
            print(f"Date: {event[2]}")
            
            confirm = input("Are you sure you want to delete this event? (y/n): ")
            if confirm.lower() == 'y':
                query = "DELETE FROM events WHERE event_id=%s"
                cursor.execute(query, (event_id,))
                connection.commit()
                print("Event deleted successfully!")
            else:
                print("Deletion cancelled.")
                
        except mysql.connector.Error as err:
            if err.errno == 1451: # Foreign key constraint error
                print("\nError: Cannot delete this event because there are participants registered for it.")
                print("You must delete the related registrations first.")
            else:
                print("Database error:", err)
        except Exception as e:
            print("Error deleting event:", e)
        finally:
            cursor.close()
            connection.close()

# ==================================================
# PARTICIPANT MANAGEMENT FUNCTIONS
# ==================================================

def add_participant():
    print("\n--- Add Participant ---")
    name = input("Enter participant name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO participants (name, email, phone) VALUES (%s, %s, %s)"
            values = (name, email, phone)
            cursor.execute(query, values)
            connection.commit()
            print("Participant added successfully!")
        except Exception as e:
            print("Error adding participant:", e)
        finally:
            cursor.close()
            connection.close()

def view_participants():
    print("\n==================================================")
    print("PARTICIPANTS")
    print("==================================================")
    
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM participants")
            rows = cursor.fetchall()
            
            print(f"{'ID':<5} | {'Name':<25} | {'Email':<30} | {'Phone':<15}")
            print("-" * 85)
            for row in rows:
                print(f"{row[0]:<5} | {row[1]:<25} | {row[2]:<30} | {row[3]:<15}")
        except Exception as e:
            print("Error viewing participants:", e)
        finally:
            cursor.close()
            connection.close()

def update_participant():
    print("\n--- Update Participant ---")
    participant_id = input("Enter Participant ID to update: ")
    
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if participant exists
            cursor.execute("SELECT * FROM participants WHERE participant_id = %s", (participant_id,))
            participant = cursor.fetchone()
            
            if not participant:
                print("Participant not found!")
                return
                
            name = input(f"Enter new name ({participant[1]}): ") or participant[1]
            email = input(f"Enter new email ({participant[2]}): ") or participant[2]
            phone = input(f"Enter new phone number ({participant[3]}): ") or participant[3]

            query = "UPDATE participants SET name=%s, email=%s, phone=%s WHERE participant_id=%s"
            values = (name, email, phone, participant_id)
            cursor.execute(query, values)
            connection.commit()
            print("Participant updated successfully!")
        except Exception as e:
            print("Error updating participant:", e)
        finally:
            cursor.close()
            connection.close()

def delete_participant():
    print("\n--- Delete Participant ---")
    participant_id = input("Enter Participant ID to delete: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if participant exists
            cursor.execute("SELECT * FROM participants WHERE participant_id = %s", (participant_id,))
            participant = cursor.fetchone()
            
            if not participant:
                print("Participant not found!")
                return
                
            print("\nParticipant Details:")
            print(f"Name: {participant[1]}")
            print(f"Email: {participant[2]}")
            
            confirm = input("Are you sure you want to delete this participant? (y/n): ")
            if confirm.lower() == 'y':
                query = "DELETE FROM participants WHERE participant_id=%s"
                cursor.execute(query, (participant_id,))
                connection.commit()
                print("Participant deleted successfully!")
            else:
                print("Deletion cancelled.")
                
        except mysql.connector.Error as err:
            if err.errno == 1451:
                print("\nError: Cannot delete this participant because they are registered for an event.")
                print("You must delete the related registrations first.")
            else:
                print("Database error:", err)
        except Exception as e:
            print("Error deleting participant:", e)
        finally:
            cursor.close()
            connection.close()

# ==================================================
# REGISTRATION MANAGEMENT FUNCTIONS
# ==================================================

def add_registration():
    print("\n--- Add Registration ---")
    participant_id = input("Enter Participant ID: ")
    
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Verify participant exists
            cursor.execute("SELECT name FROM participants WHERE participant_id = %s", (participant_id,))
            participant = cursor.fetchone()
            if not participant:
                print("Participant not found!")
                return
                
            event_id = input("Enter Event ID: ")
            # Verify event exists
            cursor.execute("SELECT event_name FROM events WHERE event_id = %s", (event_id,))
            event = cursor.fetchone()
            if not event:
                print("Event not found!")
                return
                
            # Prevent duplicate registrations
            cursor.execute("SELECT * FROM registrations WHERE participant_id = %s AND event_id = %s", (participant_id, event_id))
            if cursor.fetchone():
                print(f"Error: Participant '{participant[0]}' is already registered for event '{event[0]}'.")
                return

            registration_date = input("Enter Registration Date (YYYY-MM-DD): ")
            status = input("Enter Status (Registered, Confirmed, Attended, Cancelled): ")

            query = "INSERT INTO registrations (event_id, participant_id, registration_date, status) VALUES (%s, %s, %s, %s)"
            values = (event_id, participant_id, registration_date, status)
            cursor.execute(query, values)
            connection.commit()
            print("Registration added successfully!")
            
        except Exception as e:
            print("Error adding registration:", e)
        finally:
            cursor.close()
            connection.close()

def view_registrations():
    print("\n==================================================")
    print("ALL REGISTRATIONS")
    print("==================================================")
    
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            SELECT 
                r.registration_id,
                p.name, 
                e.event_name,
                e.event_date,
                r.registration_date,
                r.status
            FROM registrations r
            JOIN participants p ON r.participant_id = p.participant_id
            JOIN events e ON r.event_id = e.event_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            print(f"{'Reg ID':<7} | {'Participant Name':<25} | {'Event Name':<30} | {'Event Date':<12} | {'Reg Date':<12} | {'Status'}")
            print("-" * 115)
            for row in rows:
                print(f"{row[0]:<7} | {row[1]:<25} | {row[2]:<30} | {str(row[3]):<12} | {str(row[4]):<12} | {row[5]}")
        except Exception as e:
            print("Error viewing registrations:", e)
        finally:
            cursor.close()
            connection.close()

def update_registration():
    print("\n--- Update Registration ---")
    reg_id = input("Enter Registration ID to update: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if registration exists
            cursor.execute("SELECT * FROM registrations WHERE registration_id = %s", (reg_id,))
            reg = cursor.fetchone()
            
            if not reg:
                print("Registration not found!")
                return
                
            print(f"Current Participant ID: {reg[2]}, Event ID: {reg[1]}")
            participant_id = input(f"Enter new Participant ID (press Enter to keep {reg[2]}): ") or reg[2]
            
            # Validate participant
            cursor.execute("SELECT * FROM participants WHERE participant_id = %s", (participant_id,))
            if not cursor.fetchone():
                print("Participant not found!")
                return
                
            event_id = input(f"Enter new Event ID (press Enter to keep {reg[1]}): ") or reg[1]
            
            # Validate event
            cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
            if not cursor.fetchone():
                print("Event not found!")
                return
                
            registration_date = input(f"Enter new Registration Date ({reg[3]}): ") or reg[3]
            status = input(f"Enter new status ({reg[4]}): ") or reg[4]

            query = "UPDATE registrations SET participant_id=%s, event_id=%s, registration_date=%s, status=%s WHERE registration_id=%s"
            values = (participant_id, event_id, registration_date, status, reg_id)
            cursor.execute(query, values)
            connection.commit()
            print("Registration updated successfully!")
        except Exception as e:
            print("Error updating registration:", e)
        finally:
            cursor.close()
            connection.close()

def delete_registration():
    print("\n--- Delete Registration ---")
    reg_id = input("Enter Registration ID to delete: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Check if exists and get details
            query = """
            SELECT r.registration_id, p.name, e.event_name 
            FROM registrations r
            JOIN participants p ON r.participant_id = p.participant_id
            JOIN events e ON r.event_id = e.event_id
            WHERE r.registration_id = %s
            """
            cursor.execute(query, (reg_id,))
            reg = cursor.fetchone()
            
            if not reg:
                print("Registration not found!")
                return
                
            print("\nRegistration Details:")
            print(f"Participant: {reg[1]}")
            print(f"Event: {reg[2]}")
            
            confirm = input("Are you sure you want to delete this registration? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM registrations WHERE registration_id=%s", (reg_id,))
                connection.commit()
                print("Registration deleted successfully!")
            else:
                print("Deletion cancelled.")
        except Exception as e:
            print("Error deleting registration:", e)
        finally:
            cursor.close()
            connection.close()

# ==================================================
# EVENT-WISE REGISTRATIONS
# ==================================================

def view_event_registrations():
    print("\n--- View Registrations For An Event ---")
    event_id = input("Enter Event ID: ")

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            cursor.execute("SELECT event_name, event_date, venue FROM events WHERE event_id=%s", (event_id,))
            event = cursor.fetchone()
            
            if not event:
                print("Event not found!")
                return
                
            print(f"\nEvent Name: {event[0]}")
            print(f"Event Date: {event[1]}")
            print(f"Venue: {event[2]}\n")
            
            query = """
            SELECT 
                r.registration_id,
                p.name, 
                p.email,
                p.phone,
                r.registration_date,
                r.status
            FROM registrations r
            JOIN participants p ON r.participant_id = p.participant_id
            WHERE r.event_id = %s;
            """
            cursor.execute(query, (event_id,))
            rows = cursor.fetchall()
            
            print(f"{'Reg ID':<7} | {'Participant Name':<25} | {'Email':<30} | {'Phone':<15} | {'Reg Date':<12} | {'Status'}")
            print("-" * 115)
            
            for row in rows:
                print(f"{row[0]:<7} | {row[1]:<25} | {row[2]:<30} | {row[3]:<15} | {str(row[4]):<12} | {row[5]}")
                
            print(f"\nTotal Registrations: {len(rows)}")
            
        except Exception as e:
            print("Error viewing event registrations:", e)
        finally:
            cursor.close()
            connection.close()

# ==================================================
# MENUS
# ==================================================

def manage_events_menu():
    while True:
        print("\nEVENT MANAGEMENT:")
        print("1. Add Event")
        print("2. View Events")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. Back")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_event()
        elif choice == '2':
            view_events()
        elif choice == '3':
            update_event()
        elif choice == '4':
            delete_event()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_participants_menu():
    while True:
        print("\nPARTICIPANT MANAGEMENT:")
        print("1. Add Participant")
        print("2. View Participants")
        print("3. Update Participant")
        print("4. Delete Participant")
        print("5. Back")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_participant()
        elif choice == '2':
            view_participants()
        elif choice == '3':
            update_participant()
        elif choice == '4':
            delete_participant()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_registrations_menu():
    while True:
        print("\nREGISTRATION MANAGEMENT:")
        print("1. Add Registration")
        print("2. View Registrations")
        print("3. Update Registration")
        print("4. Delete Registration")
        print("5. Back")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_registration()
        elif choice == '2':
            view_registrations()
        elif choice == '3':
            update_registration()
        elif choice == '4':
            delete_registration()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    while True:
        print("\n========================================")
        print("       EVENT REGISTRATION SYSTEM")
        print("========================================")
        print("1. Event Management")
        print("2. Participant Management")
        print("3. Registration Management")
        print("4. View Event Registrations")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            manage_events_menu()
        elif choice == '2':
            manage_participants_menu()
        elif choice == '3':
            manage_registrations_menu()
        elif choice == '4':
            view_event_registrations()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
