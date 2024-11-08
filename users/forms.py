from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Teacher, Student

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Nombre de usuario' )
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'user_type', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-info-subtle'}),
            'user_type': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control bg-info-subtle'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control bg-info-subtle'}),
        }

class TeacherCreationForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['specialities', 'description', 'biography', 'availability', 'mode', 'ciudad']

        widgets = {
            'specialities': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-info-subtle'}),
            'biography': forms.Textarea(attrs={'class': 'form-control bg-info-subtle'}),
            'availability': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'mode': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
        }


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
            'name': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-info-subtle'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control bg-info-subtle'}),
            'address': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control bg-info-subtle'}),
        }



class EditTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'specialities',
            'description',
            'biography',
            'availability',
            'mode',
            'ciudad'
        ]
        widgets = {
            'specialities': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'description': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'biography': forms.Textarea(attrs={'class': 'form-control bg-info-subtle', 'rows': 5, 'placeholder': 'Biografía'}),
            'availability': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'mode': forms.Select(attrs={'class': 'form-control bg-info-subtle'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control bg-info-subtle'}),
        }


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = []  # Si no tienes campos adicionales en Student, puedes dejarlo vacío


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'username',
            'email',
            'profile_picture',
            'address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Nombre completo'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Correo electrónico'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control bg-info-subtle'}),
            'address': forms.TextInput(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Dirección'}),
        }
