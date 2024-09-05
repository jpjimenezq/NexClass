from django.shortcuts import render, get_object_or_404
from users.models import Student, Teacher, Class
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.shortcuts import redirect

import os
import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_calendar_service():
    creds = None
    if os.path.exists('credentials.json'):
        creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guardar el token de acceso
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_google_meet_event(teacher_email, student_email, class_name):
    service = get_google_calendar_service()

    event = {
        'summary': f'Clase: {class_name}',
        'description': 'Clase a través de Google Meet',
        'start': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).isoformat() + 'Z',
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z',
            'timeZone': 'America/Bogota',
        },
        'attendees': [
            {'email': teacher_email},
            {'email': student_email},
        ],
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            },
        },
    }

    # Crear el evento con Google Meet
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1,
    ).execute()

    return event['hangoutLink']

def create_meet_and_send_emails(request, class_id):
    clase = Class.objects.get(pk=class_id)
    student = Student.objects.get(user=request.user)
    teacher = clase.teacher

    meet_link = create_google_meet_event(teacher.user.email, student.user.email, clase.className)

    # Enviar el correo con el enlace
    send_mail(
        'Enlace de Google Meet para tu clase',
        f'El enlace para la clase "{clase.className}" es: {meet_link}',
        'noreply@tuapp.com',
        [teacher.user.email, student.user.email],
        fail_silently=False,
    )
    return redirect('student_classes')


