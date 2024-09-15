# myapp/urls.py
from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.inicio, name='inicio'),
    path('torneos/', views.torneos, name='torneos'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.signout, name='logout'),
    path('reglamentos/', views.reglamentos, name='reglamentos'),
    path('contacto/', views.contacto, name='contacto'),
    path('usuario/', views.usuario, name='usuario'),
    path('torneos_adm/', views.torneos_adm, name='torneos_adm'),
    path('torneos_adm/crear_torneo/', views.crear_torneo, name='crear_torneo'),
    path('torneos_adm/<int:id_torneo>/', views.edit_torneo, name='edit_torneo'),
    path('torneos_adm/<int:id_torneo>/delete', views.delete_torneo, name='delete_torneo'),
    path('temporadas_adm/', views.temporadas_adm, name='temporadas_adm'),
    path('temporadas_adm/crear_temporada/', views.crear_temporada, name='crear_temporada'),
    path('temporadas_adm/<int:id_temporada>/', views.edit_temporada, name='edit_temporada'),
    path('temporadas_adm/<int:id_temporada>/delete', views.delete_temporada, name='delete_temporada'),
]
