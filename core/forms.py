from django import forms
from .models import Lote, Falecido

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['numero']

class FalecidoForm(forms.ModelForm):
    class Meta:
        model = Falecido
        fields = ['nome', 'data_nascimento', 'data_falecimento', 'observacao']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_falecimento': forms.DateInput(attrs={'type': 'date'}),
        }
