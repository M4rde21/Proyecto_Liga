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
    path('torneo/<int:id_torneo>/partido_destacado/', views.obtener_partido_destacado, name='obtener_partido_destacado'),
    path('torneo/<int:id_torneo>/tabla_posiciones/<int:id_temporada>/', views.obtener_tabla_posiciones, name='obtener_tabla_posiciones'),
    path('torneo/<int:id_torneo>/ranking/<int:id_temporada>/', views.obtener_ranking_goles_tarjetas, name='obtener_ranking_goles_tarjetas'),
    path('equipo/<int:id_equipo>/', views.equipo_detalles, name='equipo_detalles'),
]
