from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import IntegrityError
from .models import Quadra, Lote, Gaveta, Produto, Historico

# --- SISTEMA ---

@login_required
def index(request):
    # Carregamento otimizado (não trava o servidor)
    quadras = Quadra.objects.prefetch_related('lotes__gavetas').all().order_by('numero')
    
    # Verifica tabela de produtos (se existir)
    try:
        produtos_baixo = Produto.objects.filter(quantidade__lte=5).count()
    except:
        produtos_baixo = 0
        
    return render(request, 'index.html', {'quadras': quadras, 'alerta_estoque': produtos_baixo})

def encerrar_sessao(request):
    logout(request)
    return redirect('login')

# --- VISUALIZAÇÃO ---

@login_required
def detalhe_quadra(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    lotes = quadra.lotes.prefetch_related('gavetas').all().order_by('numero')
    return render(request, 'quadra.html', {'quadra': quadra, 'lotes': lotes})

@login_required
def detalhe_lote(request, q_id, l_id):
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    return render(request, 'detalhe_lote.html', {'lote': lote})

# --- AÇÕES OPERACIONAIS ---

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
    
    # Validação de Admin/Data
    if not request.user.is_superuser:
        pode, msg = gaveta.situacao_exumacao
        if not pode:
            return HttpResponse(f"ERRO: {msg}. Apenas Administradores.")
    
    # SALVA NO HISTÓRICO ANTES DE LIMPAR
    if gaveta.nome:
        Historico.objects.create(
            gaveta=gaveta,
            nome=gaveta.nome,
            data_falecimento=gaveta.data,
            observacao="Exumação realizada pelo sistema"
        )

    gaveta.nome = None
    gaveta.data = None
    gaveta.status = 'Livre'
    gaveta.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def adicionar_historico_manual(request, gaveta_id):
    if request.method == "POST":
        gaveta = get_object_or_404(Gaveta, id=gaveta_id)
        nome = request.POST.get('nome_antigo')
        data_f = request.POST.get('data_falecimento')
        
        if nome:
            Historico.objects.create(
                gaveta=gaveta,
                nome=nome,
                data_falecimento=data_f if data_f else None,
                observacao="Registro adicionado manualmente"
            )
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- ESTRUTURA ---

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
def form_adicionar_lote(request, quadra_id):
    quadra = get_object_or_404(Quadra, id=quadra_id)
    return render(request, 'adicionar_lote.html', {'quadra': quadra})

@login_required
def salvar_lote(request, quadra_id):
    if request.method == "POST":
        quadra = get_object_or_404(Quadra, id=quadra_id)
        numero_escolhido = request.POST.get('numero_lote')
        
        try:
            lote = Lote.objects.create(quadra=quadra, numero=numero_escolhido)
            for i in range(1, 4): Gaveta.objects.create(lote=lote, numero=i)
        except IntegrityError:
            return HttpResponse("Erro: Já existe um lote com esse número nesta quadra.")
            
    return redirect('index')

@login_required
def excluir_lote(request, lote_id):
    get_object_or_404(Lote, id=lote_id).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

# --- ESTOQUE ---

@login_required
def lista_estoque(request):
    produtos = Produto.objects.all().order_by('nome')
    return render(request, 'estoque.html', {'produtos': produtos})

@login_required
def adicionar_produto(request):
    if request.method == "POST":
        Produto.objects.create(
            nome=request.POST.get('nome'),
            categoria=request.POST.get('categoria'),
            quantidade=request.POST.get('quantidade')
        )
    return redirect('lista_estoque')

@login_required
def atualizar_estoque(request, produto_id):
    if request.method == "POST":
        p = get_object_or_404(Produto, id=produto_id)
        p.quantidade = request.POST.get('nova_quantidade')
        p.save()
    return redirect('lista_estoque')

@login_required
def excluir_produto(request, produto_id):
    if request.user.is_superuser:
        get_object_or_404(Produto, id=produto_id).delete()
    return redirect('lista_estoque')

# --- PDF (IMPORTAÇÃO TARDIA PARA ECONOMIZAR MEMÓRIA) ---

@login_required
def gerar_relatorio(request):
    # IMPORTANTE: Só importa essas bibliotecas pesadas aqui dentro
    import io
    import base64
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from xhtml2pdf import pisa

    total_lotes = Lote.objects.count()
    lotes_vendidos = Lote.objects.filter(proprietario__isnull=False).count()
    lotes_livres = total_lotes - lotes_vendidos
    total_gavetas = Gaveta.objects.count()
    gavetas_ocupadas = Gaveta.objects.filter(status='Ocupado').count()
    
    plt.figure(figsize=(4,3))
    if total_lotes > 0:
        plt.pie([lotes_vendidos, lotes_livres], labels=['Vendidos', 'Livres'], autopct='%1.1f%%', colors=['#3498db', '#2ecc71'])
        plt.title('Ocupação')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close() # Limpa a memória
    buffer.seek(0)
    grafico = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'total_lotes': total_lotes, 'lotes_vendidos': lotes_vendidos, 'lotes_livres': lotes_livres,
        'total_gavetas': total_gavetas, 'gavetas_ocupadas': gavetas_ocupadas,
        'estoque': Produto.objects.all(),
        'grafico': grafico,
        'quadras': Quadra.objects.prefetch_related('lotes').all(),
    }
    
    template = get_template('relatorio.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_cemiterio.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
