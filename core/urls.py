from django.urls import path
from . import views

urlpatterns = [
    # --- PÁGINAS ---
    path('', views.index, name='index'),
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),
    
    # --- AÇÕES DE LOTE E GAVETA ---
    path('vender-lote/<int:lote_id>/', views.vender_lote, name='vender_lote'),
    path('registrar-obito/<int:gaveta_id>/', views.registrar_obito, name='registrar_obito'),
    path('limpar-gaveta/<int:gaveta_id>/', views.limpar_gaveta, name='limpar_gaveta'), # Novo

    # --- AÇÕES DE ESTRUTURA (CRIAR/EXCLUIR) ---
    path('adicionar-quadra/', views.adicionar_quadra, name='adicionar_quadra'),
    path('excluir-quadra/<int:quadra_id>/', views.excluir_quadra, name='excluir_quadra'),
    path('adicionar-lote/<int:quadra_id>/', views.adicionar_lote, name='adicionar_lote'),
    path('excluir-lote/<int:lote_id>/', views.excluir_lote, name='excluir_lote'),
]
