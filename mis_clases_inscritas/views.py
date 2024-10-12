from django.shortcuts import render, redirect, get_object_or_404
from .models import EnrolledClasses, HistoryClasses
from classCreation_Schedules.models import Class, Schedule
from users.models import Student
from django.contrib import messages


# Create your views here.
def enroll_in_class(request, class_id):
    student_class = get_object_or_404(Class, id=class_id)
    student = Student.objects.get(user=request.user)

    if EnrolledClasses.objects.filter(student=student, student_class=student_class).exists():
        messages.warning(request, 'Ya estás inscrito en esta clase.')
        return redirect('class_detail', class_id=student_class.id)
    else:
        EnrolledClasses.objects.create(student=student, student_class=student_class)

        HistoryClasses.objects.create(student=student, student_class=student_class, action='enrolled')

        messages.success(request, f'Te has inscrito exitosamente en la clase {student_class.className}.')


        # teacher_email = student_class.teacher.user.email
        # send_mail(
        #     'Nuevo estudiante inscrito',
        #     f'{student.user.username} se ha inscrito a tu clase {student_class.class_name}.',
        #     'from@example.com',
        #     [teacher_email],
        #     fail_silently=False,
        # )

    return redirect('clases_inscritas')


def remove_class(request, class_id):
    student = Student.objects.get(user=request.user)
    student_class = get_object_or_404(Class, id=class_id)

    # Eliminar la clase de las clases inscritas del estudiante
    EnrolledClasses.objects.filter(student=student, student_class=student_class).delete()

    # Registrar la acción en el historial
    HistoryClasses.objects.create(student=student, student_class=student_class, action='removed')

    messages.success(request, f'Has eliminado la clase {student_class.className} de tus clases inscritas.')

    return redirect('clases_inscritas')


def clases_inscritas(request):
    student = Student.objects.get(user=request.user)
    enrolled_classes = EnrolledClasses.objects.filter(student=student)  # Filtrar clases inscritas por el estudiante

    return render(request, 'clases_inscritas.html', {'enrolled_classes': enrolled_classes})


def mi_clase_inscrita(request, class_id):
    student = Student.objects.get(user=request.user)
    class_obj = get_object_or_404(Class, id=class_id)
    schedules = Schedule.objects.filter(class_obj=class_obj, available=True)

    return render(request, 'mi_clase_inscrita.html', {'class_obj': class_obj, 'schedules': schedules})