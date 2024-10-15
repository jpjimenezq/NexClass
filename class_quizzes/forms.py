from django import forms
from .models import Quiz, Question, Answer
from classCreation_Schedules.models import Class


class QuizForm(forms.ModelForm):
    class_obj = forms.ModelChoiceField(
        queryset=Class.objects.none(),  # Inicialmente vacío
        label="class",
        widget=forms.Select(attrs={'class': 'form-select'})  # Agregar clase Bootstrap aquí
    )
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'class_obj']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quiz title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter quiz description'}),
        }

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)  # Obtener el class_id de los kwargs
        super(QuizForm, self).__init__(*args, **kwargs)
        if class_id:
            self.fields['class_obj'].queryset = Class.objects.filter(id=class_id)


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