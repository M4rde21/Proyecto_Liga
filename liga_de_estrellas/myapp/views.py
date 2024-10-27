from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Equipo, Torneo, Temporada, Categoria, TipoTorneo, Jugador, Equipo, Entrenador, Grupo, TemporadaXTorneoXEquipoXJugador
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm, CrearZonaForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError



# Create your views here.
def inicio(request):
    return render(request, 'usuario/inicio.html')


def login_view(request):
    return render(request, 'login.html')


def resumen(request):
    return render(request, 'administracion/resumen.html')

def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'administracion/jugadores.html', {'jugadores': jugadores})

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


def torneos_adm(request):
    torneos = Torneo.objects.all()
    return render(request, 'administracion/torneos_adm.html', {
        'torneos': torneos
    })


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


def temporadas_adm(request):
    temporadas = Temporada.objects.all()
    return render(request, 'administracion/temporadas_adm.html', {
        'temporadas': temporadas
    }) 


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

    for zona in zonas:
        # Obtener solo los equipos importados para la zona actual
        zona.equipos_importados = TemporadaXTorneoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_jugador=None,
            id_equipo__in=TemporadaXTorneoXEquipoXJugador.objects.filter(
                id_temporada=temporada,
                id_jugador=None,
                id_equipo__isnull=False
            ).values_list('id_equipo', flat=True)
        ).filter(id_equipo__in=TemporadaXTorneoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_jugador=None,
            # Filtrar por la zona actual aquí
            # Esto funcionaría si tuvieras un campo de grupo en el modelo Equipo
            # id_equipo__id_grupo=zona  # Aquí sería si tuvieras el id_grupo
        ).values_list('id_equipo', flat=True))

    return render(request, 'administracion/zonas.html', {
        'temporada': temporada,
        'zonas': zonas,
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



def importar_equipos_zona(request, id_temporada, id_zona):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=temporada)
    equipos = Equipo.objects.all()

    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        equipo = get_object_or_404(Equipo, pk=equipo_id)

        # Verificar si ya existe la relación para la temporada y la zona actual
        existing_relation = TemporadaXTorneoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_equipo=equipo,
            id_jugador=None  # Suponiendo que deseas que el jugador sea None
        ).exists()

        if not existing_relation:  # Solo crea la relación si no existe
            TemporadaXTorneoXEquipoXJugador.objects.create(
                id_temporada=temporada,
                id_torneo=temporada.id_torneo,
                id_equipo=equipo,
                id_jugador=None
            )

        return redirect('zonas', id_temporada=id_temporada)

    return render(request, 'administracion/importar_equipos_zona.html', {'zona': zona, 'temporada': temporada, 'equipos': equipos})






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
                # Si hay una nueva foto, la actualizamos
                entrenador.foto_entrenador = form.cleaned_data['foto_entrenador']
            elif form.cleaned_data['foto_entrenador'] is None:
                # Si no hay una nueva foto y el campo está vacío, no cambiamos la imagen
                pass
            else:
                # Si el campo fue enviado vacío explícitamente, borramos la foto actual
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