from django.urls import path, include
from . import views

urlpatterns = [
    path('student/<int:student_id>/', views.Student_classes, name='student_classes'),
    path('Invitation/<int:student_id>/<int:teacher_id>/', views.Invitation, name='send_invitation'),

]
