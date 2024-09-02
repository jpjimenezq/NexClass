from django.urls import path, include
from . import views

urlpatterns = [
    path('teachers/', views.teachers, name='teachers'),
]