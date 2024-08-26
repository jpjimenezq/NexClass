from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('loguout/', views.logout, name='logout'),
    path('favoritos/', views.favoritos, name='favoritos')
]