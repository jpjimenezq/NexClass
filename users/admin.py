from django.contrib import admin
from .models import User
from .models import Teacher
from .models import Class
from .models import Favourites
from .models import Student

# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Favourites)
admin.site.register(Student)