from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/classes/', views.student_classes, name='student_classes'),  # La URL con el name
    path('complete_profile/', views.complete_profile_view, name='complete_profile'),
    path('edit_profile/', views.modificar_perfil, name='edit_profile'),  # Ruta para modificar perfil
]
