from django import forms
from .models import Torneos, Temporadas




class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneos
        fields = ['nombre_torneo', 'id_categoria', 'id_tipo_torneo', 'año']

class TemporadasForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    fecha_final = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    class Meta:
        model = Temporadas
        fields = ['nombre_temporada', 'id_torneo', 'fecha_inicio', 'fecha_final']