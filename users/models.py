from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import pickle
from embeddings_simmilarities.utils import generate_embedding, save_embedding_to_binary


# Create your models here.
# Opciones de tipo de usuario
class UserType(models.TextChoices):
    STUDENT = 'Student', 'Student'
    TEACHER = 'Teacher', 'Teacher'


# Opciones de disponibilidad
class Availability(models.TextChoices):
    FULL_TIME = 'Full-Time', 'Full-Time'
    PART_TIME = 'Part-Time', 'Part-Time'
    FLEXIBLE = 'Flexible', 'Flexible'


# Opciones de modalidad
class Mode(models.TextChoices):
    ONLINE = 'Online', 'Online'
    IN_PERSON = 'In-Person', 'In-Person'
    HYBRID = 'Hybrid', 'Hybrid'


class Specialties(models.TextChoices):
    MATHEMATICS = 'Mathematics', 'Mathematics'
    SCIENCE = 'Science', 'Science'
    LANGUAGES = 'Languages', 'Languages'
    HISTORY = 'History', 'History'
    GEOGRAPHY = 'Geography', 'Geography'
    MUSIC = 'Music', 'Music'
    ART = 'Art', 'Art'
    PHYSICAL_EDUCATION = 'Physical Education', 'Physical Education'
    COMPUTER_SCIENCE = 'Computer Science', 'Computer Science'
    ECONOMICS = 'Economics', 'Economics'
    PHILOSOPHY = 'Philosophy', 'Philosophy'
    ENGINEERING = 'Engineering', 'Engineering'
    PSYCHOLOGY = 'Psychology', 'Psychology'
    LAW = 'Law', 'Law'
    MEDICINE = 'Medicine', 'Medicine'
    OTHER = 'Other', 'Other'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile.png',
                                        null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_complete = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialities = models.CharField(
        max_length=50,
        choices=Specialties.choices
    )
    biography = models.TextField()
    description = models.TextField(default="No description provided.")
    average_rating = models.FloatField(default=0.0)
    availability = models.CharField(
        max_length=50,
        choices=Availability.choices
    )
    mode = models.CharField(
        max_length=50,
        choices=Mode.choices
    )
    embedding = models.BinaryField(blank=True, null=True)
    ciudad = models.CharField(max_length=150, default="Colombia")

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum([rating.rating for rating in ratings]) / ratings.count()
        return 0

    def set_embedding(self, emb_vector):
        self.embedding = save_embedding_to_binary(emb_vector)

    def get_embedding(self):
        return pickle.loads(self.embedding)

    def save(self, *args, **kwargs):
        # Combinación de los textos relevantes para generar el embedding
        combined_text = (
            f"Description: {self.description}. "
            f"Specialities: {self.specialities}. "
            f"Biography: {self.biography}. "
            f"Mode: {self.mode}. "
            f"Ciudad: {self.ciudad}. "
            f"Availability: {self.availability}. "
            f"Average rating: {self.average_rating}."
        )

        # Generar el embedding si es nuevo o si ha cambiado algún campo relevante
        if not self.embedding or self._state.adding:
            embedding = generate_embedding(combined_text)
            self.set_embedding(embedding)

        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Verificar si el usuario es estudiante
        if self.user.user_type != UserType.STUDENT:
            raise ValueError("Solo los estudiantes pueden enviar mensajes.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"
