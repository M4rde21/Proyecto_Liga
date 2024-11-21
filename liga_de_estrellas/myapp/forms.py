from django import forms
from .models import Torneo, Temporada,Categoria,TipoTorneo, Jugador, Equipo, Entrenador, PremiosGrupal, Grupo, Fecha, Predio,Partido,Planilla,Resultado
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


class TipoTorneoForm(forms.ModelForm):
    class Meta:
        model = TipoTorneo
        fields = ['nombre_tipo_torneo']


class CrearJugadorForm(forms.Form):
    nombre_jugador = forms.CharField(label="Nombres", max_length=100)
    apellido_jugador = forms.CharField(label="Apellidos", max_length=100)
    dni_jugador = forms.CharField(label="Número de DNI", max_length=20, min_length=8)
    fecha_nac_jugador = forms.DateField(label="Fecha de Nacimiento", widget=forms.DateInput(attrs={'type': 'date'}))
    foto_jugador = forms.ImageField(label="Foto del Jugador/a", required=False)
    activo_jugador = forms.BooleanField(label="Activo/a", initial=True, required=False)

    def clean_foto_jugador(self):
        foto = self.cleaned_data.get('foto_jugador')

        if foto:
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

        return foto
        
        
class CrearEquipoForm(forms.Form):
    nombre_equipo = forms.CharField(label="Nombre", max_length=100)
    logo_equipo = forms.ImageField(label="Logo del Equipo", required=False)
        
        
    def clean_logo_equipo(self):
        logo = self.cleaned_data.get('logo_equipo')

        if logo:
            if not logo.name.lower().endswith(('png', 'jpg', 'jpeg')):
                raise ValidationError("Solo se permiten imágenes en formato PNG, JPEG o JPG.")
                    
        return logo


class CrearEntrenadorForm(forms.Form):
    nombre_entrenador = forms.CharField(label="Nombres", max_length=100)
    apellido_entrenador = forms.CharField(label="Apellidos", max_length=100)
    dni_entrenador = forms.CharField(label="Numero de DNI", max_length=20, min_length=8)
    fecha_nac_entrenador = forms.DateField(label="Fecha de Nacimiento", widget=forms.DateInput(attrs={'type': 'date'}))
    foto_entrenador = forms.ImageField(label="Foto del Delegado/a", required=False)
    
    def clean_foto_entrenador(self):
        foto = self.cleaned_data.get('foto_entrenador')

        if foto:
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

        return foto

class CrearPremioGrupalForm(forms.Form):
    nombre_premio_grupal = forms.CharField(label="Nombre del Premio Grupal", max_length=100, required=True)
    foto_premio_grupal = forms.ImageField(label="Foto del Premio", required=False)
    
    def clean_foto_premio_grupal(self):
        foto = self.cleaned_data.get('foto_premio_grupal')

        if foto:
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

        return foto
    
class CrearPremioIndividualForm(forms.Form):
    nombre_premio_individual = forms.CharField(label="Nombre del Premio Individual", max_length=100, required=True)
    foto_premio_individual = forms.ImageField(label="Foto del Premio", required=False)
    
    def clean_foto_premio_individual(self):
        foto = self.cleaned_data.get('foto_premio_individual')

        if foto:
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.png', '.jpg', '.jpeg']:
                raise ValidationError('Solo se permiten archivos con extensión .png, .jpg o .jpeg.')

        return foto
    

class CrearFechaForm(forms.Form):
    nombre_fecha = forms.CharField(label="Nombre de la fecha", max_length=100, required=True)
  

class CrearZonaForm(forms.Form):
    nombre_grupo = forms.CharField(label="Nombre de la Zona", max_length=100)


class CrearPartidoForm(forms.Form):

    id_equipo_1 = forms.ModelChoiceField(label="Equipo 1", queryset=Equipo.objects.all())
    id_equipo_2 = forms.ModelChoiceField(label="Equipo 2", queryset=Equipo.objects.all())
    id_predio = forms.ModelChoiceField(label="Predio", queryset=Predio.objects.all())
    id_grupo = forms.ModelChoiceField(label="Grupo", queryset=Grupo.objects.all())
    fecha_partido = forms.DateField(
        label="Fecha", widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'], required=True
    )
    hora_partido = forms.TimeField(
        label="Hora del Partido", 
        widget=forms.TimeInput(attrs={'type': 'time', 'pattern': '[0-9]{2}:[0-9]{2}', 'title': 'Use format HH:MM'}),
        input_formats=['%H:%M']
    )
    destacado = forms.BooleanField(label="Partido Destacado", required=False)


class ResultadoForm(forms.Form):
    goles_equipo_1 = forms.IntegerField(
        label="Goles del equipo 1", 
        min_value=0, 
        initial=0, 
        required=False
    )
    goles_equipo_2 = forms.IntegerField(
        label="Goles del equipo 2", 
        min_value=0, 
        initial=0, 
        required=False
    )
    penales = forms.BooleanField(
        label="Penales", 
        required=False
    )
    penales_equipo_1 = forms.IntegerField(
        label="Goles por penales del equipo 1", 
        min_value=0, 
        initial=0, 
        required=False
    )
    penales_equipo_2 = forms.IntegerField(
        label="Goles por penales del equipo 2", 
        min_value=0, 
        initial=0, 
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        penales = cleaned_data.get('penales')
        penales_equipo_1 = cleaned_data.get('penales_equipo_1', 0)
        penales_equipo_2 = cleaned_data.get('penales_equipo_2', 0)

        # Validar si se ingresaron goles por penales cuando 'Penales' no está seleccionado
        if not penales and (penales_equipo_1 or penales_equipo_2):
            raise forms.ValidationError(
                "Si 'Penales' no está marcado, los goles por penales deben estar vacíos o en cero."
            )

        # Validar que ambos goles por penales estén presentes si 'Penales' está marcado
        if penales:
            if penales_equipo_1 is None or penales_equipo_2 is None:
                raise forms.ValidationError(
                    "Debe ingresar los goles por penales de ambos equipos si se selecciona 'Penales'."
                )
        else:
            # Si no hay penales, asegúrate de que los valores sean 0
            cleaned_data['penales_equipo_1'] = 0
            cleaned_data['penales_equipo_2'] = 0

        return cleaned_data

    

    
    

class PlanillaForm(forms.Form):
    goles = forms.IntegerField(label="Goles", min_value=0,initial=0, required=False)
    num_camiseta = forms.IntegerField(label="Nro de camiseta", min_value=1, required=False)
    participo = forms.BooleanField(label="Jugó", required=False)
    tarjeta_amarilla = forms.BooleanField(label="TA", required=False)
    tarjeta_roja = forms.BooleanField(label="TR", required=False)
    figura = forms.BooleanField(label="Figura del partido", required=False)

    def clean(self):
        cleaned_data = super().clean()
        participo = cleaned_data.get("participo")
        goles = cleaned_data.get("goles")
        num_camiseta = cleaned_data.get("num_camiseta")

        if not participo:
            cleaned_data["goles"] = 0
            cleaned_data["tarjeta_amarilla"] = False
            cleaned_data["tarjeta_roja"] = False
            cleaned_data["figura"] = False
        elif participo and (goles is None or num_camiseta is None):
            raise forms.ValidationError("Cuando un jugador participa, los campos de goles y número de camiseta son obligatorios.")
        
        return cleaned_data
    

