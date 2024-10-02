from django import forms
from .models import Class, Schedule

from django.forms.widgets import DateTimeInput



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['className', 'description', 'class_picture']

        widgets = {
            'className': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'width:100%;'}),
            'class_picture': forms.ClearableFileInput(attrs={'class': 'form-control '}),
        }



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['start_time', 'end_time', 'available']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Select date and time'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'Select date and time'}),
        }
