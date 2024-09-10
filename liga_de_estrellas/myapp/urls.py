# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.registro_inicio, name='inicio'),
    path('torneos/', views.mostrar_torneos, name='mostrar_torneos'),
    path('reglamentos/', views.reglamentos, name='reglamentos'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),
    path('torneo/<int:id_torneo>/', views.torneo_detalles, name='torneo_detalles'),
    path('torneo/<int:id_torneo>/obtener_temporadas/', views.obtener_temporadas, name='obtener_temporadas'),
]