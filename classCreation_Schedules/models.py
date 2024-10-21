from django.db import models
import pickle
from embeddings_simmilarities.utils import generate_embedding, save_embedding_to_binary


# Create your models here.
class Class(models.Model):
    className = models.CharField(max_length=100)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    description = models.TextField()
    class_picture = models.ImageField(upload_to='class_photos/', default='class_photos/default_profile.png', null=True, blank=True)
    embedding = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.className

    def set_embedding(self, emb_vector):
        self.embedding = save_embedding_to_binary(emb_vector)

    def get_embedding(self):
        return pickle.loads(self.embedding)

    def save(self, *args, **kwargs):
        combined_text = (
            f"Class Name: {self.className}. "
            f"Description: {self.description}. "
        )

        if not self.embedding or self._state.adding:
            embedding = generate_embedding(combined_text)
            self.set_embedding(embedding)

        super().save(*args, **kwargs)


class Schedule(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_obj.className} - {self.start_time} to {self.end_time}"



