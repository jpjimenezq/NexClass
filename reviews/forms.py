from django import forms
from .models import TeacherRating


class TeacherRatingForm(forms.ModelForm):
    class Meta:
        model = TeacherRating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),}