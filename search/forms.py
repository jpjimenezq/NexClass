from django import forms
from users.models import Teacher

class TeacherSearchForm(forms.Form):
    searchTeacher = forms.CharField(label='Buscar por nombre o biografía', required=False)
    specialties = forms.ChoiceField(
        choices=Teacher.Specialties.choices,
        required=False,
        label='Especialidad'
    )
    mode = forms.ChoiceField(
        choices=Teacher.Mode.choices,
        required=False,
        label='Modalidad'
    )
    availability = forms.ChoiceField(
        choices=Teacher.Availability.choices,
        required=False,
        label='Disponibilidad'
    )