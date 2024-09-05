from django.urls import path, include
from . import views

urlpatterns = [
    path('crear-llamada/<int:class_id>/', views.create_meet_and_send_emails, name='create_meet'),
]
