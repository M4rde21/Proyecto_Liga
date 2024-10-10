from django import forms
from .models import Torneo, Temporada,Categoria,TipoTorneo




class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre_torneo', 'id_categoria', 'id_tipo_torneo', 'año']

class TemporadasForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    fecha_final = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    class Meta:
        model = Temporada
        fields = ['nombre_temporada', 'id_torneo', 'fecha_inicio', 'fecha_final']


class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria']

class TipoTorneoForm(forms.ModelForm):
    class Meta:
        model = TipoTorneo
        fields = ['nombre_tipo_torneo']