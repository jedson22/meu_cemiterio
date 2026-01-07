import os
from django.http import HttpResponse
from django.conf import settings

def index(request):
    # Isso vai listar todos os arquivos do projeto na tela
    output = []
    output.append(f"PASTA BASE DO PROJETO: {settings.BASE_DIR}")
    output.append("--- LISTA DE ARQUIVOS ENCONTRADOS ---")
    
    # Caminha por todas as pastas
    for root, dirs, files in os.walk(settings.BASE_DIR):
        for file in files:
            caminho_completo = os.path.join(root, file)
            # Mostra apenas arquivos html ou py para não poluir
            if ".html" in file or ".py" in file:
                output.append(caminho_completo)
                
    return HttpResponse("<br>".join(output))

# Mantive as outras funções vazias só pro site não quebrar na inicialização
def detalhe_quadra(request, quadra_id): return HttpResponse("Modo Diagnóstico")
def detalhe_lote(request, q_id, l_id): return HttpResponse("Modo Diagnóstico")
def vender_lote(request, lote_id): return HttpResponse("Modo Diagnóstico")
