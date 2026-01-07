from django.shortcuts import render, get_object_or_404, redirect
from .models import Quadra, Lote

# 1. PÁGINA INICIAL
def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    return render(request, 'index.html', {'quadras': quadras})

# 2. DETALHES DA QUADRA (Lista os lotes)
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

# 3. DETALHES DO LOTE (A função que faltava!)
def detalhe_lote(request, q_id, l_id):
    # Pega o lote específico usando o ID da quadra e do lote
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    return render(request, 'detalhe_lote.html', {'lote': lote})

# 4. FUNÇÃO DE VENDER
def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome = request.POST.get('nome_comprador')
        if nome:
            lote.proprietario = nome
            lote.save()
    # Volta para a tela anterior
    return redirect(request.META.get('HTTP_REFERER', '/'))
