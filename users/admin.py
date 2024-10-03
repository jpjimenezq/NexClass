from django.contrib import admin
from .models import User
from .models import Teacher
from .models import StudentFavoritesClasses
from .models import Student
from .models import StudentFavoritesTeachers


# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(StudentFavoritesClasses)
admin.site.register(Student)
admin.site.register(StudentFavoritesTeachers)
