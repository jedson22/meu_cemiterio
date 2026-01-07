from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    
    # Visualizações
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),
    
    # Ações (Botões)
    path('vender-lote/<int:lote_id>/', views.vender_lote, name='vender_lote'),
    path('registrar-obito/<int:gaveta_id>/', views.registrar_obito, name='registrar_obito'),
]
