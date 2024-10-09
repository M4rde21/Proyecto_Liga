from django import forms
from .models import Torneos, Temporadas,Categorias,TipoTorneos




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
        labels = {
            'nombre_temporada': 'Nombre de la Temporada',
            'id_torneo': 'Torneo',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_final': 'Fecha Final',
}


class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre_categoria']

class TipoTorneoForm(forms.ModelForm):
    class Meta:
        model = TipoTorneos
        fields = ['nombre_tipo_torneo']