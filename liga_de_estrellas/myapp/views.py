from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from .models import Equipos

# Create your views here.
def home(request):
    return HttpResponse('La Mejor Liga del Condado')

def login(request):
    return render(request, 'login.html')

def exit(request):
    logout(request)
    return redirect('torneos')

def inicio(request):
    return render(request, 'inicio.html')

@login_required
def torneos(request):
    return render(request, 'torneos.html')

@login_required
def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')




def lista_equipos(request):
    # Obtén todos los registros de la tabla 'equipos'
    equipos = Equipos.objects.all()
    
    # Pasa los registros al contexto de la plantilla
    return render(request, 'equipos/lista_equipos.html', {'equipos': equipos})


