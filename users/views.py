from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from .models import User
from django.urls import reverse
from .models import Favourites

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
                if user.password==password:
                    request.session['usuario_autenticado'] = True
                    request.session['user_id'] = user.user_id
                    return redirect('home')
                else:
                    form.add_error(None, 'Access denied')
            except User.DoesNotExist:
                form.add_error(None, 'Access denied, user not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    try:
        del request.session['usuario_autenticado']
        del request.session['usuario_id']
    except KeyError:
        pass
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already in use')
            else:
                form.save()
                request.session['usuario_autenticado'] = True
                return redirect('home')
        else:
            form.add_error(None, "Error")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def favoritos(request):
    favourites = Favourites.objects.all()
    return render(request, 'favoritos.html', {'favourites':favourites})