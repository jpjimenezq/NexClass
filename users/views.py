from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import (
    CustomUserCreationForm, TeacherCreationForm, StudentCreationForm,
    StudentUpdateForm, UserUpdateForm, EditTeacherForm
)
from .models import User, Student, Teacher, UserType
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from mis_clases_inscritas.models import HistoryClasses
from teacher_blog.models import BlogPost
from NextClassProject.settings import GENERATIVE_AI_KEY
from .models import ChatMessage
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os
from classCreation_Schedules.models import Class
from embeddings_simmilarities.utils import calcular_similitud
from django.db.models import Count
import json

INITIAL_CONTEXT = """
    Eres un asistente virtual amigable y experto en asesoramiento sobre clases y profesores. 
    Responde a las preguntas de los usuarios de manera clara, concisa y directa, evitando explicaciones largas. 
    Si el usuario menciona dificultades en alguna materia o muestra interés en aprender algo nuevo, siempre responde recomendando un profesor o clase. 
    Usa alguna de estas expresiones forzosamente dependiendo de de la pregunta: "te recomiendo", "puedes encontrar ayuda en", o "podrías buscar un profesor especializado en". 
    Interpreta naturalmente el mensaje del usuario y haz recomendaciones cuando corresponda. 
    Si no es necesario recomendar un profesor o clase, responde normalmente.
"""


MAX_HISTORY = 10

genai.configure(api_key=GENERATIVE_AI_KEY)

# Create your views here.
@login_required
def home(request):
    user = request.user  # Usuario autenticado
    resultado_clases_sorted = []
    resultado_teacher_sorted = []
    if request.method == 'POST':
        # Procesar el mensaje del chatbot
        genai.configure(api_key=GENERATIVE_AI_KEY)
        model = genai.GenerativeModel("gemini-pro")

        user_message = request.POST.get('user_message')

        # Recupera el historial de mensajes del usuario logueado
        messages = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:MAX_HISTORY]

        # Construye el prompt con los mensajes filtrados por el usuario
        prompt = INITIAL_CONTEXT + "\n"
        for msg in reversed(messages):  # Revertir para mantener el orden cronológico
            prompt += f"Usuario: {msg.user_message}\nAsistente: {msg.bot_response}\n"
        prompt += f"Usuario: {user_message}\nAsistente:"

        # Generar la respuesta del bot
        try:
            bot_response = model.generate_content(prompt)
            bot_text = bot_response.text.strip()
            # MEjorar esto que esta como rarito, para poder identificar si necesita o no
            if "te recomiendo" in bot_text.lower() or "puedes encontrar ayuda en" in bot_text.lower() or "podrías buscar un profesor especializado en" in bot_text.lower():

                _ = load_dotenv('api_keys.env')
                client = OpenAI(
                    # This is the default and can be omitted
                    api_key=os.environ.get('openai_apikey'),)

                response = client.embeddings.create(
                    input=user_message,
                    model = "text-embedding-ada-002"
                )
                user_embedding = response.data[0].embedding

                clases = Class.objects.all()

                teachers = Teacher.objects.all()

                resultado_teacher = []
                resultado_clases = []

                for clase in clases:
                    similitud = calcular_similitud(user_embedding, clase.get_embedding())
                    resultado_clases.append((clase, similitud))

                for teacher in teachers:
                    similitud = calcular_similitud(user_embedding, teacher.get_embedding())
                    resultado_teacher.append((teacher, similitud))

                resultado_clases_sorted = sorted(resultado_clases, key=lambda x: x[1], reverse=True)[:3]
                resultado_teacher_sorted = sorted(resultado_teacher, key=lambda x: x[1], reverse=True)[:3]
                bot_text += "\nTe recomendaría estas opciones basadas en tu mensaje:\n"
                bot_text += "clases: "
                for class_obj, sim in resultado_clases_sorted:
                    bot_text += f'<a href="{reverse("class_detail", args=[class_obj.id])}" class="">'
                    bot_text += f'<strong>{class_obj.className},</strong></a> '
                bot_text += "teachers: "
                for teacher, sim in resultado_teacher_sorted:
                    bot_text += f'<a href="{reverse("teachers_detail", args=[teacher.id])}" class="">'
                    bot_text += f'<strong>{teacher.user.name},</strong></a> '


        except Exception as e:
            bot_text = "Lo siento, ocurrió un error al generar la respuesta."
            print(f"Error generando respuesta: {e}")

        # Guardar el nuevo mensaje del usuario
        ChatMessage.objects.create(user=user, user_message=user_message, bot_response=bot_text)

        # Actualizar el historial de mensajes del usuario
        messages = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:MAX_HISTORY]

        return render(request, 'home.html', {
            'user': user,
            'messages': messages,
            'bot_response': bot_text,
        })

    else:
        # Obtener solo los mensajes del usuario autenticado
        messages = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:MAX_HISTORY]
        return render(request, 'home.html', {
            'user': user,
            'messages': messages
        })


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
        student = get_object_or_404(Student, user=request.user)

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

        teacher = get_object_or_404(Teacher, user=request.user)
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
    teacher = Teacher.objects.get(user=request.user)
    print(f'teacher: {teacher}')
    classes = Class.objects.filter(teacher=teacher).annotate(enrollment_count=Count('enrolledclasses'))
    print(f"classes: {classes}")
    class_names = [cls.className for cls in classes]
    enrollment_counts = [cls.enrollment_count for cls in classes]
    print(f"class_names: {class_names}")
    print(f"enrollment_counts: {enrollment_counts}")


    context = {
        'class_names': json.dumps(class_names),
        'enrollment_counts': json.dumps(enrollment_counts),
        'teacher': teacher,
    }

    return render(request, 'home_teacher.html', context)


@login_required
def my_profile_student(request):
    user = request.user
    student = get_object_or_404(Student, user=user)
    history_classes = HistoryClasses.objects.filter(student=student)
    return render(request, 'my_profile_student.html', {'student': student, 'history_classes': history_classes})


@login_required
def my_profile_teacher(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    blog_posts = BlogPost.objects.filter(teacher=teacher)
    return render(request, 'my_profile_teacher.html', {
        'teacher': teacher,
        'blog_posts': blog_posts,
    })
