from django.urls import path, include
from . import views

urlpatterns = [
    path('classes/', views.classes, name='student_classes'),  # Ruta para mostrar la página con las clases
    path('generate_meet_link/<int:class_id>/', views.generate_meet_link, name='generate_meet_link'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),

]
