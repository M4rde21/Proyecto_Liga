from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from .models import Jugadores, Equipos, Planillas, PremiosEquipos, Partidos, Torneos, Temporadas, Categorias, TipoTorneos, TablaDePosiciones, TemporadasXTorneosXEquiposXJugadores, Tarjetas
from django.urls import reverse

# Create your views here.
def home(request):
    return HttpResponse('La Mejor Liga del Condado')

def registro_inicio(request):
    cantidad_jugadores = Jugadores.objects.count()
    cantidad_equipos = Equipos.objects.count()
    total_goles = Planillas.objects.aggregate(total_goles=Sum('goles'))['total_goles'] or 0
    cantidad_equipos_campeones = PremiosEquipos.objects.filter(id_premio_grupal=1).count()
    partidos_jugados = Partidos.objects.count()
    return render(request, 'inicio.html', {
        'cantidad_jugadores': cantidad_jugadores,
        'cantidad_equipos': cantidad_equipos,
        'total_goles': total_goles,
        'cantidad_equipos_campeones': cantidad_equipos_campeones,
        'partidos_jugados': partidos_jugados,
    })
    
def mostrar_torneos(request):
    # Obtener todos los torneos
    torneos = Torneos.objects.all()

    # Crear una lista para almacenar los datos formateados de los torneos
    torneos_datos = []

    # Recorrer cada torneo y obtener los datos necesarios
    for torneo in torneos:
        # Obtener la categoría y el tipo de torneo
        categoria = torneo.id_categoria.nombre_categoria if torneo.id_categoria else 'Sin categoría'
        tipo_torneo = torneo.id_tipo_torneo.nombre_tipo_torneo if torneo.id_tipo_torneo else 'Sin tipo'
        
        # Obtener el número de ediciones y temporadas
        ediciones = Temporadas.objects.filter(id_torneo=torneo).count()
        
        # Obtener los equipos y jugadores relacionados con este torneo mediante el modelo intermedio
        equipos_jugadores = TemporadasXTorneosXEquiposXJugadores.objects.filter(id_torneo=torneo)
        equipos = equipos_jugadores.values('id_equipo').distinct().count()  # Número de equipos únicos
        jugadores = equipos_jugadores.values('id_jugador').distinct().count()  # Número de jugadores únicos
        
        # Obtener el número de partidos para este torneo
        partidos = Partidos.objects.filter(id_torneo=torneo).count()

        # Añadir los datos del torneo a la lista
        torneos_datos.append({
            'id_torneo': torneo.id_torneo,
            'nombre_torneo': torneo.nombre_torneo,
            'categoria': categoria,
            'tipo_torneo': tipo_torneo,
            'año': torneo.año,
            'ediciones': ediciones,
            'partidos': partidos,  # Número de partidos asociados al torneo
            'equipos': equipos,  # Número de equipos
            'jugadores': jugadores,  # Número de jugadores
        })
    
    # Pasar los datos a la plantilla
    return render(request, 'torneos.html', {'torneos': torneos_datos})

def torneo_detalles(request, id_torneo):
    # Obtener el torneo específico
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    
    # Obtener las temporadas asociadas al torneo
    temporadas = Temporadas.objects.filter(id_torneo=torneo)
    
    # Obtener los partidos del torneo
    partidos = Partidos.objects.filter(id_torneo=torneo)
    
    # Opcional: Obtener los equipos que participaron en los partidos del torneo
    equipos = Equipos.objects.filter(
        id_equipo__in=partidos.values_list('id_equipo_1', flat=True)
    ).union(
        Equipos.objects.filter(id_equipo__in=partidos.values_list('id_equipo_2', flat=True))
    )
    
    # Contexto con la información del torneo, temporadas, partidos y equipos
    context = {
        'torneo': torneo,
        'temporadas': temporadas,
        'partidos': partidos,
        'equipos': equipos
    }
    
    return render(request, 'torneo_detalles.html', context)


def obtener_temporadas(request, id_torneo):
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    temporadas = Temporadas.objects.filter(id_torneo=torneo).order_by('-id_temporada')
    temporadas_data = list(temporadas.values('id_temporada', 'nombre_temporada', 'fecha_inicio'))
    return JsonResponse({'temporadas': temporadas_data})

def obtener_partido_destacado(request, id_torneo):
    # Intentar obtener el partido destacado
    partido_destacado = Partidos.objects.filter(
        id_torneo=id_torneo,
        destacado=1
    ).first()
    
    if not partido_destacado:
        # Si no hay partido destacado, obtener el último partido jugado
        partido_destacado = Partidos.objects.filter(
            id_torneo=id_torneo
        ).order_by('-fecha_partido', '-hora_partido').first()
    
    if partido_destacado:
        partido_data = {
            'id_partido': partido_destacado.id_partido,
            'id_equipo_1': partido_destacado.id_equipo_1.id_equipo,
            'id_equipo_2': partido_destacado.id_equipo_2.id_equipo,
            'fecha_partido': partido_destacado.fecha_partido,
            'hora_partido': partido_destacado.hora_partido
        }
        return JsonResponse({'partido_destacado': partido_data})
    else:
        return JsonResponse({'partido_destacado': None})
    
def obtener_tabla_posiciones(request, id_torneo, id_temporada):
    try:
        # Filtrar la tabla de posiciones según la temporada proporcionada y ordenar por puntos de forma descendente
        tabla = TablaDePosiciones.objects.filter(id_temporada=id_temporada).select_related('id_equipo').order_by('-puntos')

        # Convertir los datos a un formato JSON, incluyendo tarjetas amarillas y rojas
        data = list(tabla.values(
            'id_equipo',
            'id_equipo__nombre_equipo', 'id_equipo__foto_equipo',  # Foto del equipo incluida
            'partidos_jugados', 'partidos_ganados', 'partidos_empatados', 'partidos_perdidos',
            'goles_a_favor', 'goles_en_contra', 'diferencia_goles', 'puntos',
            'tarjetas_amarillas', 'tarjetas_rojas'  # Agregar campos de tarjetas
        ))

        # Devolver los datos en formato JSON
        return JsonResponse({'tabla_posiciones': data})

    except Exception as e:
        # Devolver un error en caso de que ocurra algún problema
        return JsonResponse({'error': str(e)}, status=500)
    
def obtener_ranking_goles_tarjetas(request, id_torneo, id_temporada):
    tipo = request.GET.get('tipo', 'goles')
    
    if tipo == 'goles':
        ranking = (Planillas.objects
            .filter(id_partido__id_temporada=id_temporada)
            .values('id_jugador__apellido_jugador', 'id_jugador__nombre_jugador', 'id_jugador__foto_jugador' , 'id_equipo__nombre_equipo', 'id_equipo__logo_equipo')
            .annotate(total=Sum('goles'))
            .order_by('-total')
            .values('id_jugador__nombre_jugador', 'id_jugador__apellido_jugador', 'id_jugador__foto_jugador', 'total' , 'id_equipo__nombre_equipo',  'id_equipo__logo_equipo'))
    
    elif tipo == 'tarjetas.amarillas':
        ranking = (Tarjetas.objects
            .filter(id_partido__id_temporada=id_temporada, tipo_tarjeta='amarilla')
            .values('id_jugador__nombre_jugador', 'id_jugador__apellido_jugador', 'id_jugador__foto_jugador')
            .annotate(total=Count('id_tarjeta'))
            .order_by('-total')
            .values('id_jugador__nombre_jugador', 'id_jugador__apellido_jugador', 'id_jugador__foto_jugador', 'total'))
    
    elif tipo == 'tarjetas.rojas':
        ranking = (Tarjetas.objects
            .filter(id_partido__id_temporada=id_temporada, tipo_tarjeta='roja')
            .values('id_jugador__nombre_jugador', 'id_jugador__apellido_jugador', 'id_jugador__foto_jugador')
            .annotate(total=Count('id_tarjeta'))
            .order_by('-total')
            .values('id_jugador__nombre_jugador', 'id_jugador__apellido_jugador', 'id_jugador__foto_jugador', 'total'))
    
    else:
        ranking = []

    return JsonResponse({'ranking': list(ranking)})

def equipo_detalles(request, id_equipo):
    # Cambiamos el campo a id_equipo
    equipo = get_object_or_404(Equipos, id_equipo=id_equipo)

    context = {
        'equipo': equipo,
    }
    return render(request, 'equipo_detalles.html', context)

def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')


def equipos(request):
    return render(request, 'equipos.html')
