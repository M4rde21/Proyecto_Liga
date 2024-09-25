from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F, Case, When, IntegerField, Q, Count
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
from datetime import datetime, date, time, timedelta
from .models import Jugadores, Equipos, Planillas, PremiosEquipos, Partidos, Torneos, Temporadas, Categorias, TipoTorneos, TemporadasXTorneosXEquiposXJugadores, TablaDePosiciones, Tarjetas, Figuras, Fechas, Resultados

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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige a la página de inicio después del login exitoso
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
        else:
            form.add_error(None, 'Formulario inválido.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
    
def mostrar_torneos(request):
    # Obtener todos los torneos
    torneos = Torneos.objects.all()

    # Crear una lista para almacenar los datos formateados de los torneos
    torneos_datos = []

    for torneo in torneos:
        # Obtener la categoría y el tipo de torneo
        categoria = torneo.id_categoria.nombre_categoria if torneo.id_categoria else 'Sin categoría'
        tipo_torneo = torneo.id_tipo_torneo.nombre_tipo_torneo if torneo.id_tipo_torneo else 'Sin tipo'
        
        # Contar el número de ediciones
        ediciones = Temporadas.objects.filter(id_torneo=torneo).count()

        # Contar el número de equipos únicos participantes en cualquier temporada del torneo
        equipos = TemporadasXTorneosXEquiposXJugadores.objects.filter(
            id_temporada__id_torneo=torneo
        ).values_list('id_equipo', flat=True).distinct().count()

        # Contar el número de partidos
        partidos = Partidos.objects.filter(
            id_temporada__id_torneo=torneo
        ).count()  # Ajusta el filtro según tu modelo de Partidos

        # Añadir los datos del torneo a la lista
        torneos_datos.append({
            'id_torneo': torneo.id_torneo,
            'nombre_torneo': torneo.nombre_torneo,
            'categoria': categoria,
            'tipo_torneo': tipo_torneo,
            'año': torneo.año,
            'ediciones': ediciones,
            'partidos': partidos,
            'equipos': equipos,
            'logo_url': '/static/images/Logo_Liga.png'  # Ajusta el camino al logo según tu estructura
        })
    
    # Pasar los datos a la plantilla
    return render(request, 'torneos.html', {'torneos': torneos_datos})

def torneo_detalles(request, id_torneo):
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    return render(request, 'torneo_detalles.html', {'torneo': torneo})

def lista_temporadas(request, id_torneo):
    # Obtén el objeto del torneo basado en el id
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    # Obtén las temporadas relacionadas con el torneo, ordenadas por fecha de inicio en orden descendente
    temporadas = Temporadas.objects.filter(id_torneo=torneo).order_by('-fecha_inicio')
    # Renderiza la plantilla con los datos del torneo y las temporadas ordenadas
    return render(request, 'lista_temporadas.html', {'torneo': torneo, 'temporadas': temporadas})



def temporada_detalles(request, id_temporada):
    # Obtener la temporada actual
    temporada = get_object_or_404(Temporadas, id_temporada=id_temporada)
    torneo = temporada.id_torneo

    # Obtener la temporada anterior y siguiente en relación a la temporada actual
    temporadas = Temporadas.objects.filter(id_torneo=torneo).order_by('fecha_inicio')
    temporada_anterior = temporadas.filter(fecha_inicio__lt=temporada.fecha_inicio).last()
    temporada_siguiente = temporadas.filter(fecha_inicio__gt=temporada.fecha_inicio).first()

    # Obtener la tabla de posiciones para la temporada actual
    tabla_posiciones = TablaDePosiciones.objects.filter(id_temporada=temporada).order_by('-puntos', '-diferencia_goles')
    
    # Obtener los equipos participantes
    equipos_participantes = TemporadasXTorneosXEquiposXJugadores.objects.filter(
        id_temporada=temporada
    ).values('id_equipo__nombre_equipo').distinct()

    # Obtener el total de partidos jugados
    total_partidos_jugados = Partidos.objects.filter(
        id_temporada=temporada,
        resultados__isnull=False
    ).count()
    total_partidos_jugados = total_partidos_jugados if total_partidos_jugados else 0

    # Calcular el total de partidos ganados en la temporada
    total_partidos_ganados = Partidos.objects.filter(
        id_temporada=temporada
    ).annotate(
        equipo_1_ganador=Case(
            When(resultados__goles_equipo_1__gt=F('resultados__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        ),
        equipo_2_ganador=Case(
            When(resultados__goles_equipo_2__gt=F('resultados__goles_equipo_1'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_ganados=Sum('equipo_1_ganador') + Sum('equipo_2_ganador')
    )['total_ganados']
    total_partidos_ganados = total_partidos_ganados if total_partidos_ganados else 0

    # Calcular el total de partidos empatados en la temporada
    total_partidos_empatados = Partidos.objects.filter(
        id_temporada=temporada
    ).annotate(
        empate=Case(
            When(resultados__goles_equipo_1=F('resultados__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_empatados=Sum('empate')
    )['total_empatados']
    total_partidos_empatados = total_partidos_empatados if total_partidos_empatados else 0

    # Calcular el total de partidos perdidos en la temporada
    total_partidos_perdidos = Partidos.objects.filter(
        id_temporada=temporada
    ).annotate(
        equipo_1_perdedor=Case(
            When(resultados__goles_equipo_1__lt=F('resultados__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        ),
        equipo_2_perdedor=Case(
            When(resultados__goles_equipo_2__lt=F('resultados__goles_equipo_1'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_perdidos=Sum('equipo_1_perdedor') + Sum('equipo_2_perdedor')
    )['total_perdidos']
    total_partidos_perdidos = total_partidos_perdidos if total_partidos_perdidos else 0

    # Calcular el total de goles en la temporada
    total_goles = Partidos.objects.filter(
        id_temporada=temporada
    ).aggregate(
        total_goles=Sum('resultados__goles_equipo_1') + Sum('resultados__goles_equipo_2')
    )['total_goles']
    total_goles = total_goles if total_goles else 0

    # Calcular el total de tarjetas amarillas en la temporada
    total_tarjetas_amarillas = Tarjetas.objects.filter(
        id_partido__id_temporada=temporada,
        tipo_tarjeta='Amarilla'
    ).count()
    total_tarjetas_amarillas = total_tarjetas_amarillas if total_tarjetas_amarillas else 0

    # Calcular el total de tarjetas rojas en la temporada
    total_tarjetas_rojas = Tarjetas.objects.filter(
        id_partido__id_temporada=temporada,
        tipo_tarjeta='Roja'
    ).count()
    total_tarjetas_rojas = total_tarjetas_rojas if total_tarjetas_rojas else 0

    # Inicializar el diccionario para almacenar estadísticas de cada equipo
    estadisticas_equipo = {}

    # Actualizar estadísticas para cada equipo en la tabla de posiciones
    for posicion in tabla_posiciones:
        equipo_id = posicion.id_equipo.id_equipo

        # Calcular los goles a favor para el equipo
        goles_a_favor = Partidos.objects.filter(
            id_temporada=temporada,
            id_equipo_1=posicion.id_equipo
        ).aggregate(total_goles=Sum('resultados__goles_equipo_1'))['total_goles'] or 0
        
        goles_a_favor += Partidos.objects.filter(
            id_temporada=temporada,
            id_equipo_2=posicion.id_equipo
        ).aggregate(total_goles=Sum('resultados__goles_equipo_2'))['total_goles'] or 0

        # Calcular los goles en contra para el equipo
        goles_en_contra = Partidos.objects.filter(
            id_temporada=temporada,
            id_equipo_1=posicion.id_equipo
        ).aggregate(total_goles=Sum('resultados__goles_equipo_2'))['total_goles'] or 0
        
        goles_en_contra += Partidos.objects.filter(
            id_temporada=temporada,
            id_equipo_2=posicion.id_equipo
        ).aggregate(total_goles=Sum('resultados__goles_equipo_1'))['total_goles'] or 0

        # Calcular los partidos ganados para el equipo
        partidos_ganados = Partidos.objects.filter(
            id_temporada=temporada
        ).annotate(
            equipo_1_ganador=Case(
                When(resultados__goles_equipo_1__gt=F('resultados__goles_equipo_2'), then=1),
                default=0,
                output_field=IntegerField()
            ),
            equipo_2_ganador=Case(
                When(resultados__goles_equipo_2__gt=F('resultados__goles_equipo_1'), then=1),
                default=0,
                output_field=IntegerField()
            )
        ).filter(
            Q(id_equipo_1=posicion.id_equipo, equipo_1_ganador=1) |
            Q(id_equipo_2=posicion.id_equipo, equipo_2_ganador=1)
        ).count()

        # Calcular los partidos perdidos para el equipo
        partidos_perdidos = Partidos.objects.filter(
            id_temporada=temporada
        ).annotate(
            equipo_1_perdedor=Case(
                When(resultados__goles_equipo_1__lt=F('resultados__goles_equipo_2'), then=1),
                default=0,
                output_field=IntegerField()
            ),
            equipo_2_perdedor=Case(
                When(resultados__goles_equipo_2__lt=F('resultados__goles_equipo_1'), then=1),
                default=0,
                output_field=IntegerField()
            )
        ).filter(
            Q(id_equipo_1=posicion.id_equipo, equipo_1_perdedor=1) |
            Q(id_equipo_2=posicion.id_equipo, equipo_2_perdedor=1)
        ).count()

        # Calcular los partidos empatados para el equipo
        partidos_empatados = Partidos.objects.filter(
            id_temporada=temporada
        ).annotate(
            empate=Case(
                When(resultados__goles_equipo_1=F('resultados__goles_equipo_2'), then=1),
                default=0,
                output_field=IntegerField()
            )
        ).filter(
            Q(id_equipo_1=posicion.id_equipo, empate=1) |
            Q(id_equipo_2=posicion.id_equipo, empate=1)
        ).count()

        # Calcular las tarjetas amarillas para los jugadores del equipo
        jugadores = Jugadores.objects.filter(
            id_jugador__in=TemporadasXTorneosXEquiposXJugadores.objects.filter(
                id_temporada=temporada,
                id_equipo=posicion.id_equipo
            ).values_list('id_jugador', flat=True)
        )
        
        tarjetas_amarillas = Tarjetas.objects.filter(
            id_jugador__in=jugadores,
            tipo_tarjeta='amarilla'
        ).count()

        # Calcular las tarjetas rojas para los jugadores del equipo
        tarjetas_rojas = Tarjetas.objects.filter(
            id_jugador__in=jugadores,
            tipo_tarjeta='roja'
        ).count()

        # Calcular la diferencia de goles
        diferencia_goles = goles_a_favor - goles_en_contra

        # Calcular los puntos
        puntos = partidos_ganados * 3 + partidos_empatados * 1

        # Actualizar los campos en la tabla de posiciones
        posicion.goles_a_favor = goles_a_favor
        posicion.goles_en_contra = goles_en_contra
        posicion.diferencia_goles = diferencia_goles
        posicion.partidos_ganados = partidos_ganados
        posicion.partidos_perdidos = partidos_perdidos
        posicion.partidos_empatados = partidos_empatados
        posicion.puntos = puntos
        posicion.tarjetas_amarillas = tarjetas_amarillas
        posicion.tarjetas_rojas = tarjetas_rojas
        posicion.save()

    # Obtener el ranking de los 5 jugadores con más goles en la temporada actual
    ranking_jugadores = (Planillas.objects.filter(
        id_partido__id_temporada=temporada
    ).values(
        'id_jugador__apellido_jugador',
        'id_jugador__nombre_jugador',
        'id_jugador__temporadasxtorneosxequiposxjugadores__id_equipo__nombre_equipo'
    ).annotate(
        total_goles=Sum('goles')
    ).filter(total_goles__gt=0)  # Filtrar jugadores con goles
    .order_by('-total_goles')[:5])  # Limitar a los primeros 5 jugadores si hay más

    # Obtener el ranking de los 5 jugadores con más tarjetas amarillas en la temporada actual
    ranking_tarjetas_amarillas = (Tarjetas.objects.filter(
        id_partido__id_temporada=temporada
    ).filter(tipo_tarjeta='amarilla')
    .values(
        'id_jugador__apellido_jugador',
        'id_jugador__nombre_jugador',
        'id_jugador__temporadasxtorneosxequiposxjugadores__id_equipo__nombre_equipo'
    ).annotate(
        total_tarjetas_amarillas=Count('id_tarjeta')
    ).order_by('-total_tarjetas_amarillas')[:5])

    # Obtener el ranking de los 5 jugadores con más tarjetas rojas en la temporada actual
    ranking_tarjetas_rojas = (Tarjetas.objects.filter(
        id_partido__id_temporada=temporada
    ).filter(tipo_tarjeta='roja')
    .values(
        'id_jugador__apellido_jugador',
        'id_jugador__nombre_jugador',
        'id_jugador__temporadasxtorneosxequiposxjugadores__id_equipo__nombre_equipo'
    ).annotate(
        total_tarjetas_rojas=Count('id_tarjeta')
    ).order_by('-total_tarjetas_rojas')[:5])
    
    # Obtener el ranking de los 5 jugadores más veces elegidos como "figura" en la temporada actual
    ranking_figuras = (Figuras.objects.filter(
        id_partido__id_temporada=temporada
    ).values(
        'id_jugador__apellido_jugador',
        'id_jugador__nombre_jugador',
        'id_jugador__temporadasxtorneosxequiposxjugadores__id_equipo__nombre_equipo'
    ).annotate(
        total_figuras=Count('id_figura')
    ).order_by('-total_figuras')[:5])
    
    # Obtener los goles recibidos por cada equipo cuando juegan como locales
    goles_recibidos_local = Partidos.objects.filter(id_temporada=temporada).values('id_equipo_1').annotate(total_goles_recibidos=Sum('resultados__goles_equipo_2'))

    # Obtener los goles recibidos por cada equipo cuando juegan como visitantes
    goles_recibidos_visitante = Partidos.objects.filter(id_temporada=temporada).values('id_equipo_2').annotate(total_goles_recibidos=Sum('resultados__goles_equipo_1'))

    # Combinar los resultados en un diccionario
    goles_recibidos = defaultdict(int)
    for item in goles_recibidos_local:
        goles_recibidos[item['id_equipo_1']] += item['total_goles_recibidos'] or 0  # Usar or 0 para manejar None
    for item in goles_recibidos_visitante:
        goles_recibidos[item['id_equipo_2']] += item['total_goles_recibidos'] or 0  # Usar or 0 para manejar None

    # Convertir el diccionario a una lista de tuplas y ordenar por goles recibidos
    ranking_equipos_menos_goles = sorted(goles_recibidos.items(), key=lambda x: x[1])

    # Obtener los nombres de los equipos
    equipos = Equipos.objects.filter(id_equipo__in=[equipo[0] for equipo in ranking_equipos_menos_goles])
    equipos_dict = {equipo.id_equipo: equipo.nombre_equipo for equipo in equipos}

    # Preparar los datos para la plantilla
    ranking_equipos_menos_goles = [(equipos_dict[equipo_id], goles) for equipo_id, goles in ranking_equipos_menos_goles]
    
    # Obtener las fechas de los partidos en orden descendente por fecha de creación
    fechas_partidos = Fechas.objects.filter(id_temporada=temporada).order_by('-id_fecha')

    # Obtener los partidos agrupados por fecha y ordenados por hora
    fechas_y_partidos = []
    fecha_mas_proxima = None
    diferencia_mas_cercana = timedelta.max  # Inicializar con el máximo valor de diferencia de tiempo
    now = datetime.now().date()  # Convertir a datetime.date
    
    for fecha in fechas_partidos:
        partidos = Partidos.objects.filter(id_fecha=fecha).select_related('id_equipo_1', 'id_equipo_2').order_by('hora_partido')
        
        for partido in partidos:
            resultado = Resultados.objects.filter(id_partido=partido).first()
            partido.resultado = f"{resultado.goles_equipo_1} - {resultado.goles_equipo_2}" if resultado else "VS"
        
        fechas_y_partidos.append((fecha, partidos))
    
        # Calcular la diferencia de días entre la fecha del partido y la fecha actual
        for partido in partidos:
            diferencia = abs(partido.fecha_partido - now)
            if diferencia < diferencia_mas_cercana:
                diferencia_mas_cercana = diferencia
                fecha_mas_proxima = fecha
    
    # Determinar la fecha a mostrar
    fecha_a_mostrar = fecha_mas_proxima

    # Renderizar la plantilla con los datos necesarios
    return render(request, 'temporada_detalles.html', {
        'temporada': temporada,
        'torneo': torneo,
        'tabla_posiciones': tabla_posiciones,
        'temporada_anterior': temporada_anterior,
        'temporada_siguiente': temporada_siguiente,
        'ranking_jugadores': ranking_jugadores,
        'ranking_tarjetas_amarillas': ranking_tarjetas_amarillas,
        'ranking_tarjetas_rojas': ranking_tarjetas_rojas,
        'ranking_figuras': ranking_figuras,
        'ranking_equipos_menos_goles': ranking_equipos_menos_goles,
        'equipos_participantes': equipos_participantes,
        'total_partidos_jugados': total_partidos_jugados,
        'total_partidos_ganados': total_partidos_ganados,
        'total_partidos_empatados': total_partidos_empatados,
        'total_partidos_perdidos': total_partidos_perdidos,
        'total_goles': total_goles,
        'total_tarjetas_amarillas': total_tarjetas_amarillas,
        'total_tarjetas_rojas': total_tarjetas_rojas,
        'fechas_partidos': fechas_partidos,
        'fechas_y_partidos': fechas_y_partidos,
        'fecha_a_mostrar': fecha_a_mostrar,
    })
    

def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')


