# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.inicio, name='inicio'),
    path('torneos/', views.torneos, name='torneos'),
    path('reglamentos/', views.reglamentos, name='reglamentos'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),

]
