from django.shortcuts import render, get_object_or_404, redirect
from users.models import Student, Teacher, Class, User, StudentFavoritesTeachers, StudentFavoritesClasses
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def add_favorite_class(request, class_id):
    student = get_object_or_404(Student, user=request.user)
    selected_class = get_object_or_404(Class, id=class_id)

    if StudentFavoritesClasses.objects.filter(student=student, student_class=selected_class).exists():
        messages.warning(request, "Ya te anadiste la clase a favoritos.")
        return redirect('class_detail', class_id=selected_class.id)

    StudentFavoritesClasses.objects.create(student=student, student_class=selected_class)
    messages.success(request, "¡Anadiste correctamente a favoritos esta clase!")
    return redirect('class_detail', class_id=selected_class.id)


def add_favorite_teacher(request, teacher_id):
    student = get_object_or_404(Student, user=request.user)
    selected_teacher = get_object_or_404(Teacher, id=teacher_id)
    if StudentFavoritesTeachers.objects.filter(student=student, teacher=selected_teacher).exists():
        messages.warning(request, "Ya te anadiste el profesor a favoritos.")
        return redirect('teachers_detail', teacher_id=selected_teacher.id)

    StudentFavoritesTeachers.objects.create(student=student, teacher=selected_teacher)
    messages.success(request, "¡Anadiste correctamente a favoritos este profesor!")
    return redirect('teachers_detail', teacher_id=selected_teacher.id)


@login_required
def favorites_view(request):
    student_instance = Student.objects.get(user=request.user)

    student_favorites_classes = StudentFavoritesClasses.objects.filter(student=student_instance)
    student_favorites_teacher = StudentFavoritesTeachers.objects.filter(student=student_instance)

    # Pasar ambos conjuntos de datos al template
    context = {
        'student_favorites_classes': student_favorites_classes,
        'student_favorites_teacher': student_favorites_teacher,
    }

    return render(request, 'favoritos.html', context)

