from django.shortcuts import render, get_object_or_404
from users.models import Teacher, Specialties, Mode, Availability
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def teachers(request):
    searchTeacher = request.GET.get('searchTeacher', '')
    specialties_filter = request.GET.get('specialties', '')
    mode_filter = request.GET.get('mode', '')
    availability_filter = request.GET.get('availability', '')
    rating_filter = request.GET.get('rating', '')

    filters = Q()
    if searchTeacher:
        filters |= (
            Q(user__username__icontains=searchTeacher) |
            Q(biography__icontains=searchTeacher) |
            Q(specialties__icontains=searchTeacher) |
            Q(mode__icontains=searchTeacher) |
            Q(availability__icontains=searchTeacher)
        )
    if specialties_filter:
        filters &= Q(specialties=specialties_filter)
    if mode_filter:
        filters &= Q(mode=mode_filter)
    if availability_filter:
        filters &= Q(availability=availability_filter)
    if rating_filter:
        filters &= Q(average_rating__gte=float(rating_filter))

    teachers = Teacher.objects.filter(filters)

    return render(request, 'teachers.html', {
        'teachers': teachers,
        'specialties': Specialties.choices,
        'modes': Mode.choices,
        'availabilities': Availability.choices
    })

@login_required()
def teachers_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teachers_detail.html', {'teacher': teacher})