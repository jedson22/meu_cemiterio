from django.shortcuts import render, get_object_or_404, redirect
from .models import Quadra, Lote, Gaveta

# 1. PÁGINA INICIAL
def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    return render(request, 'index.html', {'quadras': quadras})

# 2. DETALHES DA QUADRA
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

# 3. DETALHES DO LOTE (Onde aparecem as gavetas)
def detalhe_lote(request, q_id, l_id):
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    return render(request, 'detalhe_lote.html', {'lote': lote})

# 4. FUNÇÃO: VENDER LOTE
def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome = request.POST.get('nome_comprador')
        
        if nome:
            lote.proprietario = nome
            lote.save()
            
    return redirect(request.META.get('HTTP_REFERER', '/'))

# 5. NOVA FUNÇÃO: REGISTRAR ÓBITO NA GAVETA
def registrar_obito(request, gaveta_id):
    if request.method == "POST":
        gaveta = get_object_or_404(Gaveta, id=gaveta_id)
        
        nome_falecido = request.POST.get('nome_falecido')
        data_obito = request.POST.get('data_obito')
        
        if nome_falecido and data_obito:
            gaveta.nome = nome_falecido
            gaveta.data = data_obito
            gaveta.status = 'Ocupado'  # Muda o status automaticamente
            gaveta.save()
            
    return redirect(request.META.get('HTTP_REFERER', '/'))
