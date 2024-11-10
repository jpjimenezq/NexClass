from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Solo el contenido del mensaje


        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control bg-info-subtle', 'rows': 4}),


        }


