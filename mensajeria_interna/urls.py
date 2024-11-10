from django.urls import path, include
from . import views

urlpatterns = [
    path('clase/<int:chat_id>/mensajes/', views.class_chat_detail, name='class_chat_detail'),
    path('class_chat/<int:chat_id>/send/', views.send_class_message, name='send_class_message'),
    path('chats/', views.chat_list, name='chat_list'),
    path('private-chat/<int:chat_id>/', views.private_chat_detail, name='private_chat_detail'),
    path('start-private-chat/<int:other_user_id>/', views.get_or_create_private_chat, name='get_or_create_private_chat'),
]




