import base64
import io
import matplotlib.pyplot as plt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout # <--- IMPORTANTE
from .models import Quadra, Lote, Gaveta

# --- SISTEMA PROTEGIDO COM @login_required ---

@login_required
def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    return render(request, 'index.html', {'quadras': quadras})

@login_required
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

@login_required
def detalhe_lote(request, q_id, l_id):
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    return render(request, 'detalhe_lote.html', {'lote': lote})

# --- AÇÕES DO SISTEMA ---

def encerrar_sessao(request):
    logout(request)
    return redirect('login') # Manda de volta para a tela de login

@login_required
def vender_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        nome = request.POST.get('nome_comprador')
        if nome:
            lote.proprietario = nome
            lote.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def transferir_lote(request, lote_id):
    if request.method == "POST":
        lote = get_object_or_404(Lote, id=lote_id)
        novo = request.POST.get('novo_titular')
        if novo:
            lote.proprietario = novo
            lote.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
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

@login_required
def limpar_gaveta(request, gaveta_id):
    gaveta = get_object_or_404(Gaveta, id=gaveta_id)
    
    # Se NÃO for admin, obedece a regra de data. Se for Admin, passa direto.
    if not request.user.is_superuser:
        pode, msg = gaveta.situacao_exumacao
        if not pode:
            return HttpResponse(f"ERRO: {msg}. Apenas Administradores podem desbloquear.")

    gaveta.nome = None
    gaveta.data = None
    gaveta.status = 'Livre'
    gaveta.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- ESTRUTURA (QUADRAS E LOTES) ---

@login_required
def adicionar_quadra(request):
    max_num = Quadra.objects.aggregate(Max('numero'))['numero__max']
    novo = 1 if max_num is None else max_num + 1
    Quadra.objects.create(numero=novo)
    return redirect('index')

@login_required
def excluir_quadra(request, quadra_id):
    if request.user.is_superuser: 
        get_object_or_404(Quadra, id=quadra_id).delete()
    return redirect('index')

@login_required
def adicionar_lote(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    max_num = quadra.lotes.aggregate(Max('numero'))['numero__max']
    novo = 1 if max_num is None else max_num + 1
    lote = Lote.objects.create(quadra=quadra, numero=novo)
    for i in range(1, 4): Gaveta.objects.create(lote=lote, numero=i)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def excluir_lote(request, lote_id):
    get_object_or_404(Lote, id=lote_id).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- PDF ---

@login_required
def gerar_relatorio(request):
    total_lotes = Lote.objects.count()
    lotes_vendidos = Lote.objects.filter(proprietario__isnull=False).count()
    lotes_livres = total_lotes - lotes_vendidos
    total_gavetas = Gaveta.objects.count()
    gavetas_ocupadas = Gaveta.objects.filter(status='Ocupado').count()
    
    plt.figure(figsize=(4,3))
    plt.pie([lotes_vendidos, lotes_livres], labels=['Vendidos', 'Livres'], autopct='%1.1f%%', colors=['#3498db', '#2ecc71'])
    plt.title('Ocupação')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'total_lotes': total_lotes, 'lotes_vendidos': lotes_vendidos, 'lotes_livres': lotes_livres,
        'total_gavetas': total_gavetas, 'gavetas_ocupadas': gavetas_ocupadas,
        'grafico': grafico_base64, 'quadras': Quadra.objects.all(),
    }
    template = get_template('relatorio.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err: return HttpResponse('Erro PDF')
    return response
