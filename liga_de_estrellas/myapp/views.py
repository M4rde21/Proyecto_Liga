from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import Equipo, Torneo, Temporada, Categoria,TipoTorneo, Jugador, Equipo, Entrenador, PremiosGrupal, PremiosIndividual, Grupo, TemporadaXTorneoXGrupoXEquipoXJugador, Fecha, Partido, Resultado, Planilla
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm, CrearPremioGrupalForm, CrearPremioIndividualForm,CrearZonaForm, CrearFechaForm, CrearPartidoForm, ResultadoForm, PlanillaForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib import messages
from django.forms import formset_factory, modelformset_factory




def inicio(request):
    return render(request, 'usuario/inicio.html')


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
    return render(request, 'administracion/temporadas_adm.html', {
        'temporadas': temporadas
    })


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
    ).first()  # Usamos first() para obtener solo el primer resultado o None

    if relacion is None:
        # Manejar el caso en que no se encontró la relación
        return render(request, 'administracion/error.html', {
            'mensaje': 'No se encontró la relación entre la temporada, la zona y el equipo especificados.'
        })

    equipo = relacion.id_equipo 
    equipos = Equipo.objects.all()  # Obtener todos los equipos disponibles
    
    # Obtener todos los jugadores importados para este equipo
    jugadores_importados = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=equipo
    ).select_related('id_jugador')  # Usamos select_related para obtener los jugadores

    return render(request, 'administracion/equipo_importado.html', {
        'equipo': equipo,
        'temporada': relacion.id_temporada,
        'zona': relacion.id_grupo,
        'equipos': equipos,
        'jugadores_importados': jugadores_importados
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


# def crear_planilla(request, id_temporada, id_fecha, id_partido):
#     temporada = get_object_or_404(Temporada, pk=id_temporada)
#     fecha = get_object_or_404(Fecha, pk=id_fecha)
#     partido = get_object_or_404(Partido, pk=id_partido)
#     torneo = temporada.id_torneo

#     # Filtrar jugadores por equipos, temporada, torneo y grupo del partido
#     jugadores = Jugador.objects.filter(
#         id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
#             id_temporada=temporada,
#             id_torneo=torneo,
#             id_grupo=partido.id_grupo,
#         ).values('id_jugador')
#     ).distinct()

#     # Crear un formset para gestionar los formularios de cada jugador
#     PlanillaFormSet = formset_factory(PlanillaForm, extra=0)
#     initial_data = [{'participo': False} for jugador in jugadores]
#     formset = PlanillaFormSet(initial=initial_data)

#     # Emparejar jugadores con formularios
#     jugadores_formularios = zip(jugadores, formset)

#     if request.method == 'POST':
#         formset = PlanillaFormSet(request.POST)

#         if formset.is_valid():
#             print("Formset válido, iniciando proceso de guardado...")
#             try:
#                 for form, jugador in zip(formset, jugadores):
#                     if form.cleaned_data['participo']:
#                         print(f"Guardando planilla para el jugador {jugador.nombre_jugador}")
#                         Planilla.objects.create(
#                             id_partido=partido,
#                             id_equipo=TemporadaXTorneoXGrupoXEquipoXJugador.objects.get(
#                                 id_jugador=jugador,
#                                 id_temporada=temporada,
#                                 id_torneo=torneo,
#                                 id_grupo=partido.id_grupo
#                             ).id_equipo,
#                             id_jugador=jugador,
#                             goles=form.cleaned_data['goles'],
#                             num_camiseta=form.cleaned_data['num_camiseta'],
#                             participo=form.cleaned_data['participo'],
#                             tarjeta_amarilla=form.cleaned_data['tarjeta_amarilla'],
#                             tarjeta_roja=form.cleaned_data['tarjeta_roja'],
#                             figura=form.cleaned_data['figura']
#                         )
#                 print("Todos los datos se guardaron correctamente.")
#                 return redirect('fechas', id_temporada=id_temporada)
#             except Exception as e:
#                 print(f"Error durante el guardado: {e}")
#         else:
#             print("El formset no es válido, errores:", formset.errors)

#     return render(request, 'administracion/crear_planilla.html', {
#         'temporada': temporada,
#         'fecha': fecha,
#         'partido': partido,
#         'jugadores_formularios': jugadores_formularios,
#         'formset_errors': formset.errors,
#     })


def gestionar_partido(request, id_temporada, id_fecha, id_partido):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fecha = get_object_or_404(Fecha, pk=id_fecha)
    partido = get_object_or_404(Partido, pk=id_partido)

    # Obtener o inicializar el resultado del partido
    resultado, created = Resultado.objects.get_or_create(id_partido=partido)

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

    # Formularios
    resultado_form = ResultadoForm(request.POST or None)
    jugadores_formularios = {}

    # Crear formularios de planilla para cada jugador
    for jugador in jugadores_equipo_1 | jugadores_equipo_2:
        form = PlanillaForm(request.POST or None, prefix=f'jugador_{jugador.id}')
        jugadores_formularios[jugador] = form

    if request.method == 'POST':
        # Procesar el formulario de resultado manualmente
        if 'resultado_submit' in request.POST and resultado_form.is_valid():
            # Obtener los datos del formulario
            goles_equipo_1 = resultado_form.cleaned_data.get('goles_equipo_1', 0)
            goles_equipo_2 = resultado_form.cleaned_data.get('goles_equipo_2', 0)
            penales = resultado_form.cleaned_data.get('penales', False)
            penales_equipo_1 = resultado_form.cleaned_data.get('penales_equipo_1', 0)
            penales_equipo_2 = resultado_form.cleaned_data.get('penales_equipo_2', 0)

            # Actualizar o crear el resultado
            resultado.goles_equipo_1 = goles_equipo_1
            resultado.goles_equipo_2 = goles_equipo_2
            resultado.penales = penales
            resultado.penales_equipo_1 = penales_equipo_1
            resultado.penales_equipo_2 = penales_equipo_2
            resultado.save()

        # Procesar las planillas
        if 'planilla_submit' in request.POST:
            for jugador, form in jugadores_formularios.items():
                if form.is_valid():
                    participo = form.cleaned_data.get('participo', False)

                    if participo:
                        # Solo guardamos la planilla si el jugador participó
                        Planilla.objects.create(
                            id_partido=partido,
                            id_equipo=equipo_1 if jugador in jugadores_equipo_1 else equipo_2,
                            id_jugador=jugador,
                            goles=form.cleaned_data['goles'] or 0,
                            num_camiseta=form.cleaned_data['num_camiseta'] or 0,
                            participo=participo,
                            tarjeta_amarilla=form.cleaned_data['tarjeta_amarilla'],
                            tarjeta_roja=form.cleaned_data['tarjeta_roja'],
                            figura=form.cleaned_data['figura']
                        )
                    else:
                        # Si el jugador no participó, no se guarda nada
                        pass

            # Redirigir a la vista de fechas
            return redirect('fechas', id_temporada=temporada.id)

    return render(request, 'administracion/gestionar_partido.html', {
        'temporada': temporada,
        'fecha': fecha,
        'partido': partido,
        'equipo_1': equipo_1,
        'equipo_2': equipo_2,
        'resultado_form': resultado_form,
        'jugadores_formularios': jugadores_formularios,
        'jugadores_equipo_1': jugadores_equipo_1,
        'jugadores_equipo_2': jugadores_equipo_2,
    })







# def gestion_partido(request, id_temporada, id_fecha, id_partido):
#     # Obtener la temporada, fecha, y partido
#     temporada = get_object_or_404(Temporada, pk=id_temporada)
#     fecha = get_object_or_404(Fecha, pk=id_fecha)
#     partido = get_object_or_404(Partido, pk=id_partido)
#     torneo = temporada.id_torneo

#     # Obtener los equipos del partido
#     equipo_1 = partido.id_equipo_1
#     equipo_2 = partido.id_equipo_2

#     # Filtrar jugadores por equipos, temporada, torneo y grupo del partido
#     jugadores = Jugador.objects.filter(
#         id__in=TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
#             id_temporada=temporada,
#             id_torneo=torneo,
#             id_grupo=partido.id_grupo,
#         ).values('id_jugador')
#     ).distinct()

#     # Crear el formset para los formularios de Planilla
#     PlanillaFormSet = formset_factory(PlanillaForm, extra=0)

#     if request.method == 'POST':
#         resultado_form = ResultadoForm(request.POST)
#         formset = PlanillaFormSet(request.POST)

#         if resultado_form.is_valid() and formset.is_valid():
#             # Guardar el resultado
#             resultado = Resultado(
#                 id_partido=partido,
#                 goles_equipo_1=resultado_form.cleaned_data['goles_equipo_1'],
#                 goles_equipo_2=resultado_form.cleaned_data['goles_equipo_2'],
#                 penales=resultado_form.cleaned_data['penales'],
#                 penales_equipo_1=resultado_form.cleaned_data['penales_equipo_1'] if resultado_form.cleaned_data['penales'] else 0,
#                 penales_equipo_2=resultado_form.cleaned_data['penales_equipo_2'] if resultado_form.cleaned_data['penales'] else 0
#             )
#             resultado.save()

#             # Guardar las planillas para los jugadores
#             for form, jugador in zip(formset, jugadores):
#                 if form.cleaned_data.get('participo', False):
#                     Planilla.objects.create(
#                         id_partido=partido,
#                         id_equipo=TemporadaXTorneoXGrupoXEquipoXJugador.objects.get(
#                             id_jugador=jugador,
#                             id_temporada=temporada,
#                             id_torneo=torneo,
#                             id_grupo=partido.id_grupo
#                         ).id_equipo,
#                         id_jugador=jugador,
#                         goles=form.cleaned_data.get('goles', 0),
#                         num_camiseta=form.cleaned_data.get('num_camiseta', ''),
#                         participo=form.cleaned_data['participo'],
#                         tarjeta_amarilla=form.cleaned_data.get('tarjeta_amarilla', False),
#                         tarjeta_roja=form.cleaned_data.get('tarjeta_roja', False),
#                         figura=form.cleaned_data.get('figura', False)
#                     )

#             return redirect('fechas', id_temporada=id_temporada)  # Redirigir a la vista de fechas
#         else:
#             # Depuración de errores
#             print("Errores en resultado_form:", resultado_form.errors.as_json())
#             print("Errores en formset:", formset.errors)
#     else:
#         # Inicializar los formularios en GET
#         resultado_form = ResultadoForm()
#         initial_data = [{'participo': False} for _ in jugadores]
#         formset = PlanillaFormSet(initial=initial_data)

#     return render(request, 'administracion/gestion_partido.html', {
#         'temporada': temporada,
#         'fecha': fecha,
#         'partido': partido,
#         'equipo_1': equipo_1,
#         'equipo_2': equipo_2,
#         'resultado_form': resultado_form,
#         'formset': formset,
#         'jugadores_formularios': zip(jugadores, formset),
#     })