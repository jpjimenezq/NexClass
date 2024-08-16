from django.shortcuts import render, redirect
from .forms import CreateUserForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

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