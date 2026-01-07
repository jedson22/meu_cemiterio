from django.urls import path
from . import views

urlpatterns = [
    # Principal
    path('', views.index, name='index'),
    path('sair/', views.encerrar_sessao, name='sair'),
    path('relatorio/', views.gerar_relatorio, name='gerar_relatorio'),

    # Cemitério
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),
    path('vender-lote/<int:lote_id>/', views.vender_lote, name='vender_lote'),
    path('transferir-lote/<int:lote_id>/', views.transferir_lote, name='transferir_lote'),
    path('registrar-obito/<int:gaveta_id>/', views.registrar_obito, name='registrar_obito'),
    path('limpar-gaveta/<int:gaveta_id>/', views.limpar_gaveta, name='limpar_gaveta'),

    # Estrutura
    path('adicionar-quadra/', views.adicionar_quadra, name='adicionar_quadra'),
    path('excluir-quadra/<int:quadra_id>/', views.excluir_quadra, name='excluir_quadra'),
    path('adicionar-lote/<int:quadra_id>/', views.adicionar_lote, name='adicionar_lote'),
    path('excluir-lote/<int:lote_id>/', views.excluir_lote, name='excluir_lote'),

    # Estoque
    path('estoque/', views.lista_estoque, name='lista_estoque'),
    path('estoque/add/', views.adicionar_produto, name='adicionar_produto'),
    path('estoque/update/<int:produto_id>/', views.atualizar_estoque, name='atualizar_estoque'),
    path('estoque/delete/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
]
