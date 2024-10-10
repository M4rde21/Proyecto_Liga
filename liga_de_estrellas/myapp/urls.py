# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.inicio, name='inicio'),
    path('torneos/', views.torneos, name='torneos'),
    path('login/', views.login_view, name='login'),
    path('reglamentos/', views.reglamentos, name='reglamentos'),
    path('contacto/', views.contacto, name='contacto'),
    path('torneos_adm/', views.torneos_adm, name='torneos_adm'),
    path('torneos_adm/crear_torneo/', views.crear_torneo, name='crear_torneo'),
    path('torneos_adm/<int:id_torneo>/', views.edit_torneo, name='edit_torneo'),
    path('torneos_adm/<int:id_torneo>/delete', views.delete_torneo, name='delete_torneo'),
    path('temporadas_adm/', views.temporadas_adm, name='temporadas_adm'),
    path('temporadas_adm/crear_temporada/', views.crear_temporada, name='crear_temporada'),
    path('temporadas_adm/<int:id_temporada>/', views.edit_temporada, name='edit_temporada'),
    path('temporadas_adm/<int:id_temporada>/delete', views.delete_temporada, name='delete_temporada'),
    path('categorias_adm/', views.categorias_adm, name='categorias_adm'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('categorias_adm/<int:id_categoria>/', views.edit_categoria, name='edit_categoria'),
    path('categorias_adm/<int:id_categoria>/delete', views.delete_categoria, name='delete_categoria'),
    path('tipotorneos_adm/', views.tipotorneos_adm, name='tipotorneos_adm'),
    path('crear_tipotorneo/', views.crear_tipotorneo, name='crear_tipotorneo'),
    path('tipotorneos_adm/<int:id_tipo_torneo>/', views.edit_tipotorneo, name='edit_tipotorneo'),
    path('tipotorneos_adm/<int:id_tipo_torneo>/delete', views.delete_tipotorneo, name='delete_tipotorneo'),
    path('accounts/logout/', views.signout, name='logout'),

]
