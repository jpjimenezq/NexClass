from django.urls import path
from . import views

urlpatterns = [
    path('clases-inscritas/', views.clases_inscritas, name='clases_inscritas'),
    path('enroll-in-class/<int:class_id>/', views.enroll_in_class, name='enroll_in_class'),
    path('remove-class/<int:class_id>/', views.remove_class, name='remove_class'),
    path('mi-clase-inscrita/<int:class_id>/', views.mi_clase_inscrita, name='mi_clase_inscrita'),


]
