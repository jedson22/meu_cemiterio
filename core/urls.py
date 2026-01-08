from django.urls import path
from . import views

urlpatterns = [
    # Página Inicial e Login
    path('', views.index, name='index'),
    path('sair/', views.encerrar_sessao, name='sair'),
    path('relatorio/', views.gerar_relatorio, name='gerar_relatorio'),

    # Visualização do Cemitério
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),
    
    # Ações de Lote e Gaveta
    path('vender-lote/<int:lote_id>/', views.vender_lote, name='vender_lote'),
    path('transferir-lote/<int:lote_id>/', views.transferir_lote, name='transferir_lote'),
    path('registrar-obito/<int:gaveta_id>/', views.registrar_obito, name='registrar_obito'),
    path('limpar-gaveta/<int:gaveta_id>/', views.limpar_gaveta, name='limpar_gaveta'),
    
    # Histórico Manual
    path('add-historico/<int:gaveta_id>/', views.adicionar_historico_manual, name='adicionar_historico_manual'),

    # Estrutura (Quadras)
    path('adicionar-quadra/', views.adicionar_quadra, name='adicionar_quadra'),
    path('excluir-quadra/<int:quadra_id>/', views.excluir_quadra, name='excluir_quadra'),
    
    # --- AQUI ESTAVA O ERRO PROVAVELMENTE ---
    # Rotas para Adicionar Lote com Número Personalizado
    path('form-lote/<int:quadra_id>/', views.form_adicionar_lote, name='form_adicionar_lote'),
    path('salvar-lote/<int:quadra_id>/', views.salvar_lote, name='salvar_lote'),
    path('excluir-lote/<int:lote_id>/', views.excluir_lote, name='excluir_lote'),

    # Estoque
    path('estoque/', views.lista_estoque, name='lista_estoque'),
    path('estoque/add/', views.adicionar_produto, name='adicionar_produto'),
    path('estoque/update/<int:produto_id>/', views.atualizar_estoque, name='atualizar_estoque'),
    path('estoque/delete/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
]
