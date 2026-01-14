from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.utils import timezone
from .models import Quadra, Lote, Gaveta, Falecido, Produto, Historico
from .forms import LoteForm, FalecidoForm, ProdutoForm

# --- HOME E QUADRAS ---
def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    # Cria quadras automaticamente se não existirem (para o banco novo não ficar vazio)
    if not quadras:
        for i in range(1, 6): # Cria Quadras 1 a 5
            Quadra.objects.create(numero=i)
        quadras = Quadra.objects.all().order_by('numero')
    
    total_falecidos = Falecido.objects.count()
    produtos_baixo_estoque = Produto.objects.filter(quantidade__lte=5)
    
    return render(request, 'core/index.html', {
        'quadras': quadras, 
        'total_falecidos': total_falecidos,
        'alertas': produtos_baixo_estoque
    })

def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = Lote.objects.filter(quadra=quadra).order_by('numero')
    return render(request, 'core/quadra.html', {'quadra': quadra, 'lotes': lotes})

def criar_lote(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.quadra = quadra
            lote.save()
            # Cria 3 gavetas padrão para o lote
            for n in range(1, 4):
                Gaveta.objects.create(lote=lote, numero=n)
            return redirect('detalhe_quadra', quadra_id=quadra.id)
    
    # Numeração Automática
    ultimo_numero = Lote.objects.filter(quadra=quadra).aggregate(Max('numero'))['numero__max']
    proximo_numero = 1 if ultimo_numero is None else ultimo_numero + 1
    
    form = LoteForm(initial={'numero': proximo_numero})
    return render(request, 'core/form_lote.html', {'form': form, 'quadra': quadra, 'proximo_numero': proximo_numero})

# --- GAVETAS E FALECIDOS ---
def detalhe_lote(request, lote_id):
    lote = get_object_or_404(Lote, id=lote_id)
    gavetas = Gaveta.objects.filter(lote=lote).order_by('numero')
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
            falecido.situacao = 'sepultado'
            falecido.save()
            # Registra no histórico
            Historico.objects.create(acao=f"Sepultamento: {falecido.nome} na Gaveta {gaveta.numero}, Lote {gaveta.lote.numero}")
            return redirect('detalhe_lote', lote_id=gaveta.lote.id)
    else:
        form = FalecidoForm()
    return render(request, 'core/form_falecido.html', {'form': form, 'gaveta': gaveta})

def exumar_falecido(request, falecido_id):
    falecido = get_object_or_404(Falecido, id=falecido_id)
    falecido.situacao = 'exumado'
    falecido.data_exumacao = timezone.now().date()
    falecido.save()
    Historico.objects.create(acao=f"Exumação: {falecido.nome} do Lote {falecido.gaveta.lote.numero}")
    return redirect('detalhe_lote', lote_id=falecido.gaveta.lote.id)

# --- CONTROLE DE ESTOQUE ---
def lista_estoque(request):
    produtos = Produto.objects.all().order_by('nome')
    return render(request, 'estoque.html', {'produtos': produtos})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            Historico.objects.create(acao=f"Novo Produto: {produto.nome} adicionado ao estoque.")
            return redirect('lista_estoque')
    else:
        form = ProdutoForm()
    return render(request, 'core/form_produto.html', {'form': form})
