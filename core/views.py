from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max
from .models import Quadra, Lote, Gaveta

# --- VISUALIZAÇÃO ---

def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    return render(request, 'index.html', {'quadras': quadras})

def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

def detalhe_lote(request, q_id, l_id):
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    return render(request, 'detalhe_lote.html', {'lote': lote})

# --- AÇÕES OPERACIONAIS ---

def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome = request.POST.get('nome_comprador')
        if nome:
            lote.proprietario = nome
            lote.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def registrar_obito(request, gaveta_id):
    if request.method == "POST":
        gaveta = get_object_or_404(Gaveta, id=gaveta_id)
        nome = request.POST.get('nome_falecido')
        data = request.POST.get('data_obito')
        if nome and data:
            gaveta.nome = nome
            gaveta.data = data
            gaveta.status = 'Ocupado'
            gaveta.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def limpar_gaveta(request, gaveta_id):
    # Botão de emergência para apagar um falecido (exumação ou erro)
    gaveta = get_object_or_404(Gaveta, id=gaveta_id)
    gaveta.nome = None
    gaveta.data = None
    gaveta.status = 'Livre'
    gaveta.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- AÇÕES DE ESTRUTURA (GERENCIAMENTO) ---

def adicionar_quadra(request):
    # Descobre o último número e soma 1
    max_num = Quadra.objects.aggregate(Max('numero'))['numero__max']
    novo_numero = 1 if max_num is None else max_num + 1
    Quadra.objects.create(numero=novo_numero)
    return redirect('index')

def excluir_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    quadra.delete()
    return redirect('index')

def adicionar_lote(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    # Descobre o último lote DESTA quadra
    max_num = quadra.lotes.aggregate(Max('numero'))['numero__max']
    novo_numero = 1 if max_num is None else max_num + 1
    
    # Cria o lote
    novo_lote = Lote.objects.create(quadra=quadra, numero=novo_numero)
    
    # Cria automaticamente 3 gavetas para este lote
    Gaveta.objects.create(lote=novo_lote, numero=1)
    Gaveta.objects.create(lote=novo_lote, numero=2)
    Gaveta.objects.create(lote=novo_lote, numero=3)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def excluir_lote(request, lote_id):
    lote = get_object_or_404(Lote, id=lote_id)
    lote.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
