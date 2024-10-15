from django.contrib import admin
from .models import Answer, Question, Quiz, QuizResult

# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizResult)
