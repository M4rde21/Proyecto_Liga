from django import forms
from django.core.exceptions import ValidationError
import os
from django.forms import ModelForm
from .models import Jugador, Equipo, Entrenador

class CrearJugadorForm(ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre_jugador', 'apellido_jugador', 'dni_jugador', 'fecha_nac_jugador', 'foto_jugador', 'activo_jugador']
        widgets = {
            'fecha_nac_jugador': forms.DateInput(attrs={'type': 'date'}),
        }
        
        def clean_foto_jugador(self):
            foto = self.cleaned_data.get('foto_jugador')

            if foto:
                ext = os.path.splitext(foto.name)[1].lower()
                if ext not in ['.png', '.jpg', '.jpeg']:
                    raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

            return foto
        
        
class CrearEquipoForm(ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre_equipo', 'logo_equipo']
        
        
        def clean_logo_equipo(self):
            logo = self.cleaned_data.get('logo_equipo')

            if logo:
                if not logo.name.lower().endswith(('png', 'jpg', 'jpeg')):
                    raise ValidationError("Solo se permiten imágenes en formato PNG, JPEG o JPG.")
                    
            return logo


class CrearEntrenadorForm(ModelForm):
    class Meta:
        model = Entrenador
        fields = ['nombre_entrenador', 'apellido_entrenador', 'dni_entrenador', 'fecha_nac_entrenador', 'foto_entrenador']
        widgets = {
            'fecha_nac_entrenador': forms.DateInput(attrs={'type': 'date'}),
            }
        
    def clean_foto_entrenador(self):
        foto = self.cleaned_data.get('foto_entrenador')

        if foto:
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

        return foto