from django.contrib import admin
from .models import Equipo,Categoria,TipoTorneo

# Register your models here.
admin.site.register(Equipo)
admin.site.register(Categoria)
admin.site.register(TipoTorneo)