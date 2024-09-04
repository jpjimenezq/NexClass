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

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_profile.png', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    profile_complete = models.BooleanField(default=False)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialties = models.CharField(
        max_length=50,
        choices=Specialties.choices
    )
    biography = models.TextField()
    average_rating = models.FloatField(default=0.0)
    availability = models.CharField(
        max_length=50,
        choices=Availability.choices
    )
    mode = models.CharField(
        max_length=50,
        choices=Mode.choices
    )


class Class(models.Model):
    className = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    description = models.TextField()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Teacher, related_name='favorites')
    classes = models.ManyToManyField(Class, related_name='student')

class Favourites(models.Model):
    estudiante = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    clase = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    profesor = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)