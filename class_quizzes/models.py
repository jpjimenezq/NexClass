from django.db import models
from users.models import Student, Teacher, User
from classCreation_Schedules.models import Class
from django.utils import timezone

# Create your models here.


class Quiz(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    text = models.CharField(max_length=300)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
