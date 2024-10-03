from django.urls import path
from . import views

urlpatterns = [
    path('create_class/', views.create_class, name='create_class'),
    path('class/<int:class_id>/add_schedule/', views.add_schedule, name='add_schedule'),
    path('teacher-classes/', views.teacher_classes, name='teacher_classes'),
    path('edit-class/<int:class_id>', views.edit_class, name='edit_class'),
    path('delete-class/<int:class_id>', views.delete_class, name='delete_class'),
    path('class_detail_teacher/<int:class_id>', views.class_detail_teacher, name='class_detail_teacher'),
    path('class/<int:class_id>/schedule/edit/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('class/<int:class_id>/schedule/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),

]
