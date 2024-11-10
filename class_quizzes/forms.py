from django import forms
from .models import Quiz, Question, Answer
from classCreation_Schedules.models import Class


class QuizForm(forms.ModelForm):
    class_obj = forms.ModelChoiceField(
        queryset=Class.objects.all(),  # Inicialmente vacío
        label="class",
        widget=forms.Select(attrs={'class': 'form-select bg-info-subtle'})  # Agregar clase Bootstrap aquí
    )
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'class_obj']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Enter quiz title'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-info-subtle', 'placeholder': 'Enter quiz description'}),
        }


class QuizFormClass(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quiz title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter quiz description'}),
        }



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']

AnswerFormSet = forms.modelformset_factory(Answer, form=AnswerForm, extra=4)