from django.shortcuts import render, get_object_or_404, redirect
from .models import Quadra, Lote

# --- PÁGINA INICIAL (INDEX) ---
def index(request):
    # Pega todas as quadras para mostrar na tela inicial
    quadras = Quadra.objects.all().order_by('numero')
    
    # Se você quiser mostrar os lotes direto na home, pode passar eles também
    # Mas geralmente a home mostra as quadras
    return render(request, 'index.html', {'quadras': quadras})

# --- PÁGINA DE DETALHES DA QUADRA (Se você tiver) ---
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

# --- FUNÇÃO DE VENDER O LOTE ---
def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome_comprador = request.POST.get('nome_comprador')
        
        # Salva o nome no banco se foi digitado algo
        if nome_comprador:
            lote.proprietario = nome_comprador
            lote.save()
            
    # Redireciona de volta para a página de onde você veio
    return redirect(request.META.get('HTTP_REFERER', '/'))
