from django import forms
from .models import Torneo, Temporada,Categoria,TipoTorneo, Jugador, Equipo, Entrenador
from django.core.exceptions import ValidationError
import os
from django.forms import ModelForm




class TorneoForm(forms.Form):
    nombre_torneo = forms.CharField(label="Nombre del torneo", max_length=100, required=True)
    id_categoria = forms.ModelChoiceField(label="Categoria", queryset=Categoria.objects.all())
    id_tipo_torneo = forms.ModelChoiceField(label="Tipo de Torneo", queryset=TipoTorneo.objects.all())
    año = forms.IntegerField(label="Año", required=True, min_value=1900, max_value=2100)

class TemporadasForm(forms.Form):
    nombre_temporada = forms.CharField(label="Nombre de la Temporada", max_length=100, required=True)
    id_torneo = forms.ModelChoiceField(label="Torneo", queryset=Torneo.objects.all())
    fecha_inicio = forms.DateField(
        label="Fecha de Inicio", widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], required=True
    )
    fecha_final = forms.DateField(
        label="Fecha Final", widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], required=True
    )
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_final = cleaned_data.get("fecha_final")

        if fecha_inicio and fecha_final and fecha_final <= fecha_inicio:
            self.add_error('fecha_final', "La fecha final debe ser posterior a la fecha de inicio.")


class CategoriasForm(forms.Form):
    nombre_categoria = forms.CharField(label="Nombre de la Categoria: ", max_length=100, required=True)

class TipoTorneoForm(forms.Form):
   nombre_tipo_torneo = forms.CharField(label='Tipo de Torneo', max_length=100, required=True)


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
