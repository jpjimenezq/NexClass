from django.urls import path
from . import views
from teacher_blog import views as blog_views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/classes/', views.student_classes, name='student_classes'),
    path('complete_profile/', views.complete_profile_view, name='complete_profile'),
    path('edit_profile/', views.modificar_perfil, name='edit_profile'),
    path('home_teacher/', views.home_teacher, name='home_teacher'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('my_profile_student/', views.my_profile_student, name='my_profile_student'),
    path('my_profile_teacher/', views.my_profile_teacher, name='my_profile_teacher'),
    path('edit_teacher_profile/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('blog/create/', blog_views.create_blog_post, name='create_blog_post'),
    path('blog/edit/<int:post_id>/', blog_views.edit_blog_post, name='edit_blog_post'),
]
