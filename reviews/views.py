from django.shortcuts import render, redirect, get_object_or_404
from users.models import Teacher
from .models import TeacherRating
from .forms import TeacherRatingForm
from django.contrib.auth.decorators import login_required

@login_required
def rate_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = request.user.student  # Asumiendo que el usuario está autenticado como estudiante

    # Intenta recuperar una calificación existente
    try:
        rating = TeacherRating.objects.get(teacher=teacher, student=student)
        form = TeacherRatingForm(instance=rating)  # Prepara el formulario con la calificación existente
    except TeacherRating.DoesNotExist:
        rating = None
        form = TeacherRatingForm()

    if request.method == 'POST':
        form = TeacherRatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.teacher = teacher
            rating.student = student
            rating.save()
            return redirect('teachers_detail', teacher_id=teacher.id)

    return render(request, 'rate_teacher.html', {'form': form, 'teacher': teacher})
