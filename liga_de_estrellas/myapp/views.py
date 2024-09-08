from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Equipos

# Create your views here.
def home(request):
    return HttpResponse('La Mejor Liga del Condado')

def inicio(request):
    return render(request, 'inicio.html')

def torneos(request):
    return render(request, 'torneos.html')

def reglamentos(request):
    return render(request, 'reglamentos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')


def lista_equipos(request):
    # Obtén todos los registros de la tabla 'equipos'
    equipos = Equipos.objects.all()
    
    # Pasa los registros al contexto de la plantilla
    return render(request, 'equipos/lista_equipos.html', {'equipos': equipos})


