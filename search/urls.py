from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/<int:teacher_id>/', views.teachers_detail, name='teachers_detail')
]
