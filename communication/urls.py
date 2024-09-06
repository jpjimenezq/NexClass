from django.urls import path, include
from . import views

urlpatterns = [
    path('classes/', views.classes, name='student_classes'),  # Ruta para mostrar la página con las clases
    path('create-meet/<int:class_id>/', views.create_google_meet_link, name='create_meet'),
    path('add-favorite/<int:class_id>/', views.add_favorite, name='add_favorite'),
]
