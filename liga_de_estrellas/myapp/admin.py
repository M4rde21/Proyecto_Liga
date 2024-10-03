from django.contrib import admin
from .models import Jugador, TipoTorneo, Categoria, Torneo

# Register your models here.
admin.site.register(Jugador)
admin.site.register(TipoTorneo)
admin.site.register(Categoria)
admin.site.register(Torneo)
