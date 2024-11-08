from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from .models import Equipo, Torneo, Temporada, Categoria,TipoTorneo, Jugador, Entrenador, Aviso
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm, AvisoForm
from django.views import View
from django.conf import settings  # Importa settings para acceder a MEDIA_URL


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

def avisos(request):
    # Filtra solo los avisos que están activos (mostrar = True)
    avisos_activos = Aviso.objects.filter(activo=True)
    return render(request, 'avisos.html', {'avisos': avisos_activos})

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



def avisos_adm(request):
    avisos = Aviso.objects.all()
    form_crear = AvisoForm()  # Formulario para el modal de creación

    # Añadir un formulario de edición para cada aviso al queryset
    for aviso in avisos:
        aviso.form_editar = AvisoForm(initial={
            'titulo': aviso.titulo,
            'mensaje': aviso.mensaje,
            'mostrar': aviso.mostrar,
        })

    context = {
        'avisos': avisos,
        'form_crear': form_crear,
    }
    
    return render(request, 'administracion/avisos_adm.html', context)

def crear_aviso(request):
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo aviso en la base de datos
            Aviso.objects.create(
                titulo=form.cleaned_data['titulo'],
                mensaje=form.cleaned_data['mensaje'],
                mostrar=form.cleaned_data['mostrar'],
            )
            return redirect('avisos_adm')  # Redirige a la lista de avisos después de guardar
    else:
        form = AvisoForm()
    
    return render(request, 'administracion/crear_aviso.html', {'form': form})

def edit_aviso(request, id_aviso):
    aviso = get_object_or_404(Aviso, id=id_aviso)

    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            # Actualizar los campos del aviso
            aviso.titulo = form.cleaned_data['titulo']
            aviso.mensaje = form.cleaned_data['mensaje']
            aviso.mostrar = form.cleaned_data['mostrar']
            aviso.save()
            return redirect('avisos_adm')  # Redirige a la lista de avisos después de guardar
    else:
        form = AvisoForm(initial={
            'titulo': aviso.titulo,
            'mensaje': aviso.mensaje,
            'mostrar': aviso.mostrar,
        })

    return render(request, 'administracion/edit_aviso.html', {'form': form, 'aviso': aviso})

def delete_aviso(request, id_aviso):
    aviso = get_object_or_404(Aviso, pk=id_aviso)
    if request.method == 'POST':
        aviso.delete()
        return redirect('avisos_adm')