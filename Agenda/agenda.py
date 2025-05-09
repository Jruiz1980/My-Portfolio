import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Importamos solo FieldFilter, ya que usaremos strings para la dirección de orden
from google.cloud.firestore_v1.base_query import FieldFilter # Mantén este si lo necesitas para where
# from google.cloud.firestore_v1.base_query import Order # <--- ¡QUITAMOS ESTO!
import datetime # Para manejar timestamps

PATH_TO_FIREBASE_KEY = './config/agenda-6ad6b-firebase-adminsdk-fbsvc-0ae3e78192.json' # <--- ¡ACTUALIZA ESTO!

PROJECT_ID = 'agenda-6ad6b'

COLLECTION_NAME = 'agenda_events'

# --- Inicializar Firebase Admin SDK ---
def initialize_firebase():
    """Inicializa la app de Firebase con las credenciales del servicio."""
    try:
        # Verifica si la app ya fue inicializada para evitar errores
        if not firebase_admin._apps:
            # Usar las credenciales descargadas
            cred = credentials.Certificate(PATH_TO_FIREBASE_KEY)
            firebase_admin.initialize_app(cred, {'projectId': PROJECT_ID})

        # Retorna el cliente de Firestore
        return firestore.client()

    except Exception as e:
        print(f"Error al inicializar Firebase o conectar con Firestore: {e}")
        print("Asegúrate de que la ruta a tu archivo de clave de servicio es correcta.")
        print("También verifica que el archivo existe y que las credenciales son válidas.")
        return None # Retorna None si falla la inicialización

# --- Opciones del Menú ---
SCHEDULE = 1
ATTEND = 2
VIEW_ALL = 3 # Agregamos una opción para ver todos los eventos (pendientes y atendidos)
QUIT = 0

# --- Funciones de la Agenda con Firestore ---

def display_menu():
    """Muestra el menú principal."""
    os.system('cls' if os.name == 'nt' else 'clear') # Limpia la consola (funciona en Windows y otros)
    print(f'''                                      My Calendar
{SCHEDULE}.- Schedule event
{ATTEND}.- Attend next event
{VIEW_ALL}.- View all events
{QUIT}.- Quit''')

def schedule_event(db):
    """Programa un nuevo evento guardándolo en Firestore."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         Schedule Event')
    event_description = input('Event description: ')

    if not event_description:
        print("Description cannot be empty. Event not scheduled.")
        return

    try:
        # Crear un diccionario con los datos del evento
        nuevo_evento = {
            'description': event_description,
            'created_at': firestore.SERVER_TIMESTAMP, # Usa un timestamp del servidor
            'status': 'pending' # Añadimos un campo de estado
        }

        # Obtener una referencia a la colección de eventos
        events_ref = db.collection(COLLECTION_NAME)

        # Añadir el documento a la colección. Firestore generará un ID automáticamente.
        update_time, doc_ref = events_ref.add(nuevo_evento)

        print(f"Event '{event_description}' scheduled successfully with ID: {doc_ref.id}")

    except Exception as e:
        print(f"Error scheduling event: {e}")


def attend_event(db):
    """
    Busca el evento pendiente más antiguo en Firestore (por fecha de creación),
    lo muestra y PIDE CONFIRMACIÓN para marcarlo como 'completed'.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         Attend Event')

    try:
        # Obtener una referencia a la colección de eventos
        events_ref = db.collection(COLLECTION_NAME)

        # Consultar los eventos con estado 'pending', ordenados por fecha de creación (ascendente)
        # y limitar a 1 para obtener el más antiguo.
        query = events_ref.where(filter=FieldFilter("status", "==", "pending")).order_by("created_at", direction='ASCENDING').limit(1) # <-- Usamos el string 'ASCENDING'

        # Obtener los resultados de la consulta
        docs = list(query.stream())

        if not docs:
            print('No pending events to attend.')
        else:
            # El primer documento en la lista es el evento más antiguo pendiente
            event_doc = docs[0]
            event_data = event_doc.to_dict()
            event_id = event_doc.id
            description = event_data.get("description", "No description")

            print(f'Next pending event (ID: {event_id}):')
            print(f'  Description: {description}')

            # --- ¡AÑADIR PASO DE CONFIRMACIÓN AQUÍ! ---
            confirm = input("Mark this event as completed? (yes/no): ").lower().strip()

            if confirm == 'yes':
                # Marcar el evento como 'completed' en Firestore
                event_doc.reference.update({'status': 'completed'})
                print("\nEvent marked as completed.") # Añadir un salto de línea para mejor lectura
            elif confirm == 'no':
                print("\nEvent was NOT marked as completed.") # Añadir un salto de línea
            else:
                print("\nInvalid response. Event was NOT marked as completed.") # Añadir un salto de línea

    except Exception as e:
        print(f"Error attending event: {e}")

def view_all_events(db):
    """Muestra todos los eventos en Firestore, ordenados por fecha de creación."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print('                                         All Events')

    try:
        # Obtener una referencia a la colección de eventos
        events_ref = db.collection(COLLECTION_NAME)

        # Consultar todos los eventos, ordenados por fecha de creación (ascendente)
        # --- CORRECCIÓN AQUÍ ---
        query = events_ref.order_by("created_at", direction='ASCENDING') # <-- Usamos el string 'ASCENDING'

        # Obtener los resultados de la consulta
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
                created_at = event_data.get("created_at") # Esto será un Timestamp object

                # Formatear la fecha de creación si está disponible
                date_str = "N/A"
                # Firestore SERVER_TIMESTAMP devuelve un objeto datetime
                if isinstance(created_at, datetime.datetime):
                    date_str = created_at.strftime('%Y-%m-%d %H:%M:%S') # Añadimos segundos para más precisión

                print(f"ID: {event_id}")
                print(f"  Description: {description}")
                print(f"  Status: {status}")
                print(f"  Created At: {date_str}")
                print("-" * 40)
                print("") # Línea en blanco entre eventos para mejor lectura


    except Exception as e:
        print(f"Error viewing events: {e}")


# --- Función Principal ---
def main():
    """Función principal de la aplicación de agenda."""

    # Inicializar Firebase y obtener el cliente de Firestore
    db = initialize_firebase()

    # Si la inicialización falla, salimos
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
            continue # Vuelve al inicio del bucle

        # IMPORTANTE: Limpiamos la pantalla *después* de obtener la opción
        # y *antes* de ejecutar la función, para que la salida de la función se vea.
        os.system('cls' if os.name == 'nt' else 'clear')

        if opc == SCHEDULE:
            schedule_event(db) # Pasamos el cliente de Firestore a la función
            # Pausa para que el usuario lea el resultado antes de limpiar
            input('Press ENTER to continue...') # <-- Añadir pausa aquí
        elif opc == ATTEND:
            attend_event(db) # Pasamos el cliente de Firestore a la función
            # Pausa para que el usuario lea el resultado antes de limpiar
            input('Press ENTER to continue...') # <-- Añadir pausa aquí
        elif opc == VIEW_ALL: # Nueva opción
            view_all_events(db) # Pasamos el cliente de Firestore a la función
            # --- ¡AÑADE LA PAUSA AQUÍ! ---
            input('Press ENTER to continue...') # <-- ESTA ES LA LÍNEA QUE FALTABA
        elif opc == QUIT:
            forward = False
            # No pedir ENTER después de Salir
            print('Good-Bye')
        else:
            print('Invalid option...')
            # Solo pedir ENTER si la opción no fue Salir
            input('Press ENTER to continue...')

if __name__ == '__main__':
    main()
