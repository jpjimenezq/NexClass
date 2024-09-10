from django.shortcuts import render, get_object_or_404, redirect
from users.models import Student, Teacher, Class, User, StudentFavoritesTeachers, StudentFavoritesClasses
from django.contrib.auth.decorators import login_required



# Create your views here.
def add_favorite_class(request, class_id):
    """Añade una clase a la lista de favoritos.html del estudiante."""
    student = get_object_or_404(Student, user=request.user)
    selected_class = get_object_or_404(Class, id=class_id)

    # Crea o recupera el favorito
    favorite, created = StudentFavoritesClasses.objects.get_or_create(
        student=student,
        student_class=selected_class
    )

    return redirect('student_classes')


def add_favorite_teacher(request, teacher_id):
    """Añade una clase a la lista de favoritos.html del estudiante."""
    student = get_object_or_404(Student, user=request.user)
    selected_teacher = get_object_or_404(Teacher, id=teacher_id)

    # Crea o recupera el favorito
    favorite, created = StudentFavoritesTeachers.objects.get_or_create(
        student=student,
        teacher=selected_teacher
    )

    return redirect('teachers')

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

