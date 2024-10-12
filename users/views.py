from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, TeacherCreationForm, StudentCreationForm, StudentUpdateForm, UserUpdateForm, EditTeacherForm
from .models import User, Student, Teacher
from .models import UserType
from django.urls import reverse
from .models import StudentFavoritesTeachers, StudentFavoritesClasses
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from mis_clases_inscritas.models import HistoryClasses


# Create your views here.
@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user' : user})


def landing(request):
    return render(request, 'landing.html')


def signup_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        teacher_form = None
        student_form = None

        if user_form.is_valid():
            user = user_form.save()

            # Si el tipo de usuario es Teacher, redirigir a completar el perfil
            if user.user_type == UserType.TEACHER:
                login(request, user)  # Autenticamos al usuario antes de redirigirlo
                return redirect('complete_profile')


            elif user.user_type == UserType.STUDENT:
                student_form = StudentCreationForm(request.POST)
                if student_form.is_valid():
                    student = student_form.save(commit=False)
                    student.user = user
                    student.save()


            login(request, user)
            return redirect('home')
    else:
        user_form = CustomUserCreationForm()
        teacher_form = TeacherCreationForm()
        student_form = StudentCreationForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'student_form': student_form,
    })


@login_required()
def complete_profile_view(request):
    user = request.user

    if not user.is_authenticated or user.user_type != UserType.TEACHER:
        return redirect('login')  # Redirigir si no es un profesor o no está autenticado

    if request.method == 'POST':
        teacher_form = TeacherCreationForm(request.POST)
        if teacher_form.is_valid():
            teacher = teacher_form.save(commit=False)
            teacher.user = user  # Asociamos el usuario con el perfil de Teacher
            teacher.save()
            return redirect('home_teacher')
    else:
        teacher_form = TeacherCreationForm()

    return render(request, 'complete_profile.html', {
        'teacher_form': teacher_form,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirigir dependiendo del tipo de usuario
            if hasattr(user, 'student'):
                return redirect('home')  # Si es estudiante, redirige a home.html
            elif hasattr(user, 'teacher'):
                return redirect('home_teacher')  # Si es profesor, redirige a otro template

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def student_classes(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')
    user = request.user  # Obtenemos al usuario autenticado
    student = get_object_or_404(Student, user=user)
    # Aquí va la lógica para obtener las clases del estudiante
    return render(request, 'student_classes.html', {'user': user})  # Renderiza el template


@login_required
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    form = None
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('my_profile_teacher')
    else:
        form = TeacherCreationForm(instance=teacher)
    return render(request, 'edit_teacher_profile.html', {'form': form})


@login_required
def modificar_perfil(request):
    user = request.user


    if hasattr(user, 'student'):
        navbar_template = 'navbar.html'
        student = user.student
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            student_form = StudentUpdateForm(request.POST, instance=student)

            if user_form.is_valid() and student_form.is_valid():
                user_form.save()
                student_form.save()
                return redirect('home')
        else:
            user_form = UserUpdateForm(instance=user)
            student_form = StudentUpdateForm(instance=student)

        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'student_form': student_form,
            'navbar_template': navbar_template
        })

    elif hasattr(user, 'teacher'):
        teacher = user.teacher
        navbar_template = 'navbarTeacher.html'

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            teacher_form = EditTeacherForm(request.POST, instance=teacher)

            if user_form.is_valid() and teacher_form.is_valid():
                user_form.save()
                teacher_form.save()
                return redirect('home_teacher')
        else:
            user_form = UserUpdateForm(instance=user)
            teacher_form = EditTeacherForm(instance=teacher)

        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'teacher_form': teacher_form,
            'navbar_template': navbar_template
        })

    else:
        return redirect('landing')  # Redirigir si no es ni estudiante ni profesor

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')

            # Redirigir según el tipo de usuario y establecer el navbar
            if hasattr(user, 'student'):
                navbar_template = 'navbar.html'  # Navbar para estudiantes
                return redirect('home')  # Redirige a la página del estudiante
            elif hasattr(user, 'teacher'):
                navbar_template = 'navbarTeacher.html'  # Navbar para profesores
                return redirect('home_teacher')  # Redirige a la página del profesor
            else:
                navbar_template = 'navbarLanding.html'  # Navbar por defecto
                return redirect('home')  # Redirige a una página por defecto

    else:
        form = PasswordChangeForm(request.user)

    # Determinar el navbar antes de renderizar
    if hasattr(request.user, 'student'):
        navbar_template = 'navbar.html'
    elif hasattr(request.user, 'teacher'):
        navbar_template = 'navbarTeacher.html'
    else:
        navbar_template = 'navbarLanding.html'

    return render(request, 'cambiar_contrasena.html', {
        'form': form,
        'navbar_template': navbar_template,  # Pasar el navbar al contexto
    })


@login_required
def home_teacher(request):
    return render(request, 'home_teacher.html')


@login_required
def my_profile_student(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    history_classes = HistoryClasses.objects.filter(student=student)
    return render(request, 'my_profile_student.html', {'student': student, 'history_classes': history_classes})


@login_required
def my_profile_teacher(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    return render(request, 'my_profile_teacher.html', {'teacher': teacher})
