from django.contrib import admin
from .models import Equipos,Categorias,TipoTorneos

# Register your models here.
admin.site.register(Equipos)
admin.site.register(Categorias)
admin.site.register(TipoTorneos)