from django.contrib import admin
from .models import StudentFavoritesTeachers
from .models import StudentFavoritesClasses

# Register your models here.

admin.site.register(StudentFavoritesClasses)
admin.site.register(StudentFavoritesTeachers)
