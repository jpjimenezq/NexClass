from django.shortcuts import render, get_object_or_404, redirect
from users.models import Student, Teacher, Class, User, StudentFavoritesClasses
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse


SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')


def create_google_meet_link(request, class_id):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    # Definir la hora de inicio y fin de la reunión
    start_time = datetime.datetime.utcnow().isoformat() + 'Z'  # Hora actual UTC
    end_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'

    # Obtener la clase
    class_instance = get_object_or_404(Class, id=class_id)
    teacher = class_instance.teacher
    student = Student.objects.get(user=request.user)

    # Crear el evento con enlace de Meet
    event = {
        'summary': f'Clase: {class_instance.className}',
        'description': class_instance.description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Bogota',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Bogota',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string',  # Cambiar por un identificador único
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
            }
        },
    }

    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()

    # Obtener el enlace de Google Meet
    meet_link = event['hangoutLink']

    teacher_email = teacher.user.email
    student_email = student.user.email

    # Enviar el enlace por correo a los participantes
    send_mail(
        'Enlace de videollamada Google Meet',
        f'Aquí está el enlace para la clase: {meet_link}',
        settings.EMAIL_HOST_USER,
        ['afprietol2005@gmail.com', 'afprietol@eafit.edu.co'],  # Reemplazar con los correos reales
        fail_silently=False,
    )

    return JsonResponse({'meet_link': meet_link})


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


def add_favorite(request, class_id):

    student = get_object_or_404(Student, user=request.user)

    selected_class = get_object_or_404(Class, id=class_id)

    favorite, created = StudentFavoritesClasses.objects.get_or_create(
        student=student,
        student_class=selected_class
    )

    return redirect('student_classes')  # Cambiar por la URL adecuada
