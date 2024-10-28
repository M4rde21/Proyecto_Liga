from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Equipo, Torneo, Temporada, Categoria,TipoTorneo, Jugador, Equipo, Entrenador
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm, CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError



# Create your views here.
def inicio(request):
    return render(request, 'usuario/inicio.html')

def torneos(request):
    torneos = Torneo.objects.all()
    return render(request, 'usuario/torneos.html', {'torneos': torneos})

def reglamentos(request):
    return render(request, 'usuario/reglamentos.html')

def contacto(request):
    return render(request, 'usuario/contacto.html')



def login_view(request):
    return render(request, 'login.html')

     
def signout(request):
    logout(request)
    return redirect('inicio')

def lista_equipos(request):
    # Obtén todos los registros de la tabla 'equipos'
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
            try:
                form.save()
                return redirect('jugadores')
            except ValidationError as e:
                return render(request, 'administracion/crear_jugador.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administracion/crear_jugador.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
    

def editar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    
    if request.method == 'GET':
        form = CrearJugadorForm(instance=jugador)
        return render(request, 'administracion/editar_jugador.html', {'form': form, 'jugador': jugador})
    
    else:
        form = CrearJugadorForm(request.POST, request.FILES, instance=jugador)
        
        if form.is_valid():
            form.save() 
            return redirect('jugadores') 
        else:
            return render(request, 'administracion/editar_jugador.html', {
                'form': form,
                'jugador': jugador,
                'error': 'Por favor introduce datos válidos.'
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

def torneos_adm(request):
    torneos = Torneo.objects.all()
    return render(request, 'administracion/torneos_adm.html', {
        'torneos': torneos
    })

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
    form = TipoTorneoForm(request.POST)
    if form.is_valid():

        tipotorneo = TipoTorneo()
        tipotorneo.nombre_tipo_torneo = form.cleaned_data['nombre_tipo_torneo']
        tipotorneo.save()
        return redirect('tipotorneos_adm')
        
    else:
        return render(request, 'administracion/crear_tipotorneo.html', {'form': form})
    return render(request, 'administracion/crear_tipotorneo.html', {'form': form})

def edit_tipotorneo(request, id_tipo_torneo):
    tipotorneo = get_object_or_404(TipoTorneo, pk=id_tipo_torneo)

    if request.method == 'POST':
        form=TipoTorneoForm(request.POST)
        if form.is_valid():
            tipotorneo.nombre_tipo_torneo = form.cleaned_data['nombre_tipo_torneo']
            tipotorneo.save()
            return redirect('tipotorneos_adm')
    else:
        form = TipoTorneoForm(initial={'nombre_tipo_torneo': tipotorneo.nombre_tipo_torneo})
            
    return render(request, 'administracion/edit_tipotorneo.html', {
                 'tipotorneo': tipotorneo,
                 'form' : form
                })
        

def delete_tipotorneo(request, id_tipo_torneo):
    tipotorneo=get_object_or_404(TipoTorneo, pk=id_tipo_torneo)
    if request.method == 'POST':
        tipotorneo.delete()
        return redirect('tipotorneos_adm')
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
            try:
                form.save()
                return redirect('equipos')
            except ValidationError as e:
                return render(request, 'administracion/equipo_crear.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administracion/equipo_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
            
def equipo_editar(request, id_equipo):
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    
    if request.method == 'GET':
        form = CrearEquipoForm(instance=equipo)
        return render(request, 'administracion/equipo_editar.html' ,{'form': form, 'equipo': equipo})
    
    else:
        form = CrearEquipoForm(request.POST, request.FILES, instance=equipo)
        
        if form.is_valid():
            form.save() 
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
            try:
                form.save()
                return redirect('entrenadores')
            except ValidationError as e:
                return render(request, 'administracion/entrenador_crear.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administracion/entrenador_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })

def entrenador_editar(request, id_entrenador):
    entrenador = get_object_or_404(Entrenador, pk=id_entrenador)
    
    if request.method == 'GET':
        form = CrearEntrenadorForm(instance=entrenador)
        return render(request, 'administracion/entrenador_editar.html', {'form': form, 'entrenador': entrenador})
    
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES, instance=entrenador)
        
        if form.is_valid():
            form.save() 
            return redirect('entrenadores') 
        else:
            return render(request, 'administracion/entrenador_editar.html', {
                'form': form,
                'entrenador': entrenador,
                'error': 'Por favor introduce datos válidos.'
            })




