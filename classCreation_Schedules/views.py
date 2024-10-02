from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Schedule
from .forms import ClassForm, ScheduleForm
from users.models import Teacher


def teacher_classes(request):
    teacher = Teacher.objects.get(user=request.user)
    classes = Class.objects.filter(teacher=teacher)
    return render(request, 'teacher_classes.html', {'classes': classes})


def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST, request.FILES)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.teacher = request.user.teacher  # Asumiendo que el usuario es un Teacher
            class_obj.save()
            return redirect('add_schedule', class_id=class_obj.id)
    else:
        form = ClassForm()
    return render(request, 'create_class.html', {'form': form})


def add_schedule(request, class_id):
    class_obj = Class.objects.get(id=class_id)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_obj = class_obj
            schedule.save()
            return redirect('add_schedule', class_id=class_id)
    else:
        form = ScheduleForm()
    return render(request, 'add_schedule.html', {'form': form, 'class_obj': class_obj})


def edit_class(request, class_id):
    class_obj_instance = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ClassForm(request.POST, request.FILES, instance=class_obj_instance)
        if form.is_valid():
            form.save()
            return redirect('teacher_classes_detail', class_id=class_id)
    else:
        form = ClassForm(instance=class_obj_instance)

    return render(request, 'edit_class.html', {'form': form, 'class_obj_instance': class_obj_instance})


def delete_class(request, class_id):
    class_obj_instance = get_object_or_404(Class, id=class_id)
    class_obj_instance.delete()
    return redirect('teacher_classes')


def class_detail_teacher(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)

    return render(request, 'class_detail_teacher.html', {'class_obj': class_obj})
