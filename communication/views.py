from django.shortcuts import render, get_object_or_404
from users.models import Student, Teacher
from django.core.mail import send_mail
from .services.google_calendar import google_meet_create
from datetime import datetime, timedelta

def Student_classes(request, student_id):
    student = get_object_or_404(Student, student_id)
    classes = Student.classes.all()
    return render(request, 'student_classes.html', {'student': student, 'classes': classes})

def Invitation(request, student_id, teacher_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=student_id)
        teacher = get_object_or_404(Teacher, pk=teacher_id)

        # Define los detalles de la reunión
        start = (datetime.now() + timedelta(days=1)).isoformat()  # Ejemplo: reunión para mañana
        end = (datetime.now() + timedelta(days=1, hours=1)).isoformat()  # Duración de 1 hora
        class_name = 'Reunión con el Estudiante'
        class_description = 'Esta es una reunión programada con el estudiante.'

        # Crea la reunión y obtiene el enlace
        meet_link = google_meet_create(
            teacher.email,
            student.email,
            class_name,
            class_description,
            start,
            end
        )

        # Envía el correo electrónico
        send_mail(
            f'Invitación a la reunión de la clase: {class_name}',
            f'Por favor, únase a la reunión utilizando el siguiente enlace de Google Meet: {meet_link}',
            'correo@correo.com',
            [teacher.email, student.email],
            fail_silently=False,
        )

        return render(request, 'invitation.html', {'meet_link': meet_link})
    else:
        return redirect('student_classes')  # Redirige a la lista de clases si el método no es POST
# Create your views here.
