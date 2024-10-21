from django import forms
import os
from django.core.exceptions import ValidationError
from .models import Torneo, Temporada,Categoria,TipoTorneo, Jugador, Equipo, Entrenador




class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre_torneo', 'id_tipo_torneo', 'id_categoria', 'año']
        labels = {
            'nombre_torneo': 'Nombre del Torneo',
            'id_tipo_torneo': 'Tipo de Torneo',
            'id_categoria': 'Categoría',
            'año': 'Año',
        }

class TemporadasForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    fecha_final = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Temporada
        fields = ['nombre_temporada', 'id_torneo', 'fecha_inicio', 'fecha_final']
        labels = {
            'nombre_temporada': 'Nombre de la Temporada',
            'id_torneo': 'Nombre del Torneo',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_final': 'Fecha Final',
}


class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']

class TipoTorneoForm(forms.ModelForm):
    class Meta:
        model = TipoTorneo
        fields = ['nombre_tipo_torneo']


class CrearJugadorForm(forms.ModelForm):
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
        

class CrearEquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre_equipo', 'logo_equipo']
        
        
        def clean_logo_equipo(self):
            logo = self.cleaned_data.get('logo_equipo')

            if logo:
                if not logo.name.lower().endswith(('png', 'jpg', 'jpeg')):
                    raise ValidationError("Solo se permiten imágenes en formato PNG, JPEG o JPG.")
                    
            return logo
        

class CrearEntrenadorForm(forms.ModelForm):
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