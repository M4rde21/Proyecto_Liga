from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Equipos, Torneos, Temporadas, Categorias,TipoTorneos
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TorneoForm, TemporadasForm, CategoriasForm,TipoTorneoForm
from django.views import View


# Create your views here.
def home(request):
    return HttpResponse('La Mejor Liga del Condado')

def inicio(request):
    return render(request, 'inicio.html')

def torneos(request):
    torneos = Torneos.objects.all()
    return render(request, 'torneos.html', {'torneos': torneos})

def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def usuario(request):
    if request.method == 'GET':
        return render(request, 'inicio.html', {
        'form' : UserCreationForm,
        'error' : 'ya existe el ususario capo'
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                
                #register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('menu_adm')
            except IntegrityError:
                return render(request, 'inicio.html', {
                    'form' : UserCreationForm,
                    'error' : 'ya existe el ususario capo'
                })
        return render(request, 'inicio.html', {
                    'form' : UserCreationForm,
                    'error' : 'contraseña equivocada capo'
                })



def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form' : AuthenticationForm
        } )
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
            'form' : AuthenticationForm,
            'error' : 'unsername or password is incorret capo. aguante boca adema'
            } )
        else:
            login(request, user)
            return redirect('crear_torneo')
        
def signout(request):
    logout(request)
    return redirect('inicio')

def lista_equipos(request):
    # Obtén todos los registros de la tabla 'equipos'
    equipos = Equipos.objects.all()
    
    # Pasa los registros al contexto de la plantilla
    return render(request, 'equipos/lista_equipos.html', {'equipos': equipos})


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
    torneos = Torneos.objects.all()
    return render(request, 'administracion/torneos_adm.html', {
        'torneos': torneos
    })

def edit_torneo(request, id_torneo):
    if request.method == 'GET':
        torneo = get_object_or_404(Torneos, pk=id_torneo)
        form=TorneoForm(instance=torneo)
        return render(request, 'administracion/edit_torneo.html', {
        'torneo': torneo,
        'form' : form
        })
    else:
        try:
            torneo=get_object_or_404(Torneos, pk=id_torneo)
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
    torneo=get_object_or_404(Torneos, pk=id_torneo)
    if request.method == 'POST':
        torneo.delete()
        return redirect('torneos_adm')
    

def crear_temporada(request):
    if request.method == 'POST':
        form = TemporadasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('torneos_adm')  # Cambia esto por la vista a la que quieres redirigir después de guardar
    else:
        form = TemporadasForm()
    
    return render(request, 'administracion/crear_temporada.html', {'form': form})
    

def temporadas_adm(request):
    temporadas = Temporadas.objects.all()
    return render(request, 'administracion/temporadas_adm.html', {
        'temporadas': temporadas
    })
def edit_temporada(request, id_temporada):
    if request.method == 'GET':
        temporada = get_object_or_404(Temporadas, pk=id_temporada)
        form=TemporadasForm(instance=temporada)
        return render(request, 'administracion/edit_temporada.html', {
        'temporada': temporada,
        'form' : form
        })
    else:
        try:
            temporada=get_object_or_404(Temporadas, pk=id_temporada)
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
    temporada=get_object_or_404(Temporadas, pk=id_temporada)
    if request.method == 'POST':
        temporada.delete()
        return redirect('temporadas_adm')
    
def categorias_adm(request):
    categorias = Categorias.objects.all()
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
        categoria = get_object_or_404(Categorias, pk=id_categoria)
        form=CategoriasForm(instance=categoria)
        return render(request, 'administracion/edit_categoria.html', {
        'categoria': categoria,
        'form' : form
        })
    else:
        try:
            categoria=get_object_or_404(Categorias, pk=id_categoria)
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
    categoria=get_object_or_404(Categorias, pk=id_categoria)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias_adm')
    

def tipotorneos_adm(request):
    tipotorneos = TipoTorneos.objects.all()
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
        tipotorneo = get_object_or_404(TipoTorneos, pk=id_tipo_torneo)
        form=TipoTorneoForm(instance=tipotorneo)
        return render(request, 'administracion/edit_tipotorneo.html', {
        'tipotorneo': tipotorneo,
        'form' : form
        })
    else:
        try:
            tipotorneo=get_object_or_404(TipoTorneos, pk=id_tipo_torneo)
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
    tipotorneo=get_object_or_404(TipoTorneos, pk=id_tipo_torneo)
    if request.method == 'POST':
        tipotorneo.delete()
        return redirect('tipotorneos_adm')