from django import forms
from .models import User, Teacher

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'user_type',
            'profile_picture',
            'address',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'specialties',
            'biography',
            'availability',
            'mode'
        ]

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
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
