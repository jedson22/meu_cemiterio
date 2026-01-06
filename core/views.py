from django.shortcuts import render, redirect, get_object_or_404
from .models import Quadra, Lote, Gaveta
from django.http import HttpResponse
import csv
from datetime import datetime

def index(request):
    quadras = Quadra.objects.all().order_by('numero')
    lista = []
    for q in quadras:
        total = q.lotes.count() * 3
        indisp = Gaveta.objects.filter(lote__quadra=q, status__in=['Ocupado','Vendido']).count()
        cor = "primary"
        if indisp > 0: cor = "warning"
        if total > 0 and indisp == total: cor = "danger"
        lista.append({'obj':q, 'cor':cor, 'ocupados':indisp, 'total':total})
    return render(request, 'core/index.html', {'quadras': lista})

def detalhe_quadra(request, q_id):
    quadra = get_object_or_404(Quadra, numero=q_id)
    lotes = quadra.lotes.all().order_by('numero')
    lista = []
    tot_indisp = 0
    tot_geral = lotes.count() * 3
    for l in lotes:
        occ = l.gavetas.filter(status__in=['Ocupado','Vendido']).count()
        tot_indisp += occ
        cor = "outline-light"
        cheio = False
        if occ > 0: cor = "warning"
        if occ == 3: cor = "secondary"; cheio = True
        lista.append({'obj':l, 'cor':cor, 'cheio':cheio})
    perc = int((tot_indisp/tot_geral)*100) if tot_geral > 0 else 0
    return render(request, 'core/quadra.html', {'quadra':quadra, 'lotes':lista, 'percentual':perc})

def detalhe_lote(request, q_id, l_id):
    quadra = get_object_or_404(Quadra, numero=q_id)
    lote = get_object_or_404(Lote, quadra=quadra, numero=l_id)
    gavetas = lote.gavetas.all().order_by('numero')
    if request.method == 'POST':
        g_id = request.POST.get('gaveta_id')
        acao = request.POST.get('acao')
        g = get_object_or_404(Gaveta, id=g_id)
        if acao == 'liberar':
            g.status='Livre'; g.nome=None; g.data=None
        else:
            g.status='Vendido' if acao=='vender' else 'Ocupado'
            g.nome=request.POST.get('nome')
            dt = request.POST.get('data')
            if dt: g.data=datetime.strptime(dt, '%Y-%m-%d').date()
        g.save()
        return redirect('detalhe_lote', q_id=q_id, l_id=l_id)
    info = []
    css = {'success':'borda-verde','info':'borda-azul','warning':'borda-laranja','danger':'borda-vermelha'}
    for g in gavetas:
        txt, c, msg = g.situacao()
        info.append({'obj':g, 'texto':txt, 'css':css.get(c), 'msg':msg})
    return render(request, 'core/lote.html', {'quadra':quadra, 'lote':lote, 'gavetas':info})

def excluir_lote(request, q_id, l_id):
    lote = get_object_or_404(Lote, quadra__numero=q_id, numero=l_id)
    if request.method == 'POST':
        lote.delete()
        return redirect('detalhe_quadra', q_id=q_id)
    return redirect('detalhe_lote', q_id=q_id, l_id=l_id)

def config(request):
    if request.method == 'POST':
        tp = request.POST.get('tipo')
        if tp == 'inicializar':
            if not Quadra.objects.exists():
                for q in range(1,13):
                    nq = Quadra.objects.create(numero=q)
                    for l in range(1,25):
                        nl = Lote.objects.create(quadra=nq, numero=l)
                        for g in range(1,4): Gaveta.objects.create(lote=nl, numero=g)
        elif tp == 'nova_quadra':
            last = Quadra.objects.order_by('-numero').first()
            nq = Quadra.objects.create(numero=(last.numero+1 if last else 1))
            qtd = int(request.POST.get('qtd_lotes', 24))
            for l in range(1, qtd+1):
                nl = Lote.objects.create(quadra=nq, numero=l)
                for g in range(1,4): Gaveta.objects.create(lote=nl, numero=g)
        elif tp == 'novo_lote':
            qid = request.POST.get('quadra_alvo')
            q = Quadra.objects.get(numero=qid)
            last = q.lotes.order_by('-numero').first()
            nl = Lote.objects.create(quadra=q, numero=(last.numero+1 if last else 1))
            for g in range(1,4): Gaveta.objects.create(lote=nl, numero=g)
            return redirect('detalhe_quadra', q_id=qid)
        return redirect('index')
    existe = Quadra.objects.exists()
    last = Quadra.objects.order_by('-numero').first()
    prox = last.numero+1 if last else 1
    qs = Quadra.objects.all().order_by('numero')
    return render(request, 'core/config.html', {'existe_db':existe, 'prox':prox, 'quadras':qs})

def exportar(request):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
    resp.write(u'\ufeff'.encode('utf8'))
    w = csv.writer(resp, delimiter=';')
    w.writerow(['Quadra','Lote','Gaveta','Status','Nome','Data','Situacao'])
    for g in Gaveta.objects.select_related('lote__quadra').all().order_by('lote__quadra__numero','lote__numero','numero'):
        t,_,m = g.situacao()
        w.writerow([g.lote.quadra.numero, g.lote.numero, g.numero, g.status, g.nome, g.data, f"{t}-{m}"])
    return resp