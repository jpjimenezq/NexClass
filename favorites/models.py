from django.db import models
from users.models import Student, Teacher
from classCreation_Schedules.models import Class

class StudentFavoritesClasses(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)


class StudentFavoritesTeachers(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

# Create your models here.
