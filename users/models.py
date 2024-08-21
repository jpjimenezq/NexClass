from django.db import models

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

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialties = models.TextField()
    biography = models.TextField()
    average_rating = models.FloatField(default=0.0)
    availability = models.CharField(
        max_length=50,
        choices=Availability.choices
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(
        max_length=50,
        choices=Mode.choices
    )

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Teacher, related_name='favorites')