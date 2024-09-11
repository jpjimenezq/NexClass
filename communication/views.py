from django.shortcuts import render, get_object_or_404, redirect
from users.models import Student, Teacher, Class, User, StudentFavoritesClasses
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from datetime import datetime, timedelta
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import uuid
from google.auth.transport.requests import Request



from django.contrib import messages


SCOPES = ['https://www.googleapis.com/auth/calendar']


# Función para obtener las credenciales de Google API
def get_google_credentials():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        os.remove(token_path)

        # El usuario tendrá que iniciar sesión siempre
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open(token_path, 'w') as token:
        token.write(creds.to_json())

    return creds


def create_google_meet_event(student_email, teacher_email, class_name):
    credentials = get_google_credentials()
    service = build('calendar', 'v3', credentials=credentials)

    # Definir el evento de Google Calendar
    event = {
        'summary': f'Clase: {class_name}',
        'description': 'Enlace para la clase en Google Meet.',
        'start': {
            'dateTime': (datetime.now() + timedelta(minutes=5)).isoformat(),
            'timeZone': 'America/Bogota',  # Ajusta la zona horaria
        },
        'end': {
            'dateTime': (datetime.now() + timedelta(hours=1)).isoformat(),
            'timeZone': 'America/Bogota',
        },
        'attendees': [
            {'email': student_email},
            {'email': teacher_email},
        ],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': f'{uuid.uuid4()}',
            },
        },
    }

    # Crear el evento en Google Calendar
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return event.get('hangoutLink')


# Vista que genera el enlace de Meet y envía los correos
@login_required
def generate_meet_link(request, class_id):
    student = Student.objects.get(user=request.user)
    selected_class = Class.objects.get(id=class_id)

    meet_link = create_google_meet_event(
        student_email=request.user.email,
        teacher_email=selected_class.teacher.user.email,
        class_name=selected_class.className
    )

    # Enviar correos tanto al estudiante como al profesor
    subject = f'Enlace para la clase {selected_class.className}'
    message = f'El enlace para la clase es: {meet_link}'
    student_email = request.user.email
    teacher_email = selected_class.teacher.user.email

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [student_email, teacher_email]
    )
    return render(request, 'success.html', {'meet_link': meet_link})

@login_required()
def classes(request):
    searchClass = request.GET.get('searchClass', '')
    className = request.GET.get('className', '')
    teacher = request.GET.get('teacher', '')

    filters = Q()
    if searchClass:
        filters |= (
                Q(teacher__user__username__icontains=searchClass) |
                Q(teacher__biography__icontains=searchClass) |
                Q(teacher__specialties__icontains=searchClass) |
                Q(teacher__mode__icontains=searchClass) |
                Q(teacher__availability__icontains=searchClass) |
                Q(className__icontains=searchClass) |
                Q(description__icontains=searchClass)
        )
    if className:
        filters &= Q(className__icontains=className)

    if teacher:
        filters &= Q(teacher__user__username__icontains=teacher)

    classes = Class.objects.filter(filters)

    context = {
        'classes': classes,
        'className': Class.objects.values_list('className', flat=True).distinct(),
        'teacher': Teacher.objects.values_list('user__username', flat=True).distinct()
    }

    return render(request, 'student_classes.html', context)



