import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# We import only FieldFilter, as we will use strings for the order direction
from google.cloud.firestore_v1.base_query import FieldFilter # Keep this if you need it for where
# from google.cloud.firestore_v1.base_query import Order # <--- WE REMOVE THIS!
import datetime # To handle timestamps

PATH_TO_FIREBASE_KEY = './config/agenda-6ad6b-firebase-adminsdk-fbsvc-0ae3e78192.json' # <--- UPDATE THIS!

PROJECT_ID = 'agenda-6ad6b'

COLLECTION_NAME = 'agenda_events'

# --- Initialize Firebase Admin SDK ---
def initialize_firebase():
    """Initializes the Firebase app with the service credentials."""
    try:
        # Check if the app has already been initialized to avoid errors
        if not firebase_admin._apps:
            # Use the downloaded credentials
            cred = credentials.Certificate(PATH_TO_FIREBASE_KEY)
            firebase_admin.initialize_app(cred, {'projectId': PROJECT_ID})

        # Return the Firestore client
        return firestore.client()

    except Exception as e:
        print(f"Error initializing Firebase or connecting to Firestore: {e}")
        print("Ensure that the path to your service account key file is correct.")
        print("Also verify that the file exists and that the credentials are valid.")
        return None # Return None if initialization fails

# --- Menu Options ---
SCHEDULE = 1
ATTEND = 2
VIEW_ALL = 3 # We add an option to view all events (pending and attended)
QUIT = 0

# --- Agenda Functions with Firestore ---

def display_menu():
    """Displays the main menu."""
    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console (works on Windows and others)
    print(f'''                                      My Calendar
{SCHEDULE}.- Schedule event
{ATTEND}.- Attend next event
{VIEW_ALL}.- View all events
{QUIT}.- Quit''')

def schedule_event(db):
    """Schedules a new event by saving it to Firestore."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         Schedule Event')
    event_description = input('Event description: ')

    if not event_description:
        print("Description cannot be empty. Event not scheduled.")
        return

    try:
        # Create a dictionary with the event data
        nuevo_evento = {
            'description': event_description,
            'created_at': firestore.SERVER_TIMESTAMP, # Use a server timestamp
            'status': 'pending' # We add a status field
        }

        # Get a reference to the events collection
        events_ref = db.collection(COLLECTION_NAME)

        # Add the document to the collection. Firestore will generate an ID automatically.
        update_time, doc_ref = events_ref.add(nuevo_evento)

        print(f"Event '{event_description}' scheduled successfully with ID: {doc_ref.id}")

    except Exception as e:
        print(f"Error scheduling event: {e}")


def attend_event(db):
    """
    Searches for the oldest pending event in Firestore (by creation date),
    displays it, and ASKS FOR CONFIRMATION to mark it as 'completed'.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         Attend Event')

    try:
        # Get a reference to the events collection
        events_ref = db.collection(COLLECTION_NAME)

        # Query events with 'pending' status, ordered by creation date (ascending)
        # and limit to 1 to get the oldest.
        query = events_ref.where(filter=FieldFilter("status", "==", "pending")).order_by("created_at", direction='ASCENDING').limit(1) # <-- We use the string 'ASCENDING'

        # Get the query results
        docs = list(query.stream())

        if not docs:
            print('No pending events to attend.')
        else:
            # The first document in the list is the oldest pending event
            event_doc = docs[0]
            event_data = event_doc.to_dict()
            event_id = event_doc.id
            description = event_data.get("description", "No description")

            print(f'Next pending event (ID: {event_id}):')
            print(f'  Description: {description}')

            # --- ADD CONFIRMATION STEP HERE! ---
            confirm = input("Mark this event as completed? (yes/no): ").lower().strip()

            if confirm == 'yes':
                # Mark the event as 'completed' in Firestore
                event_doc.reference.update({'status': 'completed'})
                print("\nEvent marked as completed.") # Add a newline for better readability
            elif confirm == 'no':
                print("\nEvent was NOT marked as completed.") # Add a newline
            else:
                print("\nInvalid response. Event was NOT marked as completed.") # Add a newline

    except Exception as e:
        print(f"Error attending event: {e}")

def view_all_events(db):
    """Displays all events in Firestore, ordered by creation date."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         All Events')

    try:
        # Get a reference to the events collection
        events_ref = db.collection(COLLECTION_NAME)

        # Query all events, ordered by creation date (ascending)
        # --- CORRECTION HERE ---
        query = events_ref.order_by("created_at", direction='ASCENDING') # <-- We use the string 'ASCENDING'

        # Get the query results
        docs = list(query.stream())

        if not docs:
            print('No events found in the calendar.')
        else:
            print("-" * 40)
            for doc in docs:
                event_data = doc.to_dict()
                event_id = doc.id
                description = event_data.get("description", "No description")
                status = event_data.get("status", "unknown")
                created_at = event_data.get("created_at") # This will be a Timestamp object

                # Format the creation date if available
                date_str = "N/A"
                # Firestore SERVER_TIMESTAMP returns a datetime object
                if isinstance(created_at, datetime.datetime):
                    date_str = created_at.strftime('%Y-%m-%d %H:%M:%S') # We add seconds for more precision

                print(f"ID: {event_id}")
                print(f"  Description: {description}")
                print(f"  Status: {status}")
                print(f"  Created At: {date_str}")
                print("-" * 40)
                print("") # Blank line between events for better readability


    except Exception as e:
        print(f"Error viewing events: {e}")


# --- Main Function ---
def main():
    """Main function of the agenda application."""

    # Initialize Firebase and get the Firestore client
    db = initialize_firebase()

    # If initialization fails, exit
    if db is None:
        print("\nExiting due to Firebase initialization failure.")
        return

    forward = True
    while forward:
        display_menu()

        try:
            opc = int(input('Select an option: '))
        except ValueError:
            print("Invalid input. Please enter a number.")
            input('Press ENTER to continue...')
            continue # Go back to the beginning of the loop

        # IMPORTANT: We clear the screen *after* getting the option
        # and *before* executing the function, so that the function's output is visible.
        os.system('cls' if os.name == 'nt' else 'clear')

        if opc == SCHEDULE:
            schedule_event(db) # Pass the Firestore client to the function
            # Pause for the user to read the result before clearing
            input('Press ENTER to continue...') # <-- Add pause here
        elif opc == ATTEND:
            attend_event(db) # Pass the Firestore client to the function
            # Pause for the user to read the result before clearing
            input('Press ENTER to continue...') # <-- Add pause here
        elif opc == VIEW_ALL: # New option
            view_all_events(db) # Pass the Firestore client to the function
            # --- ADD THE PAUSE HERE! ---
            input('Press ENTER to continue...') # <-- THIS IS THE MISSING LINE
        elif opc == QUIT:
            forward = False
            # Do not ask for ENTER after exiting
            print('Good-Bye')
        else:
            print('Invalid option...')
            # Only ask for ENTER if the option was not Exit
            input('Press ENTER to continue...')

if __name__ == '__main__':
    main()
