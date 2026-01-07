from django.shortcuts import render, get_object_or_404, redirect
from .models import Quadra, Lote

# 1. PÁGINA INICIAL (Mapa Geral)
def index(request):
    # Busca todas as quadras e ordena pelo número
    quadras = Quadra.objects.all().order_by('numero')
    return render(request, 'index.html', {'quadras': quadras})

# 2. DETALHES DA QUADRA (Opcional)
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

# 3. DETALHES DO LOTE (Ver Gavetas)
def detalhe_lote(request, q_id, l_id):
    # Busca o lote pelo número da quadra e número do lote
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
            
    # Retorna para a página anterior (recarrega o mapa)
    return redirect(request.META.get('HTTP_REFERER', '/'))
