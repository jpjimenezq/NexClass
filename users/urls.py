from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('loguout/', views.loguout, name='loguout'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
]