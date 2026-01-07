from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    
    # Visualizar uma Quadra inteira
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    
    # Visualizar um Lote específico (A linha que estava dando erro)
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),

    # Ação de Vender
    path('vender-lote/<int:lote_id>/', views.vender_lote, name='vender_lote'),
]
