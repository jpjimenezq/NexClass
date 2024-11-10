from django.db import models
from classCreation_Schedules.models import Class
from users.models import User, Student, Teacher
from django.utils import timezone


class ClassChat(models.Model):
    class_instance = models.OneToOneField(Class, on_delete=models.CASCADE, related_name='chat', null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="class_chats")
    students = models.ManyToManyField(Student, related_name="class_chats_students")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

class PrivateChat(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="private_chats_professor")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="private_chats_student")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Chat between {self.teacher} and {self.student}"


class Message(models.Model):
    class_chat = models.ForeignKey(ClassChat, on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender}"