from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Configuración de la API de Google Calendar
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('calendar', 'v3', credentials=credentials)

def google_meet_create(teacher_email, student_email, class_name, class_description, start, end):
    evento = {
        'summary': class_name,
        'description': class_description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Bogota',  # Ajusta según la zona horaria
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Bogota',
        },
        'attendees': [
            {'email': teacher_email},
            {'email': student_email},
        ],
        'conferenceData': {
            'createRequest': {
                'requestId': 'some-random-id',  # Puedes usar un UUID o identificador único
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet',
                },
            },
        },
    }

    evento = service.events().insert(
        calendarId='primary',
        body=evento,
        conferenceDataVersion=1,
        sendNotifications=True,
    ).execute()

    return evento.get('hangoutLink')
