from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("")

    return render(request, 'login.html', context={
        'loginform': form
    })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'register.html', context ={
        'registerForm': form
    })