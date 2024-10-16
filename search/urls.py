from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/<int:teacher_id>/', views.teachers_detail, name='teachers_detail'),
    path('chat/<int:teacher_id>/', views.chat, name='chat'),
    path('send_message/<int:teacher_id>/', views.send_message, name='send_message'),
]
