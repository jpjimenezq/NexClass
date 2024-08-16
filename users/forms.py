from django import forms
from .models import User

# Define las opciones para el campo user_type
USER_TYPE_CHOICES = [
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
]

class CreateUserForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['name', 'email', 'user_type', 'profile_photo', 'location', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
