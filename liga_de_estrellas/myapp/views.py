from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from .models import Equipo, Torneo, Temporada, Categoria,TipoTorneo, Jugador, Entrenador, PremiosIndividual, PremiosGrupal, Grupo, TemporadaXTorneoXGrupoXEquipoXJugador, PremioEquipo, PremioJugador, Fecha, Partido, Predio, TablaDePosicion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm, CrearPremioGrupalForm, CrearPremioIndividualForm, CrearZonaForm, CrearFechaForm, CrearPartidoForm
from django.views import View
from django.conf import settings  # Importa settings para acceder a MEDIA_URL
from django.urls import reverse 
from django.contrib import messages
from django.core.exceptions import ValidationError


# Create your views here.
def home(request):
    return HttpResponse('La Mejor Liga del Condado')

def inicio(request):
    return render(request, 'inicio.html')

def torneo(request):
    torneo = Torneo.objects.all()
    return render(request, 'torneos.html', {'torneos': torneo})

def reglamento(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def resumen_adm(request):
    return render(request, 'administracion/resumen_adm.html')


def login_view(request):
    return render(request, 'login.html')
        
def signout(request):
    logout(request)
    return redirect('inicio')





def torneos_adm(request):
    torneos = Torneo.objects.all()

    context = {
        'torneos': torneos,
    }
    
    return render(request, 'administracion/torneos_adm.html', context)


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
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    if request.method == 'POST':
        temporada.delete()
        return redirect('temporadas_adm')




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
                foto_jugador=form.cleaned_data['foto_jugador'] or 'fotos_jugador/jugador_default.png',
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
            'fecha_nac_jugador': jugador.fecha_nac_jugador,
            'activo_jugador': jugador.activo_jugador,
            'foto_jugador': jugador.foto_jugador
        })
        
        # URL de la imagen actual o predeterminada
        foto_url = jugador.foto_jugador.url if jugador.foto_jugador else f"{settings.MEDIA_URL}fotos_jugador/jugador_default.png"
        
        return render(request, 'administracion/editar_jugador.html', {
            'form': form,
            'jugador': jugador,
            'foto_url': foto_url
        })
    
    else:
        form = CrearJugadorForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Actualizar los datos del jugador con los datos del formulario
            jugador.nombre_jugador = form.cleaned_data['nombre_jugador']
            jugador.apellido_jugador = form.cleaned_data['apellido_jugador']
            jugador.dni_jugador = form.cleaned_data['dni_jugador']
            jugador.fecha_nac_jugador = form.cleaned_data['fecha_nac_jugador']
            jugador.activo_jugador = form.cleaned_data['activo_jugador']
            
            # Verificar si hay un nuevo archivo para la foto
            if 'foto_jugador' in request.FILES:
                # Si hay una foto anterior, eliminarla del sistema de archivos
                if jugador.foto_jugador:
                    jugador.foto_jugador.delete(save=False)
                # Asignar la nueva foto
                jugador.foto_jugador = form.cleaned_data['foto_jugador']
            else:
                # Si no se subió una nueva foto, verificar si se debe eliminar la existente
                if 'borrar_foto' in request.POST and request.POST['borrar_foto'] == 'on':
                    if jugador.foto_jugador:
                        jugador.foto_jugador.delete(save=False)  # Eliminar del sistema de archivos
                    jugador.foto_jugador = None  # O asignar a un valor por defecto
            
            # Guardar los cambios en el modelo
            jugador.save()
            return redirect('jugadores') 
        else:
            # Mostrar errores del formulario si no es válido
            foto_url = jugador.foto_jugador.url if jugador.foto_jugador else f"{settings.MEDIA_URL}fotos_jugador/jugador_default.png"
            return render(request, 'administracion/editar_jugador.html', {
                'form': form,
                'jugador': jugador,
                'foto_url': foto_url,
                'error': 'Por favor introduce datos válidos.'
            })


def eliminar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    if request.method == 'POST':
        jugador.delete()
        return redirect('jugadores')


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
        # Obtén la URL de la imagen actual del logo si existe
        logo_url = equipo.logo_equipo.url if equipo.logo_equipo else f"{settings.MEDIA_URL}logos/logo_default.jpg"
        
        return render(request, 'administracion/equipo_editar.html', {
            'form': form,
            'equipo': equipo,
            'logo_url': logo_url
        })
    
    else:
        form = CrearEquipoForm(request.POST, request.FILES)
        
        if form.is_valid():
            equipo.nombre_equipo = form.cleaned_data['nombre_equipo']
            
            # Verificar si el logo está en los archivos subidos
            if 'logo_equipo' in request.FILES:
                equipo.logo_equipo = form.cleaned_data['logo_equipo']
            else:
                # Si no hay archivo y el usuario ha borrado el logo
                equipo.logo_equipo.delete(save=False)
                equipo.logo_equipo = f"logos/logo_default.jpg"  # Asignamos la ruta predeterminada
            
            equipo.save()
    
            return redirect('equipos') 
        else:
            logo_url = equipo.logo_equipo.url if equipo.logo_equipo else f"{settings.MEDIA_URL}logos/logo_default.jpg"
            return render(request, 'administracion/equipo_editar.html', {
                'form': form,
                'equipo': equipo,
                'logo_url': logo_url,
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

        # URL de la imagen actual o predeterminada
        foto_url = entrenador.foto_entrenador.url if entrenador.foto_entrenador else f"{settings.MEDIA_URL}fotos_jugador/jugador_default.png"

        return render(request, 'administracion/entrenador_editar.html', {
            'form': form,
            'entrenador': entrenador,
            'foto_url': foto_url
        })
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Actualizar los datos del entrenador con los datos del formulario
            entrenador.nombre_entrenador = form.cleaned_data['nombre_entrenador']
            entrenador.apellido_entrenador = form.cleaned_data['apellido_entrenador']
            entrenador.dni_entrenador = form.cleaned_data['dni_entrenador']
            entrenador.fecha_nac_entrenador = form.cleaned_data['fecha_nac_entrenador']

            # Verificar si hay un nuevo archivo para la foto
            if 'foto_entrenador' in request.FILES:
                # Si hay una foto anterior, eliminarla del sistema de archivos
                if entrenador.foto_entrenador:
                    entrenador.foto_entrenador.delete(save=False)
                # Asignar la nueva foto
                entrenador.foto_entrenador = form.cleaned_data['foto_entrenador']
            else:
                # Si no se subió una nueva foto, verificar si se debe eliminar la existente
                if 'borrar_foto' in request.POST and request.POST['borrar_foto'] == 'on':
                    if entrenador.foto_entrenador:
                        entrenador.foto_entrenador.delete(save=False)  # Eliminar del sistema de archivos
                    entrenador.foto_entrenador = None  # O asignar a un valor por defecto

            # Guardar los cambios en el modelo
            entrenador.save()
            return redirect('entrenadores') 
        else:
            # Mostrar errores del formulario si no es válido
            foto_url = entrenador.foto_entrenador.url if entrenador.foto_entrenador else f"{settings.MEDIA_URL}fotos_jugador/jugador_default.png"
            return render(request, 'administracion/entrenador_editar.html', {
                'form': form,
                'entrenador': entrenador,
                'foto_url': foto_url,
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
            return redirect('zonas', id_temporada=id_temporada)
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

        # Verificar si la relación ya existe
        relacion = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_equipo=equipo,
            id_grupo=zona,
            id_jugador=None
        ).exists()

        if relacion:
            messages.info(request, f'El equipo {equipo} ya se encuentra en la zona')
        else:
            # Crear la relación en TemporadaXTorneoXGrupoXEquipoXJugador
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
                id_temporada=temporada,
                id_torneo=temporada.id_torneo,
                id_equipo=equipo,
                id_grupo=zona,
                id_jugador=None
            )

            # Verificar si la entrada en la tabla de posiciones ya existe
            existe_posicion = TablaDePosicion.objects.filter(
                id_temporada=temporada,
                id_grupo=zona,
                id_equipo=equipo
            ).exists()

            if not existe_posicion:
                # Crear una entrada en la tabla de posiciones
                TablaDePosicion.objects.create(
                    id_temporada=temporada,
                    id_grupo=zona,
                    id_equipo=equipo,
                    puntos=0,  # Inicializar con 0 puntos
                    partidos_jugados=0,
                    partidos_ganados=0,
                    partidos_empatados=0,
                    partidos_perdidos=0,
                    goles_a_favor=0,
                    goles_en_contra=0,
                    diferencia_goles=0,
                    tarjetas_amarillas=0,
                    tarjetas_rojas=0
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
        'premios_asignados': premios_asignados,  # Premios asignados al equipo
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
        
        existe_equipo_en_zona = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada = temporada,
            id_torneo = torneo,
            id_grupo = grupo,
            id_equipo = nuevo_equipo,  
        )
        
        if existe_equipo_en_zona:
            messages.info(request, f'El equipo {nuevo_equipo} ya existe en esta zona')

        elif nuevo_equipo != relacion.id_equipo:
            # Eliminar todas las relaciones existentes del equipo actual en esta zona
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo=relacion.id_equipo
            ).delete()

            # Crear una nueva relación con el equipo seleccionado
            TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
                id_temporada=temporada,
                id_torneo=torneo,
                id_grupo=grupo,
                id_equipo=nuevo_equipo,
                id_jugador=None
            )
                

            # Actualizar la tabla de posiciones
            # Eliminar la entrada existente del equipo actual
            TablaDePosicion.objects.filter(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo=relacion.id_equipo
            ).delete()

            # Crear una nueva entrada en la tabla de posiciones para el nuevo equipo
            TablaDePosicion.objects.create(
                id_temporada=temporada,
                id_grupo=grupo,
                id_equipo=nuevo_equipo,
                puntos=0,  # Inicializar con 0 puntos
                partidos_jugados=0,
                partidos_ganados=0,
                partidos_empatados=0,
                partidos_perdidos=0,
                goles_a_favor=0,
                goles_en_contra=0,
                diferencia_goles=0,
                tarjetas_amarillas=0,
                tarjetas_rojas=0
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
    # Filtramos todas las relaciones que coinciden con los parámetros en TemporadaXTorneoXGrupoXEquipoXJugador
    relaciones = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo
    )

    # Verificamos si hay relaciones que eliminar y las eliminamos
    if relaciones.exists():
        relaciones.delete()  # Eliminar todas las relaciones que coincidan

    # Ahora, eliminar las entradas en TablaDePosicion que coincidan con los mismos parámetros
    posiciones = TablaDePosicion.objects.filter(
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo
    )

    # Verificamos si hay posiciones que eliminar y las eliminamos
    if posiciones.exists():
        posiciones.delete()  # Eliminar todas las posiciones que coincidan

    # Redirigir a la página de zonas
    return redirect('zonas', id_temporada=id_temporada)


def importar_jugador_equipo(request, id_temporada, id_zona, id_equipo):
    # Obtener la temporada y la zona
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    zona = get_object_or_404(Grupo, pk=id_zona, id_temporada=temporada)

    # Obtener todos los jugadores disponibles
    jugadores_disponibles = Jugador.objects.all()

    # Obtener la instancia del equipo
    equipo_instancia = get_object_or_404(Equipo, pk=id_equipo)

    if request.method == 'POST':
        jugador_id = request.POST.get('jugador')
        jugador = get_object_or_404(Jugador, pk=jugador_id)

        # Verificar si el jugador ya está importado en el equipo y zona especificados
        existe_relacion = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
            id_temporada=temporada,
            id_grupo=zona,
            id_equipo=equipo_instancia,
            id_jugador=jugador
        ).exists()

        if existe_relacion:
            messages.info(request, f'El jugador {jugador} ya está en el equipo.')
            return render(request, 'administracion/importar_jugador_equipo.html', {
                'zona': zona,
                'temporada': temporada,
                'jugadores': jugadores_disponibles,
                'equipo': equipo_instancia
            })

        # Crear una nueva relación con el jugador en la zona seleccionada
        TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
            id_temporada=temporada,
            id_torneo=temporada.id_torneo,
            id_grupo=zona,
            id_equipo=equipo_instancia,
            id_jugador=jugador
        )

        # Ahora agregar el jugador al mismo equipo en otras zonas de la misma temporada
        otras_zonas = Grupo.objects.filter(id_temporada=temporada).exclude(id=zona.id)
        for otra_zona in otras_zonas:
            # Verificar si el equipo está en la zona actual antes de agregar al jugador
            equipo_en_otra_zona = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                id_temporada=temporada,
                id_grupo=otra_zona,
                id_equipo=equipo_instancia
            ).exists()

            if equipo_en_otra_zona:
                # Verificar si el jugador ya está en esa zona para evitar duplicados
                existe_relacion_otra_zona = TemporadaXTorneoXGrupoXEquipoXJugador.objects.filter(
                    id_temporada=temporada,
                    id_grupo=otra_zona,
                    id_equipo=equipo_instancia,
                    id_jugador=jugador
                ).exists()

                if not existe_relacion_otra_zona:
                    # Crear la relación en la otra zona
                    TemporadaXTorneoXGrupoXEquipoXJugador.objects.create(
                        id_temporada=temporada,
                        id_torneo=temporada.id_torneo,
                        id_grupo=otra_zona,
                        id_equipo=equipo_instancia,
                        id_jugador=jugador
                    )

        messages.success(request, 'Jugador importado correctamente en el equipo de la zona en la temporada actual y en otras zonas del equipo.')
        return redirect(reverse('equipo_importado', args=[id_temporada, id_zona, id_equipo]))

    return render(request, 'administracion/importar_jugador_equipo.html', {
        'zona': zona,
        'temporada': temporada,
        'jugadores': jugadores_disponibles,
        'equipo': equipo_instancia
    })


def eliminar_jugador_equipo(request, id_temporada, id_zona, id_equipo, id_jugador):
    # Obtener la relación que corresponde al jugador específico
    relacion = get_object_or_404(
        TemporadaXTorneoXGrupoXEquipoXJugador,
        id_temporada=id_temporada,
        id_grupo=id_zona,
        id_equipo=id_equipo,
        id_jugador=id_jugador
    )

    # Eliminar la relación
    relacion.delete()

    # Mostrar un mensaje de éxito
    messages.success(request, 'El jugador ha sido eliminado exitosamente.')

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



def fechas(request,id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    fechas = Fecha.objects.filter(id_temporada=temporada)  
    return render(request, 'administracion/fechas.html', {
        'fechas': fechas,
        'temporada': temporada,  
    })

def crear_fecha(request,id_temporada):
    temporada = get_object_or_404(Temporada, pk=id_temporada)
    if request.method == 'POST':
        form = CrearFechaForm(request.POST)
        if form.is_valid():
            fecha = Fecha(
                nombre_fecha=form.cleaned_data['nombre_fecha'],
                id_temporada=temporada              )
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
