from django.shortcuts import get_object_or_404, redirect
from .models import Lote


def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome_comprador = request.POST.get('nome_comprador')
        
        # Salva o nome no banco
        if nome_comprador:
            lote.proprietario = nome_comprador
            lote.save()
            
    # Retorna para a página anterior (ajuste 'detalhe_quadra' para o nome da sua url)
    return redirect(request.META.get('HTTP_REFERER', '/'))
