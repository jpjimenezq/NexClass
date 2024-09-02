from django.shortcuts import render
from users.models import Teacher, Specialties, Mode, Availability
from django.db.models import Q

# Create your views here.
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