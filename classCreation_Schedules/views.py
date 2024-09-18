from django.shortcuts import render, redirect
from .models import Class, Schedule
from .forms import ClassForm, ScheduleForm


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
