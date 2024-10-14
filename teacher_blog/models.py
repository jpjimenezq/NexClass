# teacher_blog/models.py
from django.db import models
from users.models import Teacher

class BlogPost(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
