from django.contrib import admin
from .models import User
from .models import Teacher
from .models import Student



# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)

admin.site.register(Student)

