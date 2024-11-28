from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden,HttpRequest
from .models import Equipo, Torneo, Temporada, Categoria,TipoTorneo, Jugador, Equipo, Entrenador, PremiosGrupal, PremiosIndividual, Grupo, TemporadaXTorneoXGrupoXEquipoXJugador, Fecha, Partido, Resultado, Planilla, Reglamento,PremioEquipo, PremioJugador, TablaDePosicion,Traspaso
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm, CrearPremioGrupalForm, CrearPremioIndividualForm,CrearZonaForm, CrearFechaForm, CrearPartidoForm, ResultadoForm, PlanillaForm, CrearReglamentoForm, CrearTraspasoForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory
from django.template.loader import get_template,render_to_string
from xhtml2pdf import pisa
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.db.models import Q,Sum, F, Case, When, IntegerField,Count, Exists, OuterRef
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, time, timedelta
from collections import defaultdict
from django.utils.timezone import now
from io import BytesIO
from zipfile import ZipFile






def inicio(request):
    cantidad_jugadores = Jugador.objects.count()
    cantidad_equipos = Equipo.objects.count()
    total_goles = Planilla.objects.aggregate(total_goles=Sum('goles'))['total_goles'] or 0
    cantidad_equipos_campeones = PremioEquipo.objects.filter(id_premio_grupal=1).count()
    partidos_jugados = Resultado.objects.count()
    return render(request, 'usuario/inicio.html', {
        'cantidad_jugadores': cantidad_jugadores,
        'cantidad_equipos': cantidad_equipos,
        'total_goles': total_goles,
        'cantidad_equipos_campeones': cantidad_equipos_campeones,
        'partidos_jugados': partidos_jugados,
    })


def barra(request):
    return render(request, 'usuario/barra.html')

def buscar_entidades(request):
    """Vista para realizar búsquedas dinámicas de jugadores y equipos."""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Verificar si es AJAX
        termino = request.GET.get('q', '').strip()  # Remover espacios en blanco

        if not termino:
            return JsonResponse({"results": []})
        # Buscar en Jugadores
        jugadores = Jugador.objects.filter(
            Q(nombre_jugador__icontains=termino) | 
            Q(apellido_jugador__icontains=termino)|
            Q(dni_jugador__icontains=termino)
        ).filter(activo_jugador=True)

        # Buscar en Equipos
        equipos = Equipo.objects.filter(
            Q(nombre_equipo__icontains=termino)
        )

        # Preparar resultados combinados
        resultados = []

        # Agregar jugadores al resultado
        resultados.extend([
            {
                "id": f"jugador-{jugador.id}",  # Prefijo para diferenciar
                "text": f"Jugador: {jugador.nombre_jugador} {jugador.apellido_jugador} (DNI: {jugador.dni_jugador})",
                "image" : jugador.foto_jugador.url if jugador.foto_jugador else ""
            }
            for jugador in jugadores
        ])

        # Agregar equipos al resultado
        resultados.extend([
            {
                "id": f"equipo-{equipo.id}",  # Prefijo para diferenciar
                "text": f"Equipo: {equipo.nombre_equipo}",
                "image": equipo.logo_equipo.url if equipo.logo_equipo else ""
            }
            for equipo in equipos
        ])

        return JsonResponse({"results": resultados})

    return JsonResponse({"results": []})

def login_view(request):
    return render(request, 'login.html')



     
def signout(request):
    logout(request)
    return redirect('inicio')

def torneos(request):
    torneos = Torneo.objects.all()
    return render(request, 'usuario/torneos.html', {'torneos': torneos})

def reglamentos(request):
    return render(request, 'usuario/reglamentos.html')

def contacto(request):
    return render(request, 'usuario/contacto.html')

def lista_equipos(request):
    
    equipos = Equipo.objects.all()

def resumen(request):
    return render(request, 'administracion/resumen.html')

def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'administracion/jugadores.html', {'jugadores': jugadores})


def buscar_jugadores(request):
    """Vista para realizar búsquedas dinámicas de jugadores."""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        termino = request.GET.get('q', '')  # Obtener el término de búsqueda
        jugadores = Jugador.objects.filter(
            Q(nombre_jugador__icontains=termino) |  # Buscar por nombre
            Q(apellido_jugador__icontains=termino) |  # Buscar por apellido
            Q(dni_jugador__icontains=termino)  # Buscar por DNI
        ).filter(activo_jugador=True)  # Opcional: Filtrar solo jugadores activos
        
        # Preparar resultados para Select2
        resultados = [
            {
                "id": jugador.id,
                "text": f"{jugador.nombre_jugador} {jugador.apellido_jugador} (DNI: {jugador.dni_jugador})"
            }
            for jugador in jugadores
        ]
        return JsonResponse({"results": resultados})

    return JsonResponse({"results": []})



def crear_jugador(request):
    if request.method == 'GET':
        return render(request, 'administracion/crear_jugador.html', {
            'form': CrearJugadorForm()
        })
    else:
        form = CrearJugadorForm(request.POST, request.FILES)
        if form.is_valid():
            jugador = Jugador(
                nombre_jugador=form.cleaned_data['nombre_jugador'],
                apellido_jugador=form.cleaned_data['apellido_jugador'],
                dni_jugador=form.cleaned_data['dni_jugador'],
                fecha_nac_jugador=form.cleaned_data['fecha_nac_jugador'],
                foto_jugador=form.cleaned_data['foto_jugador'],
                activo_jugador=form.cleaned_data['activo_jugador'],
            )
            jugador.save()

            return redirect('jugadores')
        else:
            return render(request, 'administracion/crear_jugador.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })


def editar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)

    if request.method == 'GET':
        form = CrearJugadorForm(initial={
            'nombre_jugador': jugador.nombre_jugador,
            'apellido_jugador': jugador.apellido_jugador,
            'dni_jugador': jugador.dni_jugador,
            'fecha_nac_jugador': jugador.fecha_nac_jugador.strftime('%Y-%m-%d'),
            'foto_jugador': jugador.foto_jugador,
            'activo_jugador': jugador.activo_jugador
        })
        return render(request, 'administracion/editar_jugador.html', {'form': form, 'jugador': jugador})

    else:
        form = CrearJugadorForm(request.POST, request.FILES)
        
        if form.is_valid():
            jugador.nombre_jugador = form.cleaned_data['nombre_jugador']
            jugador.apellido_jugador = form.cleaned_data['apellido_jugador']
            jugador.dni_jugador = form.cleaned_data['dni_jugador']
            jugador.fecha_nac_jugador = form.cleaned_data['fecha_nac_jugador']
            if 'foto_jugador' in request.FILES:
                jugador.foto_jugador = form.cleaned_data['foto_jugador']
            elif form.cleaned_data['foto_jugador'] is None:
                pass
            else:
                jugador.foto_jugador.delete(save=False)
                jugador.foto_jugador = None
            
            jugador.save()
            return redirect('jugadores')
        else:
            return render(request, 'administracion/editar_jugador.html', {
                'form': form,
                'jugador': jugador,
                'error': 'Por favor introduce datos válidos.'
            })


def eliminar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    if request.method == 'POST':
        jugador.delete()
        return redirect('jugadores')

def crear_torneo(request):
    form = TorneoForm(request.POST)
    if form.is_valid():

        torneo = Torneo()
        torneo.nombre_torneo = form.cleaned_data['nombre_torneo']
        torneo.id_categoria = form.cleaned_data["id_categoria"]
        torneo.id_tipo_torneo = form.cleaned_data["id_tipo_torneo"]
        torneo.año = form.cleaned_data["año"]
        torneo.save()
        return redirect('torneos_adm')
        
    else:
        return render(request, 'administracion/crear_torneo.html', {'form': form})
    return render(request, 'administracion/crear_torneo.html', {'form': form})

   
def torneos_adm(request):
    torneos = Torneo.objects.all()

    context = {
        'torneos': torneos,
    }
    
    return render(request, 'administracion/torneos_adm.html', context)






def edit_torneo(request, id_torneo):
    torneo = get_object_or_404(Torneo, pk=id_torneo)

    if request.method == 'POST':
        form=TorneoForm(request.POST)
        if form.is_valid():
            torneo.nombre_torneo = form.cleaned_data['nombre_torneo']
            torneo.id_categoria = form.cleaned_data["id_categoria"]
            torneo.id_tipo_torneo = form.cleaned_data["id_tipo_torneo"]
            torneo.año = form.cleaned_data["año"]
            torneo.save()
            return redirect('torneos_adm')
    else:
        form = TorneoForm(initial={'nombre_torneo': torneo.nombre_torneo, 'id_categoria':torneo.id_categoria, 'id_tipo_torneo':torneo.id_tipo_torneo, 'año':torneo.año })
            
    return render(request, 'administracion/edit_torneo.html', {
                 'torneo': torneo,
                 'form' : form
                })
   

        
def delete_torneo(request, id_torneo):
    torneo=get_object_or_404(Torneo, pk=id_torneo)
    if request.method == 'POST':
        torneo.delete()
        return redirect('torneos_adm')

def crear_temporada(request):
    form = TemporadasForm(request.POST)
    if form.is_valid():

        temporada = Temporada()
        temporada.nombre_temporada = form.cleaned_data['nombre_temporada']
        temporada.id_torneo = form.cleaned_data["id_torneo"]
        temporada.fecha_inicio = form.cleaned_data["fecha_inicio"]
        temporada.fecha_final = form.cleaned_data["fecha_final"]
        temporada.save()
        return redirect('temporadas_adm')
        
    else:
        return render(request, 'administracion/crear_temporada.html', {'form': form})
    return render(request, 'administracion/crear_temporada.html', {'form': form})
    


def temporadas_adm(request):
    temporadas = Temporada.objects.all()
    form_crear = TemporadasForm()  # Formulario para el modal de creación

    # Añadir un formulario de edición para cada temporada al queryset
    for temporada in temporadas:
        temporada.form_editar = TemporadasForm(initial={
            'nombre_temporada': temporada.nombre_temporada,
            'id_torneo': temporada.id_torneo,
            'fecha_inicio': temporada.fecha_inicio,
            'fecha_final': temporada.fecha_final,
        })
        
    context = {
        'temporadas': temporadas,
        'form_crear': form_crear,
    }
    
    return render(request, 'administracion/temporadas_adm.html', context)


def edit_temporada(request, id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)

    if request.method == 'POST':
        form=TemporadasForm(request.POST)
        if form.is_valid():
            temporada.nombre_temporada = form.cleaned_data['nombre_temporada']
            temporada.id_torneo = form.cleaned_data["id_torneo"]
            temporada.fecha_inicio = form.cleaned_data["fecha_inicio"]
            temporada.fecha_final = form.cleaned_data["fecha_final"]
            temporada.save()
            return redirect('temporadas_adm')
    else:
        form = TemporadasForm(initial={
        'nombre_temporada': temporada.nombre_temporada,
        'id_torneo': temporada.id_torneo,
        'fecha_inicio': temporada.fecha_inicio.strftime('%Y-%m-%d') if temporada.fecha_inicio else '',
        'fecha_final': temporada.fecha_final.strftime('%Y-%m-%d') if temporada.fecha_final else ''
    })
    return render(request, 'administracion/edit_temporada.html', {
                 'temporada': temporada,
                 'form' : form
                })
   
        

def delete_temporada(request, id_temporada):
    temporada=get_object_or_404(Temporada, pk=id_temporada)
    if request.method == 'POST':
        temporada.delete()
        return redirect('temporadas_adm')


def gestion_temporada(request, id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    return render(request, 'administracion/gestion_temporada.html', {'temporada': temporada})




def zonas(request, id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zonas = Grupo.objects.filter(id_temporada=temporada)

    equipos = list(Equipo.objects.all())

    for zona in zonas:
        zona.equipos_importados = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_jugador=None,
            id_grupo=zona
        ).values_list('id_equipo', flat=True)

    return render(request, 'administracion/zonas.html', {
        'temporada': temporada,
        'zonas': zonas,
        'equipos': equipos,
    })





def zona_crear(request, id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    if request.method == 'POST':
        form = CrearZonaForm(request.POST)
        if form.is_valid():
            zona = Grupo(
                nombre_grupo=form.cleaned_data['nombre_grupo'],
                id_temporada=temporada
            )
            zona.save()
            return redirect('gestion_temporada', id_temporada=id_temporada)
    else:
        form = CrearZonaForm()
    return render(request, 'administracion/zona_crear.html', {'form': form, 'temporada': temporada})



def zona_editar(request, id_temporada, id_zona):
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=id_temporada)
    if request.method == 'POST':
        form = CrearZonaForm(request.POST)
        if form.is_valid():
            zona.nombre_grupo = form.cleaned_data['nombre_grupo']
            zona.save()
            return redirect('zonas', id_temporada=id_temporada)
    else:
        form = CrearZonaForm(initial={'nombre_grupo': zona.nombre_grupo})
    return render(request, 'administracion/zona_editar.html', {'form': form, 'temporada': zona.id_temporada})



def zona_eliminar(request, id_temporada, id_zona):
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=id_temporada)
    if request.method == 'POST':
        zona.delete()
        return redirect('zonas', id_temporada=id_temporada)



def importar_equipos_zona(request, id_temporada, id_zona):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=temporada)
    equipos = Equipo.objects.all()

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        equipo = get_object_or_404(Equipo, pk=equipo_id)

        relacion = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_equipo=equipo,
            id_grupo=zona,
            id_jugador=None
        ).exists()

        if not relacion:
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
                id_temporada=temporada,
                id_torneo=temporada.id_torneo,
                id_equipo=equipo,
                id_grupo=zona,
                id_jugador=None
            )

        return redirect('zonas', id_temporada=id_temporada)

    return render(request, 'administracion/importar_equipos_zona.html', {
        'zona': zona,
        'temporada': temporada,
        'equipos': equipos
    })

def equipo_importado(request, id_temporada, id_zona, id_equipo):
    # Filtrar la relación para obtener solo la que corresponde al equipo, temporada y zona específicos
    relacion = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo
    ).first()

    if relacion is None:
        return render(request, 'administracion/error.html', {
            'mensaje': 'No se encontró la relación entre la temporada, la zona y el equipo especificados.'
        })

    equipo = relacion.id_equipo 
    equipos = Equipo.objects.all()

    # Obtener todos los jugadores importados para este equipo
    jugadores_importados = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=equipo,
        id_jugador__isnull=False
    ).select_related('id_jugador')

    for jugador in jugadores_importados:
        jugador.premios = PremioJugador.objects.filter(
            id_temporada=id_temporada,
            id_torneo=relacion.id_temporada.id_torneo,
            id_jugador=jugador.id_jugador  # Esto asegura que solo se obtienen los premios de ese jugador específico
        ).select_related('id_premio_individual')



    # Mantener la consulta de premios asignados al equipo
    premios_asignados = PremioEquipo.objects.filter(
        id_temporada=id_temporada,
        id_torneo=relacion.id_temporada.id_torneo,
        id_equipo=equipo
    )

    return render(request, 'administracion/equipo_importado.html', {
        'equipo': equipo,
        'temporada': relacion.id_temporada,
        'zona': relacion.id_grupo,
        'equipos': equipos,
        'jugadores_importados': jugadores_importados,
        'premios_asignados': premios_asignados,  # Premios asignados al equipo
    })



def equipo_importado_cambiar(request, id_temporada, id_zona, id_equipo):
    # Obtener la relación actual de manera segura
    relacion = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo
    ).first()  # Usamos first() para evitar el error si hay más de una relación

    if relacion is None:
        # Manejar el caso en que no se encontró la relación
        messages.error(request, 'No se encontró la relación entre la temporada, la zona y el equipo especificados.')
        return redirect(reverse('zonas', args=[id_temporada]))

    equipos = Equipo.objects.all()

    if request.method == 'POST':
        nuevo_equipo_id = request.POST.get('equipo')
        nuevo_equipo = get_object_or_404(Equipo, pk=nuevo_equipo_id)

        # Obtener la instancia de Temporada y Grupo correspondientes
        temporada = get_object_or_404(Temporada, pk=id_temporada)
        grupo = get_object_or_404(Grupo, pk=id_zona, id_temporada=temporada)
        torneo = temporada.id_torneo

        if nuevo_equipo != relacion.id_equipo:
            # Eliminar todas las relaciones existentes del equipo actual en esta zona
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo=relacion.id_equipo
            ).delete()

            # Crear una nueva relación con el equipo seleccionado
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
                id_temporada=temporada,  # Instancia de Temporada
                id_torneo=torneo,         # Instancia de Torneo obtenida a través de Temporada
                id_grupo=grupo,           # Instancia de Grupo
                id_equipo=nuevo_equipo,   # Instancia de Equipo
                id_jugador=None           # Nueva relación sin jugador
            )

            messages.success(request, f'Equipo cambiado exitosamente a {nuevo_equipo}.')
            return redirect(reverse('zonas', args=[id_temporada]))

        else:
            messages.info(request, 'El equipo seleccionado ya es el equipo actual.')

    # Renderiza un formulario para seleccionar un nuevo equipo
    return render(request, 'administracion/equipo_importado_cambiar.html', {
        'relacion': relacion,
        'equipos': equipos,
        'temporada': id_temporada,
        'zona': id_zona,
        'equipo': id_equipo
    })






def equipo_importado_eliminado(request, id_temporada, id_zona, id_equipo):
    # Filtramos todas las relaciones que coinciden con los parámetros
    relaciones = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo
    )

    # Verificamos si hay relaciones que eliminar
    if relaciones.exists():
        relaciones.delete()  # Eliminar todas las relaciones que coincidan

    return redirect('zonas', id_temporada=id_temporada)






def importar_jugador_equipo(request, id_temporada, id_zona, id_equipo):
    # Obtener la temporada y la zona
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=temporada)

    # Obtener todos los jugadores disponibles
    jugadores_disponibles = Jugador.objects.all()

    # Obtener la instancia del equipo
    equipo_instance = get_object_or_404(Equipo, pk=id_equipo)

    if request.method == 'POST':
        jugador_id = request.POST.get('jugador')
        jugador = get_object_or_404(Jugador, pk=jugador_id)

        # Crear una nueva relación sin modificar la relación existente con jugador=NULL
        TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_grupo=zona,
            id_equipo=equipo_instance,
            id_jugador=jugador  # Nueva relación con el jugador seleccionado
        )

        messages.success(request, 'Jugador importado correctamente en el equipo de la zona en la temporada actual.')
        return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))

    return render(request, 'administracion/importar_jugador_equipo.html', {
        'zona': zona,
        'temporada': temporada,
        'jugadores': jugadores_disponibles,
        'equipo': equipo_instance
    })


def eliminar_jugador_equipo(request, id_temporada, id_zona, id_equipo, id_jugador):
    # Obtener la temporada y el jugador
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    jugador = get_object_or_404(Jugador, pk=id_jugador)

    # Buscar y eliminar todas las relaciones del jugador con el equipo en todas las zonas de la misma temporada
    relaciones = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=temporada,
        id_equipo=id_equipo,
        id_jugador=jugador
    )

    if relaciones.exists():
        relaciones.delete()
        # Mostrar un mensaje de éxito
        messages.success(request, 'El jugador ha sido eliminado de todas las zonas en las que el equipo está presente para la temporada actual.')
    else:
        messages.error(request, 'No se encontró la relación del jugador en las zonas del equipo para la temporada actual.')

    # Redirigir a la página de equipo importado
    return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))


def asignar_premio_grupal(request, id_temporada, id_zona, id_equipo):
    # Obtener los objetos necesarios
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    torneo = temporada.id_torneo  # Obtener el torneo a través de la temporada
    zona = get_object_or_404(Grupo, pk=id_zona)

    # Obtener los premios grupales disponibles
    premios_disponibles = PremiosGrupal.objects.all()

    if request.method == 'POST':
        premio_id = request.POST.get('premio_grupal')
        premio_grupal = get_object_or_404(PremiosGrupal, pk=premio_id)

        # Verificar si el equipo ya tiene asignado un premio grupal
        tiene_premio_grupal = PremioEquipo.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo,
            id_equipo=equipo,
            id_premio_grupal__isnull=False  # Verifica cualquier premio grupal
        ).exists()

        if tiene_premio_grupal:
            messages.error(request, 'El equipo ya tiene un premio grupal asignado y no puede recibir más.')
        else:
            # Crear la asignación de premio al equipo
            PremioEquipo.objects.create(
                id_premio_grupal=premio_grupal,
                id_temporada=temporada,
                id_torneo=torneo,
                id_equipo=equipo
            )
            messages.success(request, 'Premio asignado correctamente al equipo.')

            # Redirigir de vuelta a la URL del equipo importado, incluyendo id_zona
            return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))

    return render(request, 'administracion/asignar_premio_grupal.html', {
        'temporada': temporada,
        'torneo': torneo,
        'equipo': equipo,
        'zona': zona,
        'premios_disponibles': premios_disponibles
    })


def eliminar_premio_grupal(request, id_temporada, id_zona, id_equipo):
    # Obtener los objetos necesarios
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    torneo = temporada.id_torneo  # Obtener el torneo a través de la temporada
    zona = get_object_or_404(Grupo, pk=id_zona)

    # Filtrar y eliminar todos los premios grupales asignados al equipo en la temporada y torneo especificados
    premios_a_eliminar = PremioEquipo.objects.filter(
        id_temporada=temporada,
        id_torneo=torneo,
        id_equipo=equipo
    )

    if premios_a_eliminar.exists():
        premios_a_eliminar.delete()
    else:
        pass

    # Redirigir de vuelta a la URL del equipo importado, incluyendo id_zona
    return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))


def asignar_premio_individual(request, id_temporada, id_zona, id_equipo, id_jugador):
    # Obtener los objetos necesarios basados en los argumentos proporcionados
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    zona = get_object_or_404(Grupo, pk=id_zona)

    # Continuar con la lógica para asignar un premio al jugador
    premios_disponibles = PremiosIndividual.objects.all()

    if request.method == 'POST':
        premio_id = request.POST.get('premio_individual')
        premio_individual = get_object_or_404(PremiosIndividual, pk=premio_id)

        # Verificar cuántos premios ya tiene el jugador
        num_premios_asignados = PremioJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_jugador=jugador
        ).count()

        if num_premios_asignados >= 2:
            messages.error(request, 'El jugador ya tiene el máximo de 2 premios asignados.')
        else:
            # Verificar si el premio ya fue asignado al jugador
            existe_premio = PremioJugador.objects.filter(
                id_temporada=temporada,
                id_torneo=temporada.id_torneo,
                id_jugador=jugador,
                id_premio_individual=premio_individual
            ).exists()

            if existe_premio:
                messages.error(request, 'Este premio ya ha sido asignado al jugador.')
            else:
                # Crear la asignación de premio al jugador
                PremioJugador.objects.create(
                    id_premio_individual=premio_individual,
                    id_temporada=temporada,
                    id_torneo=temporada.id_torneo,
                    id_jugador=jugador
                )
                messages.success(request, 'Premio asignado correctamente al jugador.')
                return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))

    return render(request, 'administracion/asignar_premio_individual.html', {
        'temporada': temporada,
        'equipo': equipo,
        'jugador': jugador,
        'zona': zona,
        'premios_disponibles': premios_disponibles
    })

def eliminar_premio_individual(request, id_temporada, id_zona, id_equipo, id_jugador):
    # Obtener los objetos necesarios a partir de los IDs pasados en la URL
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zona = get_object_or_404(Grupo, pk=id_zona)
    equipo = get_object_or_404(Equipo, pk=id_equipo)

    # Eliminar todos los premios asignados a este jugador
    premios = PremioJugador.objects.filter(id_jugador=jugador)

    if premios.exists():
        premios.delete()  # Eliminar todos los premios del jugador
        messages.success(request, 'Todos los premios del jugador han sido eliminados correctamente.')
    else:
        messages.info(request, 'El jugador no tiene premios asignados.')

    # Redirigir a la página del equipo importado con los parámetros correctos
    return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))






def categorias_adm(request):
    categorias = Categoria.objects.all()
    return render(request, 'administracion/categorias_adm.html', {
        'categorias': categorias
    })



    
def crear_categoria(request):
    form = CategoriasForm(request.POST)
    if form.is_valid():

        categoria = Categoria()
        categoria.nombre_categoria = form.cleaned_data['nombre_categoria']
        categoria.save()
        return redirect('categorias_adm')
        
    else:
        return render(request, 'administracion/crear_categoria.html', {'form': form})
    return render(request, 'administracion/crear_categoria.html', {'form': form})


def edit_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, pk=id_categoria)

    if request.method == 'POST':
        form=CategoriasForm(request.POST)
        if form.is_valid():
            categoria.nombre_categoria = form.cleaned_data['nombre_categoria']
            categoria.save()
            return redirect('categorias_adm')
    else:
        form = CategoriasForm(initial={'nombre_categoria': categoria.nombre_categoria})
            
    return render(request, 'administracion/edit_categoria.html', {
                 'categoria': categoria,
                 'form' : form
                })



def delete_categoria(request, id_categoria):
    categoria=get_object_or_404(Categoria, pk=id_categoria)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias_adm')
    

def tipotorneos_adm(request):
    tipotorneos = TipoTorneo.objects.all()
    return render(request, 'administracion/tipotorneo_adm.html', {
        'tipotorneos': tipotorneos
    })

def crear_tipotorneo(request):
    if request.method == 'POST':
        form = TipoTorneoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tipotorneos_adm')  
    else:
        form = TipoTorneoForm()
    return render(request, 'administracion/crear_tipotorneo.html', {'form': form})

def edit_tipotorneo(request, id_tipo_torneo):
    if request.method == 'GET':
        tipotorneo = get_object_or_404(TipoTorneo, pk=id_tipo_torneo)
        form=TipoTorneoForm(instance=tipotorneo)
        return render(request, 'administracion/edit_tipotorneo.html', {
        'tipotorneo': tipotorneo,
        'form' : form
        })
    else:
        try:
            tipotorneo=get_object_or_404(TipoTorneo, pk=id_tipo_torneo)
            form=TipoTorneoForm(request.POST, instance=tipotorneo)
            form.save()
            return redirect('tipotorneos_adm')
        except ValueError:
            return render(request, 'administracion/tipotorneos_adm.html', {
                'tipotorneo': tipotorneo,
                'form' : form,
                'error' : "Error al actualizar datos"
            })
        

def delete_tipotorneo(request, id_tipo_torneo):
    tipotorneo=get_object_or_404(TipoTorneo, pk=id_tipo_torneo)
    if request.method == 'POST':
        tipotorneo.delete()
        return redirect('tipotorneos_adm')
        

def equipos_lista(request):
    equipos = Equipo.objects.all()
    return render(request, 'administracion/equipos.html', {'equipos': equipos})

def equipo_crear(request):
    if request.method == 'GET':
        return render(request, 'administracion/equipo_crear.html', {
            'form': CrearEquipoForm
        })
    else:
        form = CrearEquipoForm(request.POST, request.FILES)
        if form.is_valid():
            equipo = Equipo(
                nombre_equipo=form.cleaned_data['nombre_equipo'],
                logo_equipo=form.cleaned_data['logo_equipo']
            )
            
            equipo.save()
            return redirect('equipos')
        else:
            return render(request, 'administracion/equipo_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
            
def equipo_editar(request, id_equipo):
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    
    if request.method == 'GET':
        form = CrearEquipoForm(initial={
            'nombre_equipo': equipo.nombre_equipo,
            'logo_equipo': equipo.logo_equipo
        })
        return render(request, 'administracion/equipo_editar.html' ,{'form': form, 'equipo': equipo})
    
    else:
        form = CrearEquipoForm(request.POST, request.FILES)
        
        if form.is_valid():
            equipo.nombre_equipo=form.cleaned_data['nombre_equipo']
            if 'logo_equipo' in request.FILES:
                equipo.logo_equipo=form.cleaned_data['logo_equipo']
            elif form.cleaned_data['logo_equipo'] is None:
                pass
            else:
                equipo.logo_equipo.delete(save=False)
                equipo.logo_equipo = None
            
            equipo.save()
    
            return redirect('equipos') 
        else:
            return render(request, 'administracion/equipo_editar.html', {
                'form': form,
                'equipo': equipo,
                'error': 'Por favor introduce datos válidos.'
            })

def entrenadores_lista(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'administracion/entrenadores.html', {'entrenadores': entrenadores})

def entrenador_crear(request):
    if request.method == 'GET':
        return render(request, 'administracion/entrenador_crear.html', {
            'form': CrearEntrenadorForm
        })
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES)
        if form.is_valid():
            entrenador = Entrenador(
                nombre_entrenador=form.cleaned_data['nombre_entrenador'],
                apellido_entrenador=form.cleaned_data['apellido_entrenador'],
                dni_entrenador=form.cleaned_data['dni_entrenador'],
                fecha_nac_entrenador=form.cleaned_data['fecha_nac_entrenador'],
                foto_entrenador=form.cleaned_data['foto_entrenador']
            )
            entrenador.save()
            
            return redirect('entrenadores')
        else:
            return render(request, 'administracion/entrenador_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })

def entrenador_editar(request, id_entrenador):
    entrenador = get_object_or_404(Entrenador, pk=id_entrenador)

    if request.method == 'GET':
        form = CrearEntrenadorForm(initial={
            'nombre_entrenador': entrenador.nombre_entrenador,
            'apellido_entrenador': entrenador.apellido_entrenador,
            'dni_entrenador': entrenador.dni_entrenador,
            'fecha_nac_entrenador': entrenador.fecha_nac_entrenador.strftime('%Y-%m-%d'),
            'foto_entrenador': entrenador.foto_entrenador
        })
        return render(request, 'administracion/entrenador_editar.html', {'form': form, 'entrenador': entrenador})
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES)
        if form.is_valid():
            entrenador.nombre_entrenador = form.cleaned_data['nombre_entrenador']
            entrenador.apellido_entrenador = form.cleaned_data['apellido_entrenador']
            entrenador.dni_entrenador = form.cleaned_data['dni_entrenador']
            entrenador.fecha_nac_entrenador = form.cleaned_data['fecha_nac_entrenador']
            
            if 'foto_entrenador' in request.FILES:
                entrenador.foto_entrenador = form.cleaned_data['foto_entrenador']
            elif form.cleaned_data['foto_entrenador'] is None:
                pass
            else:
                entrenador.foto_entrenador.delete(save=False)
                entrenador.foto_entrenador = None
                
            entrenador.save()
            return redirect('entrenadores')
        else:
            return render(request, 'administracion/entrenador_editar.html', {
                'form': form,
                'entrenador': entrenador,
                'error': 'Por favor introduce datos válidos.'
            })


def premios_grupal(request):
    premios = PremiosGrupal.objects.all()
    return render(request, 'administracion/premios_grupal.html', {
        'premios': premios
    })

def crear_premio_grupal(request):
    if request.method == 'GET':
        return render(request, 'administracion/crear_premio_grupal.html', {
            'form': CrearPremioGrupalForm
        })
    else:
        form = CrearPremioGrupalForm(request.POST, request.FILES)
        if form.is_valid():
            premiogrupal = PremiosGrupal(
                nombre_premio_grupal=form.cleaned_data['nombre_premio_grupal'],
                foto_premio_grupal=form.cleaned_data['foto_premio_grupal']
            )
            premiogrupal.save()
            
            return redirect('premios_grupal')
        else:
            return render(request, 'administracion/crear_premio_grupal.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
    

def edit_premio_grupal(request, id_premio_grupal):
    premiogrupal = get_object_or_404(PremiosGrupal, pk=id_premio_grupal)

    if request.method == 'GET':
        form = CrearPremioGrupalForm(initial={
            'nombre_premio_grupal': premiogrupal.nombre_premio_grupal,
            'foto_premio_grupal': premiogrupal.foto_premio_grupal
        })
        return render(request, 'administracion/edit_premio_grupal.html', {'form': form, 'premiogrupal': premiogrupal})
    else:
        form = CrearPremioGrupalForm(request.POST, request.FILES)
        if form.is_valid():
            premiogrupal.nombre_premio_grupal = form.cleaned_data['nombre_premio_grupal']
            
            if 'foto_premio_grupal' in request.FILES:
                # Si hay una nueva foto, la actualizamos
                premiogrupal.foto_premio_grupal = form.cleaned_data['foto_premio_grupal']
            elif form.cleaned_data['foto_premio_grupal'] is None:
                # Si no hay una nueva foto y el campo está vacío, no cambiamos la imagen
                pass
            else:
                # Si el campo fue enviado vacío explícitamente, borramos la foto actual
                premiogrupal.foto_premio_grupal.delete(save=False)
                premiogrupal.foto_premio_grupal = None
                
            premiogrupal.save()
            return redirect('premios_grupal')
        else:
            return render(request, 'administracion/edit_premio_grupal.html', {
                'form': form,
                'premiogrupal': premiogrupal,
                'error': 'Por favor introduce datos válidos.'
            })
    

def delete_premio_grupal(request, id_premio_grupal):
    premiogrupal=get_object_or_404(PremiosGrupal, pk=id_premio_grupal)
    if request.method == 'POST':
        premiogrupal.delete()
        return redirect('premios_grupal')


def premios_individual(request):
    premios = PremiosIndividual.objects.all()
    return render(request, 'administracion/premios_individual.html', {
        'premios': premios
    })


def crear_premio_individual(request):
    if request.method == 'GET':
        return render(request, 'administracion/crear_premio_individual.html', {
            'form': CrearPremioIndividualForm
        })
    else:
        form = CrearPremioIndividualForm(request.POST, request.FILES)
        if form.is_valid():
            premioindividual = PremiosIndividual(
                nombre_premio_individual=form.cleaned_data['nombre_premio_individual'],
                foto_premio_individual=form.cleaned_data['foto_premio_individual']
            )
            premioindividual.save()
            
            return redirect('premios_individual')
        else:
            return render(request, 'administracion/crear_premio_individual.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
        

def edit_premio_individual(request, id_premio_individual):
    premioindividual = get_object_or_404(PremiosIndividual, pk=id_premio_individual)

    if request.method == 'GET':
        form = CrearPremioIndividualForm(initial={
            'nombre_premio_individual': premioindividual.nombre_premio_individual,
            'foto_premio_individual': premioindividual.foto_premio_individual
        })
        return render(request, 'administracion/edit_premio_individual.html', {'form': form, 'premioindividual': premioindividual})
    else:
        form = CrearPremioIndividualForm(request.POST, request.FILES)
        if form.is_valid():
            premioindividual.nombre_premio_individual = form.cleaned_data['nombre_premio_individual']
            
            if 'foto_premio_individual' in request.FILES:
                # Si hay una nueva foto, la actualizamos
                premioindividual.foto_premio_individual = form.cleaned_data['foto_premio_individual']
            elif form.cleaned_data['foto_premio_individual'] is None:
                # Si no hay una nueva foto y el campo está vacío, no cambiamos la imagen
                pass
            else:
                # Si el campo fue enviado vacío explícitamente, borramos la foto actual
                premioindividual.foto_premio_individual.delete(save=False)
                premioindividual.foto_premio_individual = None
                
            premioindividual.save()
            return redirect('premios_individual')
        else:
            return render(request, 'administracion/edit_premio_individual.html', {
                'form': form,
                'premioindividual': premioindividual,
                'error': 'Por favor introduce datos válidos.'
            })
        
def delete_premio_individual(request, id_premio_individual):
    premioindividual=get_object_or_404(PremiosIndividual, pk=id_premio_individual)
    if request.method == 'POST':
        premioindividual.delete()
        return redirect('premios_individual')



def fechas(request, id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fechas = Fecha.objects.filter(id_temporada=temporada)

    equipos = list(Equipo.objects.all())
    partidos = Partido.objects.filter(id_temporada=temporada)

    for fecha in fechas:
        fecha.partidos_listados = partidos.filter(id_fecha=fecha).select_related('id_equipo_1', 'id_equipo_2')

    return render(request, 'administracion/fechas.html', {
        'temporada': temporada,
        'fechas': fechas,
        'equipos': equipos,
    })



    
def crear_fecha(request,id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    if request.method == 'POST':
        form = CrearFechaForm(request.POST)
        if form.is_valid():
            fecha = Fecha(
                nombre_fecha=form.cleaned_data['nombre_fecha'],
                id_temporada=temporada  # Asocia la temporada actual
            )
            fecha.save()
            return redirect('fechas', id_temporada=id_temporada)
    else:
        form = CrearFechaForm()

    return render(request, 'administracion/crear_fecha.html', {'form': form, 'temporada': temporada})
    

def edit_fecha(request,id_temporada, id_fecha):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha, id_temporada=temporada) 

    if request.method == 'POST':
        form = CrearFechaForm(request.POST)
        if form.is_valid():
            fecha.nombre_fecha = form.cleaned_data['nombre_fecha']
            fecha.save()
            return redirect('fechas', id_temporada=id_temporada)
    else:
        form = CrearFechaForm(initial={'nombre_fecha': fecha.nombre_fecha})

    return render(request, 'administracion/edit_fecha.html', {
        'temporada': temporada,  
        'fecha': fecha,
        'form': form,
    })
    


def delete_fecha(request, id_temporada, id_fecha):
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    
    if request.method == 'POST':
        fecha.delete()
        
        return redirect('fechas', id_temporada=id_temporada)

    return render(request, 'administracion/delete_fecha.html', {'fecha': fecha, 'temporada': id_temporada})

def partidos(request,id_temporada, id_fecha):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partidos = Partido.objects.filter(id_temporada=temporada, id_fecha=fecha)  
    return render(request, 'administracion/partidos.html', {
        'partidos': partidos,
        'temporada': temporada,  
        'fecha' : fecha,
    })

def crear_partido(request, id_temporada, id_fecha):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    torneo = temporada.id_torneo

    # Filtrar los grupos correspondientes a la temporada y torneo actual
    grupos = Grupo.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo
        ).values('id_grupo')
    ).distinct()

    # Filtrar los equipos que pertenecen a esos grupos, temporada y torneo
    equipos = Equipo.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo,
            id_grupo__in=grupos
        ).values('id_equipo')
    ).distinct()

    if request.method == 'POST':
        form = CrearPartidoForm(request.POST)
        form.fields['id_equipo_1'].queryset = equipos
        form.fields['id_equipo_2'].queryset = equipos
        form.fields['id_grupo'].queryset = grupos

        if form.is_valid():
            equipo_1 = form.cleaned_data['id_equipo_1']
            equipo_2 = form.cleaned_data['id_equipo_2']

            # Verificar que los equipos no sean el mismo
            if equipo_1 == equipo_2:
                form.add_error('id_equipo_2', 'El equipo 2 no puede ser el mismo que el equipo 1.')
            else:
                partido = Partido(
                    id_temporada=temporada,
                    id_fecha=fecha,
                    id_torneo=torneo,
                    id_equipo_1=equipo_1,
                    id_equipo_2=equipo_2,
                    id_predio=form.cleaned_data['id_predio'],
                    id_grupo=form.cleaned_data['id_grupo'],
                    fecha_partido=form.cleaned_data['fecha_partido'],
                    hora_partido=form.cleaned_data['hora_partido'],
                    destacado=form.cleaned_data['destacado']
                )
                partido.save()
                return redirect('fechas', id_temporada=id_temporada)
    else:
        form = CrearPartidoForm()
        form.fields['id_equipo_1'].queryset = equipos
        form.fields['id_equipo_2'].queryset = equipos
        form.fields['id_grupo'].queryset = grupos

    return render(request, 'administracion/crear_partido.html', {
        'form': form,
        'temporada': temporada,
        'fecha': fecha
    })


def edit_partido(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido)

    # Filtrar los grupos correspondientes a la temporada y torneo actual
    torneo = temporada.id_torneo
    grupos = Grupo.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo
        ).values('id_grupo')
    ).distinct()

    # Filtrar los equipos que pertenecen a esos grupos, temporada y torneo
    equipos = Equipo.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo,
            id_grupo__in=grupos
        ).values('id_equipo')
    ).distinct()

    if request.method == 'POST':
        form = CrearPartidoForm(request.POST)
        form.fields['id_equipo_1'].queryset = equipos
        form.fields['id_equipo_2'].queryset = equipos
        form.fields['id_grupo'].queryset = grupos

        if form.is_valid():
            equipo_1 = form.cleaned_data['id_equipo_1']
            equipo_2 = form.cleaned_data['id_equipo_2']

            # Verificar que los equipos no sean el mismo
            if equipo_1 == equipo_2:
                form.add_error('id_equipo_2', 'El equipo 2 no puede ser el mismo que el equipo 1.')
            else:
                partido.id_equipo_1 = equipo_1
                partido.id_equipo_2 = equipo_2
                partido.id_predio = form.cleaned_data['id_predio']
                partido.id_grupo = form.cleaned_data['id_grupo']
                partido.fecha_partido = form.cleaned_data['fecha_partido']
                partido.hora_partido = form.cleaned_data['hora_partido']
                partido.destacado = form.cleaned_data['destacado']
                partido.save()
                return redirect('fechas', id_temporada=id_temporada)
    else:
        # Inicializa el formulario con los datos del partido
        form = CrearPartidoForm(initial={
            'id_equipo_1': partido.id_equipo_1,
            'id_equipo_2': partido.id_equipo_2,
            'id_predio': partido.id_predio,
            'id_grupo': partido.id_grupo,
            'fecha_partido': partido.fecha_partido.strftime('%Y-%m-%d'),  # Formato correcto
            'hora_partido': partido.hora_partido.strftime('%H:%M'),
            'destacado': partido.destacado
        })
        form.fields['id_equipo_1'].queryset = equipos
        form.fields['id_equipo_2'].queryset = equipos
        form.fields['id_grupo'].queryset = grupos

    return render(request, 'administracion/edit_partido.html', {
        'form': form,
        'temporada': temporada,
        'fecha': fecha
    })


def delete_partido(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido, id_temporada=temporada, id_fecha=fecha)

    if request.method == 'POST':
        partido.delete()
        return redirect('fechas', id_temporada=id_temporada)

    return render(request, 'administracion/delete_partido.html', {
        'temporada': temporada,
        'fecha': fecha,
        'partido': partido
    })

def crear_resultado(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido, id_temporada=temporada, id_fecha=fecha)
    
    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        
        if form.is_valid():
            resultado = Resultado(
                id_partido=partido,
                goles_equipo_1=form.cleaned_data['goles_equipo_1'],
                goles_equipo_2=form.cleaned_data['goles_equipo_2'],
                penales=form.cleaned_data['penales'],
                penales_equipo_1=form.cleaned_data['penales_equipo_1'] if form.cleaned_data['penales'] else 0,
                penales_equipo_2=form.cleaned_data['penales_equipo_2'] if form.cleaned_data['penales'] else 0
            )
            resultado.save()
            return redirect('fechas', id_temporada=id_temporada)
    else:
        form = ResultadoForm()
    
    return render(request, 'administracion/crear_resultado.html', {
        'form': form,
        'temporada': temporada,
        'fecha': fecha,
        'partido': partido
    })


def crear_planilla(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido)
    torneo = temporada.id_torneo

    # Filtrar jugadores por equipos, temporada, torneo y grupo del partido
    jugadores = Jugador.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=torneo,
            id_grupo=partido.id_grupo,
        ).values('id_jugador')
    ).distinct()

    # Crear un diccionario para los formularios de cada jugador
    jugadores_formularios = {}

    if request.method == 'POST':
        # Procesar cada formulario individualmente
        for jugador in jugadores:
            # Crear un formulario por jugador con los datos del POST
            form = PlanillaForm(request.POST, prefix=f'jugador_{jugador.id}')
            if form.is_valid():
                # Solo guardar si el jugador participó
                if form.cleaned_data['participo']:
                    try:
                        Planilla.objects.create(
                            id_partido=partido,
                            id_equipo=TemporadaXTorneoXGrupoXEquipoXJugador.objects.get(
                                id_jugador=jugador,
                                id_temporada=temporada,
                                id_torneo=torneo,
                                id_grupo=partido.id_grupo
                            ).id_equipo,
                            id_jugador=jugador,
                            goles=form.cleaned_data['goles'],
                            num_camiseta=form.cleaned_data['num_camiseta'],
                            participo=form.cleaned_data['participo'],
                            tarjeta_amarilla=form.cleaned_data['tarjeta_amarilla'],
                            tarjeta_roja=form.cleaned_data['tarjeta_roja'],
                            figura=form.cleaned_data['figura']
                        )
                    except Exception as e:
                        print(f"Error al guardar la planilla para el jugador {jugador.nombre_jugador}: {e}")
            jugadores_formularios[jugador] = form  # Guardar el formulario con el objeto jugador completo

        # Si todos los formularios son válidos, redirigir a la vista de fechas
        return redirect('fechas', id_temporada=id_temporada)

    else:
        # Crear los formularios vacíos cuando el request es GET
        for jugador in jugadores:
            form = PlanillaForm(prefix=f'jugador_{jugador.id}')
            jugadores_formularios[jugador] = form  # Guardar el formulario con el objeto jugador completo

    return render(request, 'administracion/crear_planilla.html', {
        'temporada': temporada,
        'fecha': fecha,
        'partido': partido,
        'jugadores_formularios': jugadores_formularios,
    })



def gestionar_partido(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido)

    # Verificar si ya existe un resultado para el partido
    resultado = Resultado.objects.filter(id_partido=partido).first()

    # Acceso a los equipos
    equipo_1 = partido.id_equipo_1
    equipo_2 = partido.id_equipo_2

    # Filtrar jugadores por equipos, temporada, torneo y grupo del partido
    jugadores_equipo_1 = Jugador.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=partido.id_torneo,
            id_grupo=partido.id_grupo,
            id_equipo=equipo_1
        ).values('id_jugador')
    ).order_by('nombre_jugador')

    jugadores_equipo_2 = Jugador.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=partido.id_torneo,
            id_grupo=partido.id_grupo,
            id_equipo=equipo_2
        ).values('id_jugador')
    ).order_by('nombre_jugador')

    # Formularios existentes de planillas
    planillas_existentes = Planilla.objects.filter(id_partido=partido)

    # Crear formularios para cada jugador del equipo 1
    jugadores_formularios_equipo_1 = []
    for jugador in jugadores_equipo_1:
        planilla_jugador = planillas_existentes.filter(id_jugador=jugador).first()
        initial_data = {
            'goles': planilla_jugador.goles if planilla_jugador else 0,
            'num_camiseta': planilla_jugador.num_camiseta if planilla_jugador else '',
            'participo': planilla_jugador.participo if planilla_jugador else False,
            'tarjeta_amarilla': planilla_jugador.tarjeta_amarilla if planilla_jugador else False,
            'tarjeta_roja': planilla_jugador.tarjeta_roja if planilla_jugador else False,
            'figura': planilla_jugador.figura if planilla_jugador else False,
        }
        form = PlanillaForm(request.POST or None, initial=initial_data, prefix=f'jugador_{jugador.id}')
        jugadores_formularios_equipo_1.append((jugador, form))  # Emparejamos jugador con formulario

    # Crear formularios para cada jugador del equipo 2
    jugadores_formularios_equipo_2 = []
    for jugador in jugadores_equipo_2:
        planilla_jugador = planillas_existentes.filter(id_jugador=jugador).first()
        initial_data = {
            'goles': planilla_jugador.goles if planilla_jugador else 0,
            'num_camiseta': planilla_jugador.num_camiseta if planilla_jugador else '',
            'participo': planilla_jugador.participo if planilla_jugador else False,
            'tarjeta_amarilla': planilla_jugador.tarjeta_amarilla if planilla_jugador else False,
            'tarjeta_roja': planilla_jugador.tarjeta_roja if planilla_jugador else False,
            'figura': planilla_jugador.figura if planilla_jugador else False,
        }
        form = PlanillaForm(request.POST or None, initial=initial_data, prefix=f'jugador_{jugador.id}')
        jugadores_formularios_equipo_2.append((jugador, form))  # Emparejamos jugador con formulario

    # Crear formulario para resultado si existe, de lo contrario, sin datos iniciales
    initial_resultado = {
        'goles_equipo_1': resultado.goles_equipo_1 if resultado else None,
        'goles_equipo_2': resultado.goles_equipo_2 if resultado else None,
    }
    resultado_form = ResultadoForm(request.POST or None, initial=initial_resultado)

    if request.method == 'POST':
        # Procesar el formulario de resultado
        if resultado_form.is_valid():
            resultado_data = resultado_form.cleaned_data
            if not resultado:
                resultado = Resultado(id_partido=partido)
            resultado.goles_equipo_1 = resultado_data.get('goles_equipo_1', 0)
            resultado.goles_equipo_2 = resultado_data.get('goles_equipo_2', 0)
            resultado.save()

        # Procesar las planillas
        for jugador, form in jugadores_formularios_equipo_1 + jugadores_formularios_equipo_2:
            if form.is_valid():
                participo = form.cleaned_data.get('participo', False)
                if participo:
                    planilla, _ = Planilla.objects.update_or_create(
                        id_partido=partido,
                        id_jugador=jugador,
                        defaults={
                            'id_equipo': equipo_1 if jugador in jugadores_equipo_1 else equipo_2,
                            'goles': form.cleaned_data.get('goles', 0),
                            'num_camiseta': form.cleaned_data.get('num_camiseta', ''),
                            'participo': participo,
                            'tarjeta_amarilla': form.cleaned_data.get('tarjeta_amarilla', False),
                            'tarjeta_roja': form.cleaned_data.get('tarjeta_roja', False),
                            'figura': form.cleaned_data.get('figura', False),
                        }
                    )

        # Redirigir a la vista de fechas
        return redirect('fechas', id_temporada=temporada.id)

    return render(request, 'administracion/gestionar_partido.html', {
        'temporada': temporada,
        'fecha': fecha,
        'partido': partido,
        'equipo_1': equipo_1,
        'equipo_2': equipo_2,
        'resultado_form': resultado_form,
        'jugadores_formularios_equipo_1': jugadores_formularios_equipo_1,
        'jugadores_formularios_equipo_2': jugadores_formularios_equipo_2,
    })







def generar_planilla_pdf(request, id_temporada, id_fecha, id_partido):
    # Obtener temporada, fecha y partido
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido)

    # Obtener equipos del partido
    equipo_1 = partido.id_equipo_1
    equipo_2 = partido.id_equipo_2

    # Obtener jugadores de ambos equipos
    jugadores_equipo_1 = Jugador.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=partido.id_torneo,
            id_grupo=partido.id_grupo,
            id_equipo=equipo_1
        ).values('id_jugador')
    ).order_by('apellido_jugador', 'nombre_jugador')

    jugadores_equipo_2 = Jugador.objects.filter(
        id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=partido.id_torneo,
            id_grupo=partido.id_grupo,
            id_equipo=equipo_2
        ).values('id_jugador')
    ).order_by('apellido_jugador', 'nombre_jugador')

    # Datos para el contexto
    context = {
        'equipo_1': equipo_1.nombre_equipo,
        'equipo_2': equipo_2.nombre_equipo,
        'jugadores_equipo_1': jugadores_equipo_1,
        'jugadores_equipo_2': jugadores_equipo_2,
    }

    # Cargar la plantilla HTML
    template = get_template('administracion/planillapdf.html')
    html = template.render(context)

    # Configurar la respuesta HTTP como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="planilla_partido_{id_partido}.pdf"'

    # Crear el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)
    return response
 




def generar_planillas_pdf(request, id_temporada, id_fecha):
    # Obtener temporada y fecha
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    # Obtener todos los partidos para esa fecha
    partidos = Partido.objects.filter(id_fecha=fecha)

    # Verificar que los partidos de la fecha se están obteniendo correctamente
    print(f"Partidos encontrados: {partidos.count()}")  # Esto debería devolver el número correcto de partidos

    # Crear un buffer en memoria para el ZIP
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        # Generar los PDFs para cada partido y agregar al ZIP
        for partido in partidos:
            equipo_1 = partido.id_equipo_1
            equipo_2 = partido.id_equipo_2

            jugadores_equipo_1 = Jugador.objects.filter(
                id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                    id_temporada=temporada,
                    id_torneo=partido.id_torneo,
                    id_grupo=partido.id_grupo,
                    id_equipo=equipo_1
                ).values('id_jugador')
            ).order_by('apellido_jugador', 'nombre_jugador')

            jugadores_equipo_2 = Jugador.objects.filter(
                id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                    id_temporada=temporada,
                    id_torneo=partido.id_torneo,
                    id_grupo=partido.id_grupo,
                    id_equipo=equipo_2
                ).values('id_jugador')
            ).order_by('apellido_jugador', 'nombre_jugador')

            # Datos para el contexto de la plantilla
            context = {
                'equipo_1': equipo_1.nombre_equipo,
                'equipo_2': equipo_2.nombre_equipo,
                'jugadores_equipo_1': jugadores_equipo_1,
                'jugadores_equipo_2': jugadores_equipo_2,
                'fecha': fecha,
            }

            # Cargar la plantilla HTML para el PDF
            template = get_template('administracion/planillapdf.html')
            html = template.render(context)

            # Crear el PDF en un buffer en memoria
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
            if pisa_status.err:
                return HttpResponse('Hubo un error al generar el PDF', status=500)

            # Guardar el PDF en el archivo ZIP
            zip_file.writestr(f'planilla_partido_{partido.id}.pdf', pdf_buffer.getvalue())

    # Volver al inicio del buffer del ZIP para leerlo
    zip_buffer.seek(0)

    # Configurar la respuesta HTTP como un archivo ZIP
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="planillas_partidos.zip"'
    return response


def reglamentos_lista(request):
    reglamentos = Reglamento.objects.all()
    return render(request, 'administracion/reglamentos_lista.html', {'reglamentos': reglamentos})

def reglamentos_crear(request):
    if request.method == 'GET':
        return render(request, 'administracion/reglamentos_crear.html', {
            'form': CrearReglamentoForm()
        })
    else: 
        form = CrearReglamentoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre_reglamento = form.cleaned_data['nombre_reglamento']
            if Reglamento.objects.filter(nombre_reglamento=nombre_reglamento).exists():
                return render(request, 'administracion/reglamentos_crear.html', {
                    'form': form,
                    'error': 'Ya existe un reglamento con este nombre'
                })
                
            reglamento = Reglamento(
                nombre_reglamento = nombre_reglamento,
                archivo_reglamento = form.cleaned_data['archivo_reglamento']
            )
            reglamento.save()
            
            return redirect('reglamentos_lista')
        else:
            return render(request, 'administracion/reglamentos_crear.html', {
                'form': form,
                'error': 'Datos no validos, vuelve a intentar'
            })
            
            
def reglamentos_editar(request, id_reglamento):
    reglamento = get_object_or_404(Reglamento, pk=id_reglamento)
    
    if request.method == 'GET':
        form = CrearReglamentoForm(initial={
            'nombre_reglamento': reglamento.nombre_reglamento,
            'archivo_reglamento': reglamento.archivo_reglamento
        })
        return render(request, 'administracion/reglamentos_editar.html', {'form': form, 'reglamento': reglamento})
    
    else:
        form = CrearReglamentoForm(request.POST, request.FILES)
        
        if form.is_valid():
            nombre_reglamento = form.cleaned_data['nombre_reglamento']
            if Reglamento.objects.filter(nombre_reglamento=nombre_reglamento).exclude(pk=id_reglamento).exists():
                return render(request, 'administracion/reglamentos_editar.html', {
                    'form': form,
                    'reglamento': reglamento,
                    'error': 'Ya existe un reglamento con este nombre.'
                })
            
            reglamento.nombre_reglamento = nombre_reglamento
            if 'archivo_reglamento' in request.FILES:
                reglamento.archivo_reglamento = form.cleaned_data['archivo_reglamento']
            elif form.cleaned_data['archivo_reglamento'] is None:
                pass
            else:
                reglamento.archivo_reglamento.delete(save=False)
                reglamento.archivo_reglamento = None
            
            reglamento.save()
            return redirect('reglamentos_lista') 
        else:
            return render(request, 'administracion/reglamentos_editar.html', {
                'form': form,
                'reglamento': reglamento,
                'error': 'Por favor introduce datos válidos.'
            })

            

def reglamentos_eliminar(request, id_reglamento):
    reglamento = get_object_or_404(Reglamento, pk=id_reglamento)
    if request.method == 'POST':
        reglamento.delete()
        return redirect('reglamentos_lista')



def resumen_adm(request):
    return render(request, 'administracion/resumen_adm.html')


def traspasos(request):
    traspasos = Traspaso.objects.all()
    return render(request, 'administracion/traspasos.html', {'traspasos': traspasos})


def traspasos_crear(request):
    if request.method == 'GET':
        return render(request, 'administracion/traspasos_crear.html', {
            'form': CrearTraspasoForm()
        })
    else:
        form = CrearTraspasoForm(request.POST)
        if form.is_valid():
            equipo_actual = form.cleaned_data.get('id_equipo_actual')
            equipo_nuevo = form.cleaned_data.get('id_equipo_nuevo')
            
            if equipo_actual == equipo_nuevo:
                messages.error(request, 'No puedes crear un traspaso con el mismo equipo')
                return render(request, 'administracion/traspasos_crear.html', {
                    'form': form
                })
                
                
            traspaso = Traspaso(
                id_jugador=form.cleaned_data.get('id_jugador'),
                id_equipo_actual=equipo_actual,
                id_equipo_nuevo=equipo_nuevo,
                fecha_transferencia=form.cleaned_data['fecha_transferencia']
            )
            traspaso.save()
            
            return redirect('traspasos')
        
        else:
            return render(request, 'administracion/traspasos_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos validos'
            })
            
def traspasos_editar(request, id_traspaso):
    traspaso = get_object_or_404(Traspaso, pk=id_traspaso)
    if request.method == 'GET':
        form = CrearTraspasoForm(initial={
            'id_jugador': traspaso.id_jugador,
            'id_equipo_actual': traspaso.id_equipo_actual,
            'id_equipo_nuevo': traspaso.id_equipo_nuevo,
            'fecha_transferencia': traspaso.fecha_transferencia.strftime('%Y-%m-%d')
        })
        return render(request, 'administracion/traspasos_editar.html', {'form': form, 'traspaso': traspaso})
    else: 
        form = CrearTraspasoForm(request.POST)
        if form.is_valid():
            equipo_actual = form.cleaned_data.get('id_equipo_actual')
            equipo_nuevo = form.cleaned_data.get('id_equipo_nuevo')
            
            if equipo_actual == equipo_nuevo:
                messages.error(request, 'No se permite un traspaso de mismos equipos')
                return render(request, 'administracion/traspasos_editar.html', {
                    'form': form,
                    'traspaso': traspaso
                })
                
            traspaso.id_jugador = form.cleaned_data.get('id_jugador')
            traspaso.id_equipo_actual = form.cleaned_data.get('id_equipo_actual')
            traspaso.id_equipo_nuevo = form.cleaned_data.get('id_equipo_nuevo')
            traspaso.fecha_transferencia = form.cleaned_data.get('fecha_transferencia')
            
            traspaso.save()
            return redirect('traspasos')
        
        else:
            return render(request, 'administracion/traspasos_editar.html', {
                'form': form,
                'traspaso': traspaso
            })
            
            
def traspasos_eliminar(request, id_traspaso):
    traspaso = get_object_or_404(Traspaso, pk=id_traspaso)
    if request.method == 'POST':
        traspaso.delete()
        return redirect('traspasos')


def mostrar_torneos(request):
    # Obtener todos los torneos
    torneos = Torneo.objects.all()

    # Crear una lista para almacenar los datos formateados de los torneos
    torneos_datos = []

    for torneo in torneos:
        # Obtener la categoría y el tipo de torneo
        categoria = torneo.id_categoria.nombre_categoria if torneo.id_categoria else 'Sin categoría'
        tipo_torneo = torneo.id_tipo_torneo.nombre_tipo_torneo if torneo.id_tipo_torneo else 'Sin tipo'
        
        # Contar el número de ediciones
        ediciones = Temporada.objects.filter(id_torneo=torneo).count()

        # Contar el número de equipos únicos participantes en cualquier temporada del torneo
        equipos = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada__id_torneo=torneo
        ).values_list('id_equipo', flat=True).distinct().count()

        # Contar el número de partidos
        partidos = Partido.objects.filter(
            id_temporada__id_torneo=torneo
        ).count()  # Ajusta el filtro según tu modelo de Partidos

        # Añadir los datos del torneo a la lista
        torneos_datos.append({
            'id_torneo': torneo.id,
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


def lista_temporadas(request, id_torneo):
    # Obtén el objeto del torneo basado en el id
    torneo = get_object_or_404(Torneo, id=id_torneo)
    
    # Obtén las temporadas relacionadas con el torneo utilizando el campo id_torneo
    temporadas = Temporada.objects.filter(id_torneo=torneo).order_by('-fecha_inicio')
    
    # Renderiza la plantilla con los datos del torneo y las temporadas ordenadas
    return render(request, 'lista_temporadas.html', {'torneo': torneo, 'temporadas': temporadas})



def temporada_detalles(request, id_temporada, id_torneo):
    # Obtener la temporada actual
    temporada = get_object_or_404(Temporada, id=id_temporada, id_torneo=id_torneo)
    torneo = temporada.id_torneo
    
    # Obtener la temporada anterior y siguiente en relación a la temporada actual
    temporadas = Temporada.objects.filter(id_torneo=torneo).order_by('fecha_inicio')
    temporada_anterior = temporadas.filter(fecha_inicio__lt=temporada.fecha_inicio).last()
    temporada_siguiente = temporadas.filter(fecha_inicio__gt=temporada.fecha_inicio).first()
    
    # Obtener los grupos de la temporada
    grupos = Grupo.objects.filter(id_temporada=temporada)

    # Para cada grupo, obtener su tabla de posiciones
    grupos_y_tablas = []
    for grupo in grupos:
        tabla_posiciones = TablaDePosicion.objects.filter(
            id_temporada=temporada,
            id_grupo=grupo
        ).order_by('-puntos', '-diferencia_goles')
        
        # Actualizar los partidos jugados de cada equipo en la tabla de posiciones
        for tabla in tabla_posiciones:
            equipo = tabla.id_equipo
            
            # Calcular partidos jugados
            partidos_jugados = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo
            ).exclude(resultado__isnull=True).count() + Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo
            ).exclude(resultado__isnull=True).count()
            
            # Calcular partidos ganados
            partidos_ganados = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo,
                resultado__goles_equipo_1__gt=F('resultado__goles_equipo_2')
            ).exclude(resultado__isnull=True).count() + Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo,
                resultado__goles_equipo_2__gt=F('resultado__goles_equipo_1')
            ).exclude(resultado__isnull=True).count()
            
            # Calcular partidos empatados
            partidos_empatados = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo,
                resultado__goles_equipo_1=F('resultado__goles_equipo_2')
            ).exclude(resultado__isnull=True).count() + Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo,
                resultado__goles_equipo_2=F('resultado__goles_equipo_1')
            ).exclude(resultado__isnull=True).count()

            # Calcular partidos perdidos
            partidos_perdidos = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo,
                resultado__goles_equipo_1__lt=F('resultado__goles_equipo_2')
            ).exclude(resultado__isnull=True).count() + Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo,
                resultado__goles_equipo_2__lt=F('resultado__goles_equipo_1')
            ).exclude(resultado__isnull=True).count()
            
            # Calcular goles a favor (goles anotados por el equipo)
            goles_a_favor = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo
            ).exclude(resultado__isnull=True).aggregate(Sum('resultado__goles_equipo_1'))['resultado__goles_equipo_1__sum'] or 0

            goles_a_favor += Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo
            ).exclude(resultado__isnull=True).aggregate(Sum('resultado__goles_equipo_2'))['resultado__goles_equipo_2__sum'] or 0

            # Calcular goles en contra (goles recibidos por el equipo)
            goles_en_contra = Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_1=equipo
            ).exclude(resultado__isnull=True).aggregate(Sum('resultado__goles_equipo_2'))['resultado__goles_equipo_2__sum'] or 0

            goles_en_contra += Partido.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo_2=equipo
            ).exclude(resultado__isnull=True).aggregate(Sum('resultado__goles_equipo_1'))['resultado__goles_equipo_1__sum'] or 0

            # Calcular diferencia de goles
            diferencia_goles = goles_a_favor - goles_en_contra
            
            # Calcular tarjetas amarillas
            tarjetas_amarillas = Planilla.objects.filter(
                id_partido__id_temporada=temporada,
                id_partido__id_grupo=grupo,
                id_equipo=equipo,
                tarjeta_amarilla=True
            ).count()

            # Calcular tarjetas rojas
            tarjetas_rojas = Planilla.objects.filter(
                id_partido__id_temporada=temporada,
                id_partido__id_grupo=grupo,
                id_equipo=equipo,
                tarjeta_roja=True
            ).count()
            
            puntos = (partidos_ganados * 3) + (partidos_empatados * 1)
            
            # Actualizamos la tabla de posiciones con el número de partidos jugados
            tabla.partidos_jugados = partidos_jugados
            tabla.partidos_ganados = partidos_ganados
            tabla.partidos_empatados = partidos_empatados
            tabla.partidos_perdidos = partidos_perdidos
            tabla.goles_a_favor = goles_a_favor
            tabla.goles_en_contra = goles_en_contra
            tabla.diferencia_goles = diferencia_goles
            tabla.tarjetas_amarillas = tarjetas_amarillas
            tabla.tarjetas_rojas = tarjetas_rojas
            tabla.puntos = puntos
            tabla.save()
            

        # Agregar el grupo y su tabla de posiciones a la lista
        grupos_y_tablas.append({
            'grupo': grupo,
            'tabla_posiciones': tabla_posiciones
        })

    # Obtener las fechas y los partidos de la temporada
    fechas_partidos = Fecha.objects.filter(id_temporada=temporada).order_by('-id')  # Fechas en orden descendente
    fechas_y_partidos = []
    fecha_mas_proxima = None
    diferencia_mas_cercana = timedelta.max
    now = datetime.now().date()
    partidos = []  # Inicializamos partidos como una lista vacía

    for fecha in fechas_partidos:
        partidos = Partido.objects.filter(id_fecha=fecha).select_related('id_equipo_1', 'id_equipo_2').order_by('hora_partido')

        partidos_con_resultados = []
        for partido in partidos:
            resultado = Resultado.objects.filter(id_partido=partido).first()
            partidos_con_resultados.append({
                'id': partido.id,
                'fecha': partido.fecha_partido,
                'hora': partido.hora_partido,
                'equipo_1': partido.id_equipo_1,
                'equipo_2': partido.id_equipo_2,
                'resultado': f"{resultado.goles_equipo_1} - {resultado.goles_equipo_2}" if resultado else "VS"
            })

            # Determinar la fecha más próxima
            diferencia = abs(partido.fecha_partido - now)
            if diferencia < diferencia_mas_cercana:
                diferencia_mas_cercana = diferencia
                fecha_mas_proxima = fecha

        fechas_y_partidos.append((fecha, partidos_con_resultados))
    
    # Obtener el partido destacado que no tiene resultado
    partido_destacado = Partido.objects.filter(
        id_temporada=temporada,
        destacado=True,
        resultado__isnull=True  # Asegura que el resultado sea nulo
    ).first()
    
    # Obtener los jugadores con goles en la temporada actual (Top 5)
    ranking_jugadores = (
        Planilla.objects.filter(id_partido__id_temporada=temporada)  # Filtrar por temporada
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_goles=Sum('goles'))  # Calcular el total de goles
        .filter(total_goles__gt=0)  # Filtrar jugadores con más de 0 goles
        .order_by('-total_goles')[:5]  # Ordenar por goles (de mayor a menor) y limitar al top 5
    )

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores = Jugador.objects.filter(id__in=[item['id_jugador'] for item in ranking_jugadores])

    # Crear el ranking con los datos completos de jugadores y sus goles
    ranking_goleadores = [
        {
            'jugador': jugador,
            'total_goles': next(item['total_goles'] for item in ranking_jugadores if item['id_jugador'] == jugador.id)
        }
        for jugador in jugadores
    ]
    
    
    # Obtener los jugadores marcados como figura en la temporada actual
    planillas_con_figuras = (
        Planilla.objects.filter(
            id_partido__id_temporada=temporada,  # Filtrar por la temporada actual
            figura=True  # Filtrar únicamente los jugadores marcados como figura
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_figuras=Count('figura'))  # Contar las veces que fueron figura
        .order_by('-total_figuras')[:5]  # Ordenar por cantidad de figuras y limitar a los 5 primeros
    )
    
    # Crear un diccionario con las figuras por jugador
    figuras_por_jugador = {item['id_jugador']: item['total_figuras'] for item in planillas_con_figuras}
    
    # Obtener los objetos completos de los jugadores en el ranking
    jugadores = Jugador.objects.filter(id__in=figuras_por_jugador.keys())
    
    # Preparar el ranking con los datos completos de jugadores y sus figuras
    ranking_figuras = [
        {
            'jugador': jugador,
            'total_figuras': figuras_por_jugador[jugador.id]
        }
        for jugador in jugadores
    ]
    
    # Obtener los jugadores con tarjetas amarillas en la temporada actual (Top 5)
    planillas_con_amarillas = (
        Planilla.objects.filter(
            id_partido__id_temporada=temporada,  # Filtrar por la temporada actual
            tarjeta_amarilla=True  # Filtrar únicamente los jugadores con tarjeta amarilla
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_amarillas=Count('tarjeta_amarilla'))  # Contar las veces que recibieron tarjeta amarilla
        .order_by('-total_amarillas')[:5]  # Ordenar por cantidad de tarjetas amarillas y limitar a los 5 primeros
    )

    # Crear un diccionario con las tarjetas amarillas por jugador
    tarjetas_amarillas_por_jugador = {item['id_jugador']: item['total_amarillas'] for item in planillas_con_amarillas}

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_amarillas = Jugador.objects.filter(id__in=tarjetas_amarillas_por_jugador.keys())

    # Preparar el ranking con los datos completos de jugadores y sus tarjetas amarillas
    ranking_amarillas = [
        {
            'jugador': jugador,
            'total_amarillas': tarjetas_amarillas_por_jugador[jugador.id]
        }
        for jugador in jugadores_amarillas
    ]

    
    # Obtener los jugadores con tarjetas rojas en la temporada actual (Top 5)
    planillas_con_rojas = (
        Planilla.objects.filter(
            id_partido__id_temporada=temporada,  # Filtrar por la temporada actual
            tarjeta_roja=True  # Filtrar únicamente los jugadores con tarjeta roja
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_rojas=Count('tarjeta_roja'))  # Contar las veces que recibieron tarjeta roja
        .order_by('-total_rojas')[:5]  # Ordenar por cantidad de tarjetas rojas y limitar a los 5 primeros
    )

    # Crear un diccionario con las tarjetas rojas por jugador
    tarjetas_rojas_por_jugador = {item['id_jugador']: item['total_rojas'] for item in planillas_con_rojas}

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_rojas = Jugador.objects.filter(id__in=tarjetas_rojas_por_jugador.keys())

    # Preparar el ranking con los datos completos de jugadores y sus tarjetas rojas
    ranking_rojas = [
        {
            'jugador': jugador,
            'total_rojas': tarjetas_rojas_por_jugador[jugador.id]
        }
        for jugador in jugadores_rojas
    ]
    
    # Obtener los goles recibidos por cada equipo cuando juegan como locales
    goles_recibidos_local = (
        Partido.objects.filter(id_temporada=temporada)  # Filtrar por temporada
        .values('id_equipo_1')  # Equipos que juegan como locales
        .annotate(total_goles_recibidos=Sum('resultado__goles_equipo_2'))  # Goles recibidos por el equipo local (de equipo 2)
    )
    
    # Obtener los goles recibidos por cada equipo cuando juegan como visitantes
    goles_recibidos_visitante = (
        Partido.objects.filter(id_temporada=temporada)  # Filtrar por temporada
        .values('id_equipo_2')  # Equipos que juegan como visitantes
        .annotate(total_goles_recibidos=Sum('resultado__goles_equipo_1'))  # Goles recibidos por el equipo visitante (de equipo 1)
    )
    
    # Combinar los resultados en un diccionario
    goles_recibidos = defaultdict(int)
    
    # Sumar goles recibidos como local
    for item in goles_recibidos_local:
        goles_recibidos[item['id_equipo_1']] += item['total_goles_recibidos'] or 0  # Usar or 0 para manejar None
    
    # Sumar goles recibidos como visitante
    for item in goles_recibidos_visitante:
        goles_recibidos[item['id_equipo_2']] += item['total_goles_recibidos'] or 0  # Usar or 0 para manejar None
    
    # Convertir el diccionario a una lista de tuplas y ordenar por goles recibidos (menor a mayor)
    ranking_equipos_menos_goles = sorted(goles_recibidos.items(), key=lambda x: x[1])
    
    # Obtener los equipos completos, incluyendo el logo
    equipos = Equipo.objects.filter(id__in=[equipo[0] for equipo in ranking_equipos_menos_goles])
    equipos_dict = {equipo.id: equipo for equipo in equipos}  # Cambiar a almacenar el objeto completo
    
    # Preparar los datos para la plantilla
    ranking_equipos_menos_goles = [(equipos_dict[equipo_id], goles) for equipo_id, goles in ranking_equipos_menos_goles]
    
    # Filtrar por la temporada específica y contar los equipos únicos
    equipos_en_temporada = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(id_temporada=temporada) \
        .values('id_equipo') \
        .distinct() \
        .count()

    total_partidos_jugados = Partido.objects.filter(
        id_temporada=temporada
    ).filter(
        resultado__isnull=False  # Verifica si hay un resultado asociado (no nulo)
    ).count()

    # Si no hay partidos jugados, ponerlo en 0
    total_partidos_jugados = total_partidos_jugados if total_partidos_jugados else 0
    
    # Calcular el total de partidos ganados en la temporada
    total_partidos_ganados = Partido.objects.filter(
        id_temporada=temporada
    ).annotate(
        equipo_1_ganador=Case(
            When(resultado__goles_equipo_1__gt=F('resultado__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        ),
        equipo_2_ganador=Case(
            When(resultado__goles_equipo_2__gt=F('resultado__goles_equipo_1'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_ganados=Sum('equipo_1_ganador') + Sum('equipo_2_ganador')
    )['total_ganados']

    # Si no hay partidos ganados, ponerlo en 0
    total_partidos_ganados = total_partidos_ganados if total_partidos_ganados else 0
    
    # Calcular el total de partidos empatados en la temporada
    total_partidos_empatados = Partido.objects.filter(
        id_temporada=temporada
    ).annotate(
        empate=Case(
            When(resultado__goles_equipo_1=F('resultado__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_empatados=Sum('empate')
    )['total_empatados']

    # Si no hay partidos empatados, ponerlo en 0
    total_partidos_empatados = total_partidos_empatados if total_partidos_empatados else 0
    
    # Calcular el total de partidos perdidos por ambos equipos en la temporada
    total_partidos_perdidos = Partido.objects.filter(
        id_temporada=temporada
    ).annotate(
        equipo_1_perdido=Case(
            When(resultado__goles_equipo_1__lt=F('resultado__goles_equipo_2'), then=1),
            default=0,
            output_field=IntegerField()
        ),
        equipo_2_perdido=Case(
            When(resultado__goles_equipo_2__lt=F('resultado__goles_equipo_1'), then=1),
            default=0,
            output_field=IntegerField()
        )
    ).aggregate(
        total_perdidos=Sum('equipo_1_perdido') + Sum('equipo_2_perdido')
    )['total_perdidos']

    # Si no hay partidos perdidos, ponerlo en 0
    total_partidos_perdidos = total_partidos_perdidos if total_partidos_perdidos else 0
    
    # Calcular el total de goles en la temporada
    total_goles = Resultado.objects.filter(
        id_partido__id_temporada=temporada
    ).aggregate(
        total_goles=Sum('goles_equipo_1') + Sum('goles_equipo_2')
    )['total_goles']

    # Manejo de valores nulos
    total_goles = total_goles if total_goles else 0
    
    # Calcular el total de tarjetas amarillas en la temporada
    total_tarjetas_amarillas = Planilla.objects.filter(
        id_partido__id_temporada=temporada,  # Filtrar por la temporada actual
        tarjeta_amarilla=True  # Solo contar las planillas con tarjetas amarillas
    ).count()

    # Manejo de valores nulos o sin resultados
    total_tarjetas_amarillas = total_tarjetas_amarillas if total_tarjetas_amarillas else 0
    
    # Calcular el total de tarjetas rojas en la temporada
    total_tarjetas_rojas = Planilla.objects.filter(
        id_partido__id_temporada=temporada,  # Filtrar por la temporada actual
        tarjeta_roja=True  # Solo contar las planillas con tarjetas rojas
    ).count()

    # Manejo de valores nulos o sin resultados
    total_tarjetas_rojas = total_tarjetas_rojas if total_tarjetas_rojas else 0
    
    # Renderizar la plantilla con los datos necesarios
    return render(request, 'temporada_detalles.html', {
        'temporada': temporada,
        'torneo': torneo,
        'temporada_anterior': temporada_anterior,
        'temporada_siguiente': temporada_siguiente,
        'grupos_y_tablas': grupos_y_tablas,
        'fechas_y_partidos': fechas_y_partidos,
        'fecha_a_mostrar': fecha_mas_proxima,
        'partido_destacado': partido_destacado,
        'ranking_jugadores': ranking_goleadores,
        'ranking_figuras': ranking_figuras, 
        'ranking_amarillas': ranking_amarillas,
        'ranking_rojas': ranking_rojas,
        'ranking_equipos_menos_goles': ranking_equipos_menos_goles,
        'equipos_en_temporada': equipos_en_temporada,
        'total_partidos_jugados': total_partidos_jugados,
        'total_partidos_ganados': total_partidos_ganados,
        'total_partidos_empatados': total_partidos_empatados,
        'total_partidos_perdidos': total_partidos_perdidos,
        'total_goles': total_goles,
        'total_tarjetas_amarillas': total_tarjetas_amarillas,
        'total_tarjetas_rojas': total_tarjetas_rojas,
        'partidos': partidos,
        'id_torneo': id_torneo,
        'id_temporada': id_temporada,

    })


def equipo_perfil(request, equipo_id, temporada_id):
    # Traemos el equipo usando el id proporcionado
    equipo = get_object_or_404(Equipo, id=equipo_id)
    
    # Traemos la temporada usando el id proporcionado
    temporada = get_object_or_404(Temporada, id=temporada_id)
    
    # Obtener el entrenador del equipo, si tiene uno asignado
    entrenador = Entrenador.objects.filter(id_equipo=equipo).first()  # Usamos .first() para obtener el primer entrenador si existe
    
    # Obtenemos los jugadores que pertenecen a este equipo en esta temporada y excluimos id_jugador=NULL
    jugadores_relacionados = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_equipo=equipo,
        id_temporada=temporada
    ).exclude(
        id_jugador__isnull=True  # Excluir los registros donde id_jugador es NULL
    ).select_related('id_jugador')  # Traemos los jugadores completos asociados a la relación
    
    # Obtenemos solo los jugadores válidos (no NULL)
    jugadores = [jugador.id_jugador for jugador in jugadores_relacionados]
    
    # Calculamos el total de jugadores
    total_jugadores = len(jugadores)
    
    # Cálculo de edad promedio
    if total_jugadores > 0:
        total_edad = sum(jugador.calcular_edad() for jugador in jugadores)
        edad_promedio = round(total_edad / total_jugadores, 2)
    else:
        edad_promedio = 0.0
        
    # Calcular el total de torneos en los que participó este equipo
    total_torneos = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_equipo=equipo
    ).values('id_torneo').distinct().count()
    
    # Obtener las bajas (jugadores que han dejado el equipo y se han ido a otro equipo)
    bajas = Traspaso.objects.filter(
        id_equipo_actual=equipo  # Filtrar por el equipo que tiene al jugador actualmente
    ).order_by('-fecha_transferencia')[:10]  # Limitar a los 10 traspasos más recientes

    # Obtener las altas (jugadores que se han unido al equipo)
    altas = Traspaso.objects.filter(
        id_equipo_nuevo=equipo  # Filtrar por el equipo al que ha llegado el jugador
    ).order_by('-fecha_transferencia')[:10]  # Limitar a los 10 traspasos más recientes
    
    # Obtenemos el siguiente partido del equipo en la temporada
    siguiente_partido = Partido.objects.filter(
        id_temporada=temporada,
        fecha_partido__gte=now().date()  # Filtrar partidos a partir de hoy
    ).filter(
        id_equipo_1=equipo  # Equipo como local
    ) | Partido.objects.filter(
        id_temporada=temporada,
        fecha_partido__gte=now().date(),  # Filtrar partidos a partir de hoy
        id_equipo_2=equipo  # Equipo como visitante
    )
    
    # Ordenamos por fecha y tomamos el primero (el próximo partido)
    siguiente_partido = siguiente_partido.order_by('fecha_partido', 'hora_partido').first()
    
    
    # Buscar partidos donde el equipo haya participado en esta temporada
    partidos_equipo = Partido.objects.filter(
        id_temporada=temporada,
        id_equipo_1__isnull=False,
        id_equipo_2__isnull=False
    ).filter(
        Q(id_equipo_1=equipo) | Q(id_equipo_2=equipo)
    )

    # Construir el historial incluyendo los resultados y logos
    historial_partidos = []
    for partido in partidos_equipo:
        try:
            # Acceder al resultado relacionado
            resultado = Resultado.objects.get(id_partido=partido)
            historial_partidos.append({
                'equipo_1': partido.id_equipo_1.nombre_equipo,
                'equipo_2': partido.id_equipo_2.nombre_equipo,
                'equipo_1_logo': partido.id_equipo_1.logo_equipo,
                'equipo_2_logo': partido.id_equipo_2.logo_equipo,
                'goles_equipo_1': resultado.goles_equipo_1,
                'goles_equipo_2': resultado.goles_equipo_2,
                'penales': resultado.penales,
                'penales_equipo_1': resultado.penales_equipo_1,
                'penales_equipo_2': resultado.penales_equipo_2,
            })
        except Resultado.DoesNotExist:
            # Si no hay un resultado asociado, puedes decidir ignorarlo o manejarlo
            pass

    # Inicializar variables de estadísticas
    partidos_jugados = 0
    partidos_ganados = 0
    partidos_empatados = 0
    partidos_perdidos = 0
    goles_a_favor = 0
    goles_en_contra = 0
    tarjetas_amarillas_equipo = 0
    tarjetas_rojas_equipo = 0

    # Obtener las estadísticas del equipo desde la tabla de posiciones
    estadisticas = TablaDePosicion.objects.filter(
        id_equipo=equipo_id,
        id_temporada=temporada_id
    ).first()
    
    

    # Si no se encuentran estadísticas, se inicializan en 0 para evitar errores
    partidos_jugados = estadisticas.partidos_jugados if estadisticas else 0
    partidos_ganados = estadisticas.partidos_ganados if estadisticas else 0
    partidos_empatados = estadisticas.partidos_empatados if estadisticas else 0
    partidos_perdidos = estadisticas.partidos_perdidos if estadisticas else 0
    goles_a_favor = estadisticas.goles_a_favor if estadisticas else 0
    goles_en_contra = estadisticas.goles_en_contra if estadisticas else 0
    tarjetas_amarillas_equipo = estadisticas.tarjetas_amarillas if estadisticas else 0
    tarjetas_rojas_equipo = estadisticas.tarjetas_rojas if estadisticas else 0
    
    # Obtener el ranking de goleadores del equipo para la temporada
    ranking_jugadores = (
        Planilla.objects.filter(
            id_partido__in=partidos_equipo,  # Solo los partidos del equipo
            id_equipo=equipo  # Solo los jugadores de este equipo
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_goles=Sum('goles'))  # Calcular el total de goles
        .filter(total_goles__gt=0)  # Filtrar jugadores con goles > 0
        .order_by('-total_goles')  # Ordenar por goles de mayor a menor
    )

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_ranking_goleadores = Jugador.objects.filter(id__in=[item['id_jugador'] for item in ranking_jugadores])

    # Crear el ranking con los datos completos de jugadores y sus goles
    ranking_goleadores = [
        {
            'jugador': jugador,
            'total_goles': next(item['total_goles'] for item in ranking_jugadores if item['id_jugador'] == jugador.id)
        }
        for jugador in jugadores_ranking_goleadores
    ]

    # Obtener los jugadores marcados como figura en la temporada actual
    planillas_con_figuras = (
        Planilla.objects.filter(
            id_partido__in=partidos_equipo,  # Solo los partidos del equipo
            id_equipo=equipo,  # Solo los jugadores de este equipo
            figura=True  # Solo los jugadores marcados como figura
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_figuras=Count('figura'))  # Contar las veces que fueron figura
        .order_by('-total_figuras')[:5]  # Ordenar por cantidad de figuras y limitar a los 5 primeros
    )

    # Crear un diccionario con las figuras por jugador
    figuras_por_jugador = {item['id_jugador']: item['total_figuras'] for item in planillas_con_figuras}

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_ranking_figuras = Jugador.objects.filter(id__in=figuras_por_jugador.keys())

    # Preparar el ranking con los datos completos de jugadores y sus figuras
    ranking_figuras = [
        {
            'jugador': jugador,
            'total_figuras': figuras_por_jugador[jugador.id]
        }
        for jugador in jugadores_ranking_figuras
    ]

    # Obtener los jugadores con tarjetas amarillas en los partidos del equipo para la temporada actual
    planillas_con_tarjetas_amarillas = (
        Planilla.objects.filter(
            id_partido__in=partidos_equipo,  # Filtra los partidos del equipo
            id_equipo=equipo,  # Solo los jugadores de este equipo
            tarjeta_amarilla=True  # Solo los jugadores con tarjetas amarillas
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_tarjetas_amarillas=Count('tarjeta_amarilla'))  # Contar las veces que tuvieron tarjeta amarilla
        .order_by('-total_tarjetas_amarillas')  # Ordenar por la cantidad de tarjetas amarillas de mayor a menor
    )

    # Crear un diccionario con las tarjetas amarillas por jugador
    tarjetas_amarillas_por_jugador = {item['id_jugador']: item['total_tarjetas_amarillas'] for item in planillas_con_tarjetas_amarillas}

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_ranking_tarjetas_amarillas = Jugador.objects.filter(id__in=tarjetas_amarillas_por_jugador.keys())

    # Preparar el ranking con los datos completos de jugadores y sus tarjetas amarillas
    ranking_tarjetas_amarillas = [
        {
            'jugador': jugador,
            'total_tarjetas_amarillas': tarjetas_amarillas_por_jugador[jugador.id]  # Asociamos las tarjetas amarillas a cada jugador
        }
        for jugador in jugadores_ranking_tarjetas_amarillas
    ]

    # Obtener los jugadores con tarjetas rojas en los partidos del equipo para la temporada actual
    planillas_con_tarjetas_rojas = (
        Planilla.objects.filter(
            id_partido__in=partidos_equipo,  # Solo los partidos del equipo
            id_equipo=equipo,  # Solo los jugadores de este equipo
            tarjeta_roja=True  # Solo los jugadores marcados con tarjeta roja
        )
        .values('id_jugador')  # Obtener los IDs de los jugadores
        .annotate(total_tarjetas_rojas=Count('tarjeta_roja'))  # Contar las veces que tuvieron tarjeta roja
        .order_by('-total_tarjetas_rojas')[:5]  # Ordenar por cantidad de tarjetas rojas y limitar a los 5 primeros
    )

    # Crear un diccionario con las tarjetas rojas por jugador
    tarjetas_rojas_por_jugador = {item['id_jugador']: item['total_tarjetas_rojas'] for item in planillas_con_tarjetas_rojas}

    # Obtener los objetos completos de los jugadores en el ranking
    jugadores_ranking_tarjetas_rojas = Jugador.objects.filter(id__in=tarjetas_rojas_por_jugador.keys())

    # Preparar el ranking con los datos completos de jugadores y sus tarjetas rojas
    ranking_tarjetas_rojas = [
        {
            'jugador': jugador,
            'total_tarjetas_rojas': tarjetas_rojas_por_jugador[jugador.id]
        }
        for jugador in jugadores_ranking_tarjetas_rojas
    ]

    # Recuperamos los premios del equipo, sin usar values()
    premios_equipos = PremioEquipo.objects.filter(
        id_equipo=equipo  # Reemplazar 'equipo' con el equipo específico que se desea consultar
    ).select_related(
        'id_premio_grupal', 'id_temporada', 'id_torneo'
    ).annotate(
        total_premios=Count('id_premio_grupal')  # Cuenta cuántas veces el equipo ha recibido un premio
    ).order_by('-total_premios')

    # Contexto para pasar a la plantilla
    contexto = {
        'nombre_equipo': equipo.nombre_equipo,
        'entrenador': entrenador,
        'logo_equipo': equipo.logo_equipo,  # El logo del equipo
        'jugadores': jugadores,  # Lista de jugadores asociados al equipo en la temporada
        'temporada_id': temporada.id,  # Asegurarte de incluir la temporada_id
        'equipo_id': equipo.id,        # Asegurarte de incluir el equipo_id
        'total_jugadores': total_jugadores,  # Total de jugadores del equipo
        'edad_promedio': edad_promedio,  # Edad promedio redondeada a 1 decimal
        'total_torneos': total_torneos,  # Total de torneos en los que participó el equipo
        'partido_destacado': siguiente_partido,  # El próximo partido si existe
        'historial_partidos': historial_partidos,  # Lista con el historial
        'partidos_jugados': partidos_jugados,
        'partidos_ganados': partidos_ganados,
        'partidos_empatados': partidos_empatados,
        'partidos_perdidos': partidos_perdidos,
        'goles_a_favor': goles_a_favor,
        'goles_en_contra': goles_en_contra,
        'tarjetas_amarillas_equipo': tarjetas_amarillas_equipo,
        'tarjetas_rojas_equipo': tarjetas_rojas_equipo,
        'ranking_goleadores': ranking_goleadores,
        'ranking_figuras': ranking_figuras,
        'ranking_tarjetas_amarillas': ranking_tarjetas_amarillas,
        'ranking_tarjetas_rojas': ranking_tarjetas_rojas,
        'altas': altas,
        'bajas': bajas,
        'premios_equipos': premios_equipos,
    }

    return render(request, 'equipo_detalles.html', contexto)


def jugador_detalles(request, jugador_id, temporada_id, equipo_id):
    # Obtener el jugador, equipo y temporada
    jugador = get_object_or_404(Jugador, id=jugador_id)
    equipo = get_object_or_404(Equipo, id=equipo_id)
    temporada = get_object_or_404(Temporada, id=temporada_id)
    
    # Filtrar los partidos jugados por el jugador en la temporada y el equipo
    total_jugados = Planilla.objects.filter(
        id_jugador=jugador_id,
        id_equipo=equipo_id,
        id_partido__id_temporada=temporada_id
    ).extra(where=["participo = 1"]).count()  # Condición específica para "participo"
    
    # Obtener el total de goles marcados por el jugador en la temporada y equipo
    total_goles = Planilla.objects.filter(
        id_jugador=jugador_id,
        id_equipo=equipo_id,
        id_partido__id_temporada=temporada_id
    ).aggregate(Sum('goles'))['goles__sum'] or 0  # Si no hay goles, devolvemos 0

    # Calcular el promedio de goles
    if total_jugados > 0:
        promedio_goles = total_goles / total_jugados
    else:
        promedio_goles = 0  # Si no ha jugado ningún partido, el promedio es 0
        
    # Obtener el total de tarjetas amarillas para el jugador en la temporada
    total_tarjetas_amarillas = Planilla.objects.filter(
        id_jugador=jugador_id,
        id_equipo=equipo_id,
        id_partido__id_temporada=temporada_id,
        tarjeta_amarilla=True
    ).count()  # Contamos las entradas con tarjeta_amarilla=True
    
    # Obtener el total de tarjetas rojas para el jugador en la temporada
    total_tarjetas_rojas = Planilla.objects.filter(
        id_jugador=jugador_id,
        id_equipo=equipo_id,
        id_partido__id_temporada=temporada_id,
        tarjeta_roja=True
    ).count()  # Contamos las entradas con tarjeta_roja=True
    
    traspasos = Traspaso.objects.filter(id_jugador=jugador_id).order_by('-fecha_transferencia')
    
    # Filtrar los partidos en los que el jugador ha participado
    partidos_equipo = Partido.objects.filter(
        planilla__id_jugador=jugador,
        planilla__id_equipo=equipo,
        id_temporada=temporada,
        planilla__participo=True  # Solo aquellos partidos en los que participó
    )

    # Inicializar el historial de partidos
    historial_partidos = []

    # Para cada partido en los que el jugador participó, obtenemos los resultados
    for partido in partidos_equipo:
        try:
            # Acceder al resultado del partido
            resultado = Resultado.objects.get(id_partido=partido)
            
            # Guardar los detalles del partido junto con el resultado
            historial_partidos.append({
                'equipo_1': partido.id_equipo_1.nombre_equipo,
                'equipo_2': partido.id_equipo_2.nombre_equipo,
                'equipo_1_logo': partido.id_equipo_1.logo_equipo,
                'equipo_2_logo': partido.id_equipo_2.logo_equipo,
                'goles_equipo_1': resultado.goles_equipo_1,
                'goles_equipo_2': resultado.goles_equipo_2,
                'penales': resultado.penales,
                'penales_equipo_1': resultado.penales_equipo_1,
                'penales_equipo_2': resultado.penales_equipo_2,
                'fecha_partido': partido.fecha_partido,  # Fecha del partido
                'hora_partido': partido.hora_partido,    # Hora del partido
            })
        except Resultado.DoesNotExist:
            # Si no hay resultado, ignoramos este partido (o puedes manejarlo de otra forma)
            pass
        
    # Estadísticas Generales (sin tener en cuenta equipo o temporada)
    total_jugados_generales = Planilla.objects.filter(id_jugador=jugador_id, participo=True).count()

    # Obtener el total de goles marcados por el jugador en cualquier temporada y equipo
    total_goles_generales = Planilla.objects.filter(id_jugador=jugador_id, participo=True).aggregate(Sum('goles'))['goles__sum'] or 0

    # Obtener el total de tarjetas amarillas
    total_tarjetas_amarillas_generales = Planilla.objects.filter(id_jugador=jugador_id, tarjeta_amarilla=True).count()

    # Obtener el total de tarjetas rojas
    total_tarjetas_rojas_generales = Planilla.objects.filter(id_jugador=jugador_id, tarjeta_roja=True).count()
    
    # Recuperamos los premios del jugador, sin usar values()
    premios_individuales = PremioJugador.objects.filter(
        id_jugador=jugador
    ).select_related(
        'id_premio_individual', 'id_torneo', 'id_temporada'
    ).annotate(
        total_premios=Count('id_premio_individual')  # Cuenta cuántas veces se ha ganado el premio
    ).order_by('-total_premios')

    # Contexto para la plantilla de detalles
    context = {
        'jugador': jugador,
        'equipo': equipo,
        'temporada': temporada,
        'total_jugados': total_jugados,
        'total_goles': total_goles,
        'promedio_goles': promedio_goles,
        'total_tarjetas_amarillas': total_tarjetas_amarillas,
        'total_tarjetas_rojas': total_tarjetas_rojas,
        'traspasos': traspasos,
        'historial_partidos': historial_partidos,
        'total_jugados_generales': total_jugados_generales,
        'total_goles_generales': total_goles_generales,
        'total_tarjetas_amarillas_generales': total_tarjetas_amarillas_generales,
        'total_tarjetas_rojas_generales': total_tarjetas_rojas_generales,
        'premios_individuales': premios_individuales,
    }
    return render(request, 'jugador_detalles.html', context)


def partido_detalles(request, id_torneo, temporada_id, partido_id):
    # Recuperar el torneo (si necesario)
    torneo = get_object_or_404(Torneo, id=id_torneo)
    
    # Recuperar la temporada
    temporada = get_object_or_404(Temporada, id=temporada_id)

    # Recuperar el partido específico relacionado con el torneo y la temporada
    partido = get_object_or_404(Partido, id=partido_id, id_temporada=temporada, id_torneo=torneo)
    
    # Intentar obtener el resultado asociado directamente al partido
    resultado = Resultado.objects.filter(id_partido=partido).first()  # Usamos filter().first() en lugar de get_object_or_404
    
    # Si no existe un resultado, asignamos None
    if not resultado:
        resultado = None
    
    # Obtener las planillas de los equipos 1 y 2 para ese partido
    planilla_equipo_1 = Planilla.objects.filter(id_partido=partido, id_equipo=partido.id_equipo_1)
    planilla_equipo_2 = Planilla.objects.filter(id_partido=partido, id_equipo=partido.id_equipo_2)
    
    # Buscar la figura del partido (si existe)
    figura_equipo_1 = planilla_equipo_1.filter(figura=True).first()
    figura_equipo_2 = planilla_equipo_2.filter(figura=True).first()
    
    # Si la figura del equipo 1 existe, asignamos el jugador
    if figura_equipo_1:
        figura_equipo_1_jugador = figura_equipo_1.id_jugador
    else:
        figura_equipo_1_jugador = None
    
    # Si la figura del equipo 2 existe, asignamos el jugador
    if figura_equipo_2:
        figura_equipo_2_jugador = figura_equipo_2.id_jugador
    else:
        figura_equipo_2_jugador = None
    
    # Contar la cantidad de enfrentamientos entre los dos equipos
    enfrentamientos = Partido.objects.filter(
        Q(id_equipo_1=partido.id_equipo_1, id_equipo_2=partido.id_equipo_2) |
        Q(id_equipo_1=partido.id_equipo_2, id_equipo_2=partido.id_equipo_1)
    ).count()

    # Contar las victorias del equipo 1
    victorias_equipo_1 = Resultado.objects.filter(
    Q(id_partido__id_equipo_1=partido.id_equipo_1, goles_equipo_1__gt=F('goles_equipo_2')) |
    Q(id_partido__id_equipo_2=partido.id_equipo_1, goles_equipo_2__gt=F('goles_equipo_1')),
    Q(id_partido__id_equipo_1=partido.id_equipo_1, id_partido__id_equipo_2=partido.id_equipo_2) |
    Q(id_partido__id_equipo_1=partido.id_equipo_2, id_partido__id_equipo_2=partido.id_equipo_1)  # Filtramos solo los partidos entre Barcelona y Boca
    ).count()

    # Contar las victorias del equipo 2
    victorias_equipo_2 = Resultado.objects.filter(
    Q(id_partido__id_equipo_1=partido.id_equipo_2, goles_equipo_1__gt=F('goles_equipo_2')) |
    Q(id_partido__id_equipo_2=partido.id_equipo_2, goles_equipo_2__gt=F('goles_equipo_1')),
    Q(id_partido__id_equipo_1=partido.id_equipo_1, id_partido__id_equipo_2=partido.id_equipo_2) |
    Q(id_partido__id_equipo_1=partido.id_equipo_2, id_partido__id_equipo_2=partido.id_equipo_1)  # Filtramos solo los partidos entre Barcelona y Boca
    ).count()
    
    # Historial de enfrentamientos entre los dos equipos, limitando a los últimos 5 partidos
    enfrentamientos_partidos = Partido.objects.filter(
        Q(id_equipo_1=partido.id_equipo_1, id_equipo_2=partido.id_equipo_2) |
        Q(id_equipo_1=partido.id_equipo_2, id_equipo_2=partido.id_equipo_1)
    ).filter(resultado__isnull=False).order_by('-fecha_partido')[:5]  # Últimos 5 partidos, ordenados por fecha descendente

    # Historial de los enfrentamientos con los resultados
    historial = []
    for enfrentamiento in enfrentamientos_partidos:
        # Usar filter().first() para obtener el resultado sin generar un error 404
        resultado_partido = Resultado.objects.filter(id_partido=enfrentamiento).first()
    
        # Si no hay resultado, asignamos una cadena vacía
        historial.append({
            'equipo_1': enfrentamiento.id_equipo_1.nombre_equipo,
            'equipo_1_logo': enfrentamiento.id_equipo_1.logo_equipo.url if enfrentamiento.id_equipo_1.logo_equipo else None,
            'equipo_2': enfrentamiento.id_equipo_2.nombre_equipo,
            'equipo_2_logo': enfrentamiento.id_equipo_2.logo_equipo.url if enfrentamiento.id_equipo_2.logo_equipo else None,
            'goles_equipo_1': resultado_partido.goles_equipo_1 if resultado_partido else '',
            'goles_equipo_2': resultado_partido.goles_equipo_2 if resultado_partido else '',
            'penales': resultado_partido.penales if resultado_partido else '',
            'penales_equipo_1': resultado_partido.penales_equipo_1 if resultado_partido else '',
            'penales_equipo_2': resultado_partido.penales_equipo_2 if resultado_partido else '',
        })
        
    # Historial de los últimos 5 partidos del equipo 1 con resultado en la temporada
    partidos_equipo_1 = Partido.objects.filter(
        Q(id_equipo_1=partido.id_equipo_1) | Q(id_equipo_2=partido.id_equipo_1),
        id_temporada=temporada
    ).filter(resultado__isnull=False).order_by('-fecha_partido')[:5]

    # Historial de los últimos 5 partidos del equipo 2 con resultado en la temporada
    partidos_equipo_2 = Partido.objects.filter(
        Q(id_equipo_1=partido.id_equipo_2) | Q(id_equipo_2=partido.id_equipo_2),
        id_temporada=temporada
    ).filter(resultado__isnull=False).order_by('-fecha_partido')[:5]

    # Historial de partidos con los resultados para el equipo 1
    historial_equipo_1 = []
    for enfrentamiento in partidos_equipo_1:
        resultado_partido = Resultado.objects.filter(id_partido=enfrentamiento).first()
        historial_equipo_1.append({
            'equipo_1': enfrentamiento.id_equipo_1.nombre_equipo,
            'equipo_1_logo': enfrentamiento.id_equipo_1.logo_equipo.url if enfrentamiento.id_equipo_1.logo_equipo else None,
            'equipo_2': enfrentamiento.id_equipo_2.nombre_equipo,
            'equipo_2_logo': enfrentamiento.id_equipo_2.logo_equipo.url if enfrentamiento.id_equipo_2.logo_equipo else None,
            'goles_equipo_1': resultado_partido.goles_equipo_1 if resultado_partido else '',
            'goles_equipo_2': resultado_partido.goles_equipo_2 if resultado_partido else '',
            'penales': resultado_partido.penales if resultado_partido else '',
            'penales_equipo_1': resultado_partido.penales_equipo_1 if resultado_partido else '',
            'penales_equipo_2': resultado_partido.penales_equipo_2 if resultado_partido else '',
        })

    # Historial de partidos con los resultados para el equipo 2
    historial_equipo_2 = []
    for enfrentamiento in partidos_equipo_2:
        resultado_partido = Resultado.objects.filter(id_partido=enfrentamiento).first()
        historial_equipo_2.append({
            'equipo_1': enfrentamiento.id_equipo_1.nombre_equipo,
            'equipo_1_logo': enfrentamiento.id_equipo_1.logo_equipo.url if enfrentamiento.id_equipo_1.logo_equipo else None,
            'equipo_2': enfrentamiento.id_equipo_2.nombre_equipo,
            'equipo_2_logo': enfrentamiento.id_equipo_2.logo_equipo.url if enfrentamiento.id_equipo_2.logo_equipo else None,
            'goles_equipo_1': resultado_partido.goles_equipo_1 if resultado_partido else '',
            'goles_equipo_2': resultado_partido.goles_equipo_2 if resultado_partido else '',
            'penales': resultado_partido.penales if resultado_partido else '',
            'penales_equipo_1': resultado_partido.penales_equipo_1 if resultado_partido else '',
            'penales_equipo_2': resultado_partido.penales_equipo_2 if resultado_partido else '',
        })
    
    # Contexto para la plantilla
    context = {
        'torneo': torneo,
        'partido': partido,
        'temporada': temporada,
        'resultado': resultado,
        'planilla_equipo_1': planilla_equipo_1,
        'planilla_equipo_2': planilla_equipo_2,
        'figura_equipo_1_jugador': figura_equipo_1_jugador,
        'figura_equipo_2_jugador': figura_equipo_2_jugador,
        'enfrentamientos': enfrentamientos,
        'victorias_equipo_1': victorias_equipo_1,
        'victorias_equipo_2': victorias_equipo_2,
        'enfrentamientos_partidos': historial,
        'historial_equipo_1': historial_equipo_1,
        'historial_equipo_2': historial_equipo_2,
    }
    
    return render(request, 'partido_detalles.html', context)

