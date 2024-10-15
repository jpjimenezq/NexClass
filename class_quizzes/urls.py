from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/class/<int:class_id>/', views.quiz_list, name='quiz_list_by_class'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quizzes/create/<int:class_id>/', views.create_quiz, name='create_quiz_with_class'),

    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),  # Agrega preguntas al quiz

    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

]
