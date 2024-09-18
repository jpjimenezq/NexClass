from django.urls import path
from . import views

urlpatterns = [
    path('create_class/', views.create_class, name='create_class'),
    path('class/<int:class_id>/add_schedule/', views.add_schedule, name='add_schedule'),
]
