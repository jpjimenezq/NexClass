from django.contrib import admin

# Register your models here.

from .models import Message, PrivateChat, ClassChat



# Register your models here.
admin.site.register(Message)
admin.site.register(PrivateChat)

admin.site.register(ClassChat)
