from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from .models import Jugadores, Equipos, Planillas, PremiosEquipos, Partidos, Torneos, Temporadas, Categorias, TipoTorneos, TemporadasXTorneosXEquiposXJugadores

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
    # Obtén el objeto de la temporada basado en el id
    temporada = get_object_or_404(Temporadas, id_temporada=id_temporada)
    # Obtén el objeto del torneo relacionado con esta temporada
    torneo = temporada.id_torneo
    
    # Obtener los equipos y jugadores participando en la temporada
    participantes = TemporadasXTorneosXEquiposXJugadores.objects.filter(id_temporada=temporada)
    equipos_participantes = Equipos.objects.filter(id_equipo__in=participantes.values_list('id_equipo', flat=True))
    jugadores_participantes = Jugadores.objects.filter(id_jugador__in=participantes.values_list('id_jugador', flat=True))
    
    # Pasa los datos a la plantilla
    return render(request, 'temporada_detalles.html', {
        'temporada': temporada,
        'torneo': torneo,
        'equipos_participantes': equipos_participantes,
        'jugadores_participantes': jugadores_participantes
    })

def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')


