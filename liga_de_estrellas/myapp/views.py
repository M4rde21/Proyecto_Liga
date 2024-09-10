from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from .models import Jugadores, Equipos, Planillas, PremiosEquipos, Partidos, Torneos, Temporadas, Categorias, TipoTorneos

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
        
        # Contar el número de ediciones, partidos y equipos (puedes ajustar estos métodos según sea necesario)
        ediciones = Temporadas.objects.filter(id_torneo=torneo).count()
        partidos = '10'  # Debes implementar la lógica para obtener el número real de partidos
        equipos = '10'  # Debes implementar la lógica para obtener los equipos participantes

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
            'logo_url': f'/static/images/{torneo.id_torneo}.png'  # Ajusta el camino al logo según tu estructura
        })
    
    # Pasar los datos a la plantilla
    return render(request, 'torneos.html', {'torneos': torneos_datos})

def torneo_detalles(request, id_torneo):
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    return render(request, 'torneo_detalles.html', {'torneo': torneo})

def obtener_temporadas(request, id_torneo):
    torneo = get_object_or_404(Torneos, id_torneo=id_torneo)
    # Ordenar por id_temporada en orden descendente
    temporadas = Temporadas.objects.filter(id_torneo=torneo).order_by('-id_temporada')
    temporadas_data = list(temporadas.values('id_temporada', 'nombre_temporada', 'fecha_inicio'))
    return JsonResponse({'temporadas': temporadas_data})


def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')


