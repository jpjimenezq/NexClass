from django.db import models
from users.models import Student
from classCreation_Schedules.models import Class
from django.utils import timezone
# Create your models here.


class EnrolledClasses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(default=timezone.now)


class HistoryClasses(models.Model):
    ACTION_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('removed', 'Removed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(default=timezone.now)
