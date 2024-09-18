from django.db import models
from users.models import Teacher, Student

class TeacherRating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'student')  # Un estudiante solo puede calificar a un profesor una vez
