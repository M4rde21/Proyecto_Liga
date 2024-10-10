from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login, name='login'),
    path('resumen/', views.resumen, name='resumen'),
    path('jugadores/', views.lista_jugadores, name='jugadores'),
    path('jugadores/crear/', views.crear_jugador, name='crear_jugador'),
    path('jugadores/<int:id_jugador>/', views.editar_jugador, name='editar_jugador'),
    path('jugadores/<int:id_jugador>/eliminar', views.eliminar_jugador, name='eliminar_jugador'),
    path('equipos/', views.equipos_lista, name='equipos'),
    path('equipos/crear/', views.equipo_crear, name='equipo_crear'),
    path('equipos/<int:id_equipo>/', views.equipo_editar, name='equipo_editar'),
    path('entrenadores/', views.entrenadores_lista, name='entrenadores'),
    path('entrenadores/crear/', views.entrenador_crear, name='entrenador_crear'),
    path('entrenadores/<int:id_entrenador>/', views.entrenador_editar, name='entrenador_editar'),
    path('torneos/', views.torneos, name='torneos'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
