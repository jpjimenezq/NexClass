from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm, TeacherForm, EditUserForm, EditTeacherForm
from .models import User, Student, Teacher
from django.urls import reverse
from .models import StudentFavoritesTeachers, StudentFavoritesClasses

# Create your views here.
def home(request):
    return render(request, 'home.html')

def landing(request):
    return render(request, 'landing.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['usuario_autenticado'] = True
                    request.session['usuario_id'] = user.user_id
                    if not user.profile_complete:
                        if user.user_type == 'Teacher':
                            return redirect('complete_profile')
                        elif user.user_type == 'Student':
                            Student.objects.get_or_create(user=user)
                            user.profile_complete = True
                            user.save()
                    return redirect('home')
                else:
                    form.add_error(None, 'Access denied')
            except User.DoesNotExist:
                form.add_error(None, 'Access denied, user not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def loguout(request):
    try:
        del request.session['usuario_autenticado']
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('login')

def register(request):
    try:
        del request.session['usuario_autenticado']
        del request.session['usuario_id']
    except KeyError:
        pass
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already in use')
            else:
                form.save()
                user = User.objects.get(username=username)
                request.session['usuario_autenticado'] = True
                request.session['usuario_id'] = user.user_id
                if not user.profile_complete:
                    if user.user_type == 'Teacher':
                        return redirect('complete_profile')
                    elif user.user_type == 'Student':
                        Student.objects.get_or_create(user=user)
                        user.profile_complete = True
                        user.save()
                return redirect('home')
        else:
            form.add_error(None, "Error")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def favoritos(request):
    favourites = Favourites.objects.all()
    return render(request, 'favoritos.html', {'favourites':favourites})

def complete_profile(request):
    user_id = request.session.get('usuario_id')
    user = User.objects.get(user_id=user_id)
    if request.method == 'POST':
        if user.user_type == 'Teacher':
            form = TeacherForm(request.POST)
        if form.is_valid():
            if user.user_type == 'Teacher':
                teacher = form.save(commit=False)
                teacher.user = user
                teacher.save()
            user.profile_complete = True
            user.save()
            return redirect('home')
    else:
        if user.user_type == 'Teacher':
            form = TeacherForm()
    return render(request, 'complete_profile.html', {'form': form})

def edit_profile(request):
    if not request.session.get('usuario_autenticado'):
        return redirect('login')
    user_id = request.session.get('usuario_id')
    user = get_object_or_404(User, user_id=user_id)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, request.FILES, instance=user)
        if user.user_type == 'Teacher':
            teacher = get_object_or_404(Teacher, user=user)
            teacher_form = EditTeacherForm(request.POST, instance=teacher)
            if user_form.is_valid() and teacher_form.is_valid():
                user_form.save()
                teacher_form.save()
                return redirect('home')
        else:
            if user_form.is_valid():
                user_form.save()
                return redirect('home')
    else:
        user_form = EditUserForm(instance=user)
        teacher_form = None
        if user.user_type == 'Teacher':
            teacher = get_object_or_404(Teacher, user=user)
            teacher_form = EditTeacherForm(instance=teacher)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'teacher_form': teacher_form})

def student_classes(request):
    # Aquí va la lógica para obtener las clases del estudiante
    return render(request, 'student_classes.html')  # Renderiza el template