from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from .forms import CrearJugadorForm, CrearEquipoForm, CrearEntrenadorForm
from .models import Jugador, Equipo, Entrenador
# Create your views here.
def inicio(request):
    return render(request, 'usuario/inicio.html')

def login(request):
    return render(request, 'login.html')

def resumen(request):
    return render(request, 'administration/resumen.html')

def lista_jugadores(request):
    jugadores = Jugador.objects.all()
    return render(request, 'administration/jugadores.html', {'jugadores': jugadores})

def crear_jugador(request):
    if request.method == 'GET':
        return render(request, 'administration/crear_jugador.html', {
            'form': CrearJugadorForm()
        })
    else:
        form = CrearJugadorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('jugadores')
            except ValidationError as e:
                return render(request, 'administration/crear_jugador.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administration/crear_jugador.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
    

def editar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    
    if request.method == 'GET':
        form = CrearJugadorForm(instance=jugador)
        return render(request, 'administration/editar_jugador.html', {'form': form, 'jugador': jugador})
    
    else:
        form = CrearJugadorForm(request.POST, request.FILES, instance=jugador)
        
        if form.is_valid():
            form.save() 
            return redirect('jugadores') 
        else:
            return render(request, 'administration/editar_jugador.html', {
                'form': form,
                'jugador': jugador,
                'error': 'Por favor introduce datos válidos.'
            })


def eliminar_jugador(request, id_jugador):
    jugador = get_object_or_404(Jugador, pk=id_jugador)
    if request.method == 'POST':
        jugador.delete()
        return redirect('jugadores')
        

def equipos_lista(request):
    equipos = Equipo.objects.all()
    return render(request, 'administration/equipos.html', {'equipos': equipos})

def equipo_crear(request):
    if request.method == 'GET':
        return render(request, 'administration/equipo_crear.html', {
            'form': CrearEquipoForm
        })
    else:
        form = CrearEquipoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('equipos')
            except ValidationError as e:
                return render(request, 'administration/equipo_crear.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administration/equipo_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })
            
def equipo_editar(request, id_equipo):
    equipo = get_object_or_404(Equipo, pk=id_equipo)
    
    if request.method == 'GET':
        form = CrearEquipoForm(instance=equipo)
        return render(request, 'administration/equipo_editar.html' ,{'form': form, 'equipo': equipo})
    
    else:
        form = CrearEquipoForm(request.POST, request.FILES, instance=equipo)
        
        if form.is_valid():
            form.save() 
            return redirect('equipos') 
        else:
            return render(request, 'administration/equipo_editar.html', {
                'form': form,
                'equipo': equipo,
                'error': 'Por favor introduce datos válidos.'
            })

def entrenadores_lista(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'administration/entrenadores.html', {'entrenadores': entrenadores})

def entrenador_crear(request):
    if request.method == 'GET':
        return render(request, 'administration/entrenador_crear.html', {
            'form': CrearEntrenadorForm
        })
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('entrenadores')
            except ValidationError as e:
                return render(request, 'administration/entrenador_crear.html', {
                    'form': form,
                    'error': f'Error en los datos: {e}'
                })
        else:
            return render(request, 'administration/entrenador_crear.html', {
                'form': form,
                'error': 'Por favor introduce datos válidos.'
            })

def entrenador_editar(request, id_entrenador):
    entrenador = get_object_or_404(Entrenador, pk=id_entrenador)
    
    if request.method == 'GET':
        form = CrearEntrenadorForm(instance=entrenador)
        return render(request, 'administration/entrenador_editar.html', {'form': form, 'entrenador': entrenador})
    
    else:
        form = CrearEntrenadorForm(request.POST, request.FILES, instance=entrenador)
        
        if form.is_valid():
            form.save() 
            return redirect('entrenadores') 
        else:
            return render(request, 'administration/entrenador_editar.html', {
                'form': form,
                'entrenador': entrenador,
                'error': 'Por favor introduce datos válidos.'
            })

def exit(request):
    logout(request)
    return redirect('inicio')

def torneos(request):
    return render(request, 'usuario/torneos.html')

def reglamentos(request):
    return render(request, 'usuario/reglamentos.html')

def contacto(request):
    return render(request, 'usuario/contacto.html')
