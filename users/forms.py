from django import forms
from .models import User

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
