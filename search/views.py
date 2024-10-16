from django.shortcuts import render, get_object_or_404, redirect
from users.models import Teacher, Specialties, Mode, Availability
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from teacher_blog.models import BlogPost
from users.models import ProfessorChatMessage
from users.forms import ChatMessageForm

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

    
    teachers = Teacher.objects.filter(filters)

    
    filtered_teachers = []
    for teacher in teachers:
        avg_rating = teacher.average_rating()
        if rating_filter:
            if avg_rating >= float(rating_filter):
                filtered_teachers.append(teacher)
        else:
            filtered_teachers.append(teacher)

    return render(request, 'teachers.html', {
        'teachers': filtered_teachers,
        'specialties': Specialties.choices,
        'modes': Mode.choices,
        'availabilities': Availability.choices
    })



@login_required()
def teachers_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    ratings = teacher.ratings.all()
    blog_posts = BlogPost.objects.filter(teacher=teacher)

    return render(request, 'teachers_detail.html', {
        'teacher': teacher,
        'ratings': ratings,
        'average_rating': teacher.average_rating(),
        'blog_posts': blog_posts,
    })

@login_required()
def send_message(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            professor_chat_message = form.save(commit=False)
            professor_chat_message.student = request.user.student  # Asegúrate de que el usuario es un estudiante
            professor_chat_message.teacher = teacher  # Relaciona con el profesor
            professor_chat_message.content = form.cleaned_data['content']  # Asigna el contenido
            professor_chat_message.save()
            return redirect('chat', teacher_id=teacher_id)  # Redirige al chat
    else:
        form = ChatMessageForm()

    return render(request, 'chat/send_message.html', {
        'form': form,
        'teacher': teacher
    })


@login_required()
def chat(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    messages = ProfessorChatMessage.objects.filter(teacher=teacher, student=request.user.student).order_by('timestamp')

    return render(request, 'chat.html', {
        'messages': messages,
        'teacher': teacher  # Para mostrar información del profesor
    })


