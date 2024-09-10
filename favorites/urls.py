from django.urls import path, include
from . import views

urlpatterns = [
    path('add_favorite_class/<int:class_id>/', views.add_favorite_class, name='add_favorite_class'),
    path('add_favorite_teacher/<int:teacher_id>/', views.add_favorite_teacher, name='add_favorite_teacher'),
    path('favoritos/', views.favorites_view, name='favoritos'),

]
