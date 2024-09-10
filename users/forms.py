from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Teacher, Student
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'user_type', 'password1', 'password2']

class TeacherCreationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['specialties', 'biography', 'availability', 'mode']

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'profile_picture',
            'address',
            'password',
        ]
        widgets = {
            'email': forms.EmailInput(),
        }

class EditTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'specialties',
            'biography',
            'availability',
            'mode'
        ]
