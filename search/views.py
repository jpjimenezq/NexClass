from django.shortcuts import render
from users.models import Teacher

# Create your views here.
def teachers(request):
    searchTeacher = request.GET.get('searchTeacher', '')
    if searchTeacher:
        teachers = Teacher.objects.filter(specialties__icontains=searchTeacher)
    else:
        teachers = []
    return render(request, 'teachers.html', {'teachers': teachers, 'searchTeacher': searchTeacher})