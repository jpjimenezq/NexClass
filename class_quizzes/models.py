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


class QuizResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()  # Guardará el puntaje obtenido
    total_questions = models.IntegerField()  # Número total de preguntas
    correct_answers = models.IntegerField()  # Número de respuestas correctas
    completed_at = models.DateTimeField(auto_now_add=True)  # Fecha en que el estudiante completó el quiz
