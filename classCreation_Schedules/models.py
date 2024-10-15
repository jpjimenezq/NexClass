from django.db import models


# Create your models here.
class Class(models.Model):
    className = models.CharField(max_length=100)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    description = models.TextField()
    class_picture = models.ImageField(upload_to='class_photos/', default='class_photos/default_profile.png', null=True, blank=True)

    def __str__(self):
        return self.className


class Schedule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_obj.className} - {self.start_time} to {self.end_time}"



