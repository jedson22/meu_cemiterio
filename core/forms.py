from django import forms
from .models import Lote, Falecido, Produto

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['numero']

class FalecidoForm(forms.ModelForm):
    class Meta:
        model = Falecido
        fields = ['nome', 'data_nascimento', 'data_falecimento', 'observacao']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_falecimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'quantidade', 'preco', 'descricao']
