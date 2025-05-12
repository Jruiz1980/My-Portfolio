# Simple CLI Agenda with Firebase Firestore

This is a simple command-line interface (CLI) application for managing agenda events. It uses Google's Firebase Firestore as a backend to store and retrieve event data.

## Video Tutorial
[Agenda](https://youtube.com)

## Features

*   **Schedule Event:** Add new events to your agenda.
*   **Attend Next Event:** View the oldest pending event and mark it as completed.
*   **View All Events:** Display a list of all events (both pending and completed), ordered by creation date.
*   **Persistent Storage:** Events are stored in a Firebase Firestore database.

## Prerequisites

*   Python 3.x
*   A Google Firebase project.
*   Firebase Admin Python SDK.
*   Google Cloud Firestore client library.

## Setup

1.  **Clone the repository (optional):**
   If you have this project in a Git repository, clone it:
    ```bash
    git clone <your-repository-url>
    cd <repository-folder```

2.  **Install Dependencies:**
    Install the required Python libraries:
    ```bash
    pip install firebase-admin google-cloud-firestore```

3.  **Firebase Setup:**
    *   Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project (or use an existing one).
    *   In your Firebase project settings, go to "Service accounts".
    *   Click on "Generate new private key" and download the JSON file.
    *   **Important:** Rename this downloaded JSON file (e.g., `your-service-account-key.json`) and place it in a `config` directory within your project (e.g., `./config/your-service-account-key.json`).
    *   **Update the script:**
        Open `agenda.py` and modify the following constants:
        *   `PATH_TO_FIREBASE_KEY`: Update this to the actual path of your downloaded service account key JSON file.
            ```python
            PATH_TO_FIREBASE_KEY = './config/your-service-account-key.json' # <--- UPDATE THIS!
            ```
        *   `PROJECT_ID`: Update this with your Firebase Project ID (found in your Firebase project settings).
            ```python
            PROJECT_ID = 'your-firebase-project-id' # <--- UPDATE THIS!
            ```
        *   `COLLECTION_NAME` (optional): You can change the name of the Firestore collection if desired. The default is `agenda_events`.

4.  **Enable Firestore:**
    In the Firebase Console, navigate to "Firestore Database" (or "Cloud Firestore") and create a database. Choose a region and start in "test mode" for initial development (remember to set up proper security rules for production).

## Usage

To run the application, navigate to the directory containing `agenda.py` in your terminal and execute:

```bash
  python agenda.py
```

You will be presented with a menu to interact with your agenda:

```
                                     My Calendar
1.- Schedule event
2.- Attend next event
3.- View all events
0.- Quit
Select an option:
```

Follow the on-screen prompts to manage your events.

## How it Works

*   The script connects to your Firebase Firestore database using the Admin SDK.
*   Events are stored as documents in a collection (default: `agenda_events`).
*   Each event document typically includes:
    *   `description`: The text description of the event.
    *   `created_at`: A server timestamp indicating when the event was scheduled.
    *   `status`: The current status of the event (e.g., `pending`, `completed`).

## Configuration Constants in `agenda.py`

*   `PATH_TO_FIREBASE_KEY`: Path to your Firebase service account key JSON file.
*   `PROJECT_ID`: Your Firebase project ID.
*   `COLLECTION_NAME`: The name of the Firestore collection where events are stored.

