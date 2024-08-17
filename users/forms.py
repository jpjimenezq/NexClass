from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import User

class CreateUserForm(UserCreationForm):
    typeUser = forms.ChoiceField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')])
    location = forms.CharField(max_length=255, required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'typeUser', 'location', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())