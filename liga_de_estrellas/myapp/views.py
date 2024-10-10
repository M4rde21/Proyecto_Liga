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
    if request.method == 'POST':
        form = TorneoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('torneos_adm')  
    else:
        form = TorneoForm()
    return render(request, 'administracion/crear_torneo.html', {'form': form})

def torneos_adm(request):
    torneos = Torneo.objects.all()
    return render(request, 'administracion/torneos_adm.html', {
        'torneos': torneos
    })

def edit_torneo(request, id_torneo):
    if request.method == 'GET':
        torneo = get_object_or_404(Torneo, pk=id_torneo)
        form=TorneoForm(instance=torneo)
        return render(request, 'administracion/edit_torneo.html', {
        'torneo': torneo,
        'form' : form
        })
    else:
        try:
            torneo=get_object_or_404(Torneo, pk=id_torneo)
            form=TorneoForm(request.POST, instance=torneo)
            form.save()
            return redirect('torneos_adm')
        except ValueError:
            return render(request, 'administracion/torneos_adm.html', {
                'torneo': torneo,
                'form' : form,
                'error' : "Error al actualizar datos"
            })
        
def delete_torneo(request, id_torneo):
    torneo=get_object_or_404(Torneo, pk=id_torneo)
    if request.method == 'POST':
        torneo.delete()
        return redirect('torneos_adm')
    

def crear_temporada(request):
    if request.method == 'POST':
        form = TemporadasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('temporadas_adm')  # Cambia esto por la vista a la que quieres redirigir después de guardar
    else:
        form = TemporadasForm()
    
    return render(request, 'administracion/crear_temporada.html', {'form': form})
    

def temporadas_adm(request):
    temporadas = Temporada.objects.all()
    return render(request, 'administracion/temporadas_adm.html', {
        'temporadas': temporadas
    })
def edit_temporada(request, id_temporada):
    if request.method == 'GET':
        temporada = get_object_or_404(Temporada, pk=id_temporada)
        form=TemporadasForm(instance=temporada)
        return render(request, 'administracion/edit_temporada.html', {
        'temporada': temporada,
        'form' : form
        })
    else:
        try:
            temporada=get_object_or_404(Temporada, pk=id_temporada)
            form=TemporadasForm(request.POST, instance=temporada)
            form.save()
            return redirect('temporadas_adm')
        except ValueError:
            return render(request, 'administracion/temporadas_adm.html', {
            'temporada': temporada,
            'form' : form,
            'error' : "Error al actualizar datos"
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
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias_adm')  
    else:
        form = CategoriasForm()
    return render(request, 'administracion/crear_categoria.html', {'form': form})

def edit_categoria(request, id_categoria):
    if request.method == 'GET':
        categoria = get_object_or_404(Categoria, pk=id_categoria)
        form=CategoriasForm(instance=categoria)
        return render(request, 'administracion/edit_categoria.html', {
        'categoria': categoria,
        'form' : form
        })
    else:
        try:
            categoria=get_object_or_404(Categoria, pk=id_categoria)
            form=CategoriasForm(request.POST, instance=categoria)
            form.save()
            return redirect('categorias_adm')
        except ValueError:
            return render(request, 'administracion/categorias_adm.html', {
                'categoria': categoria,
                'form' : form,
                'error' : "Error al actualizar datos"
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




