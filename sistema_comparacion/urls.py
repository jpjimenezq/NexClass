from django.urls import path
from . import views

urlpatterns = [
    path('comparacion/', views.seleccionar_comparacion, name='seleccionar_comparacion'),
    path('comparar/<str:tipo>/', views.seleccionar_elementos, name='comparar_elementos'),
    path('mostrar_comparacion/<str:tipo>/<str:seleccionados>/', views.mostrar_comparacion, name='mostrar_comparacion'),

]
