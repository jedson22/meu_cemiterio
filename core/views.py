from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.utils import timezone
from .models import Quadra, Lote, Gaveta, Falecido
from .forms import LoteForm, FalecidoForm  # Certifique-se que seus forms estão importados

def index(request):
    return render(request, 'core/index.html')

# --- Lógica de Lotes com Numeração Automática ---

def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = Lote.objects.filter(quadra=quadra).order_by('numero')
    return render(request, 'core/quadra.html', {'quadra': quadra, 'lotes': lotes})

def criar_lote(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    
    # Lógica para descobrir o próximo número automaticamente
    if request.method == 'GET':
        ultimo_numero = Lote.objects.filter(quadra=quadra).aggregate(Max('numero'))['numero__max']
        proximo_numero = 1 if ultimo_numero is None else ultimo_numero + 1
        
        # Preenche o formulário com o próximo número
        form = LoteForm(initial={'numero': proximo_numero, 'quadra': quadra})
        return render(request, 'core/form_lote.html', {'form': form, 'quadra': quadra, 'proximo_numero': proximo_numero})
    
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.quadra = quadra
            lote.save()
            return redirect('detalhe_quadra', quadra_id=quadra.id)
            
    return render(request, 'core/form_lote.html', {'form': form, 'quadra': quadra})

# --- Lógica de Exumação e Detalhes ---

def detalhe_lote(request, lote_id):
    lote = get_object_or_404(Lote, id=lote_id)
    gavetas = Gaveta.objects.filter(lote=lote).order_by('numero')
    
    # Separa quem está sepultado de quem foi exumado
    sepultados = Falecido.objects.filter(gaveta__lote=lote, situacao='sepultado')
    exumados = Falecido.objects.filter(gaveta__lote=lote, situacao='exumado').order_by('-data_exumacao')
    
    return render(request, 'core/lote.html', {
        'lote': lote,
        'gavetas': gavetas,
        'sepultados': sepultados,
        'exumados': exumados
    })

def adicionar_falecido(request, gaveta_id):
    gaveta = get_object_or_404(Gaveta, id=gaveta_id)
    if request.method == 'POST':
        form = FalecidoForm(request.POST)
        if form.is_valid():
            falecido = form.save(commit=False)
            falecido.gaveta = gaveta
            falecido.situacao = 'sepultado' # Padrão ao adicionar
            falecido.save()
            return redirect('detalhe_lote', lote_id=gaveta.lote.id)
    else:
        form = FalecidoForm()
    return render(request, 'core/form_falecido.html', {'form': form, 'gaveta': gaveta})

def exumar_falecido(request, falecido_id):
    falecido = get_object_or_404(Falecido, id=falecido_id)
    
    # Realiza a exumação
    falecido.situacao = 'exumado'
    falecido.data_exumacao = timezone.now().date()
    falecido.save()
    
    # Retorna para o lote
    return redirect('detalhe_lote', lote_id=falecido.gaveta.lote.id)
