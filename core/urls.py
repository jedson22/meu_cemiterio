from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # Cemitério
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('quadra/<int:quadra_id>/novo_lote/', views.criar_lote, name='criar_lote'),
    path('lote/<int:lote_id>/', views.detalhe_lote, name='detalhe_lote'),
    path('gaveta/<int:gaveta_id>/adicionar/', views.adicionar_falecido, name='adicionar_falecido'),
    path('falecido/<int:falecido_id>/exumar/', views.exumar_falecido, name='exumar_falecido'),
    
    # Estoque
    path('estoque/', views.lista_estoque, name='lista_estoque'),
    path('estoque/adicionar/', views.adicionar_produto, name='adicionar_produto'),
]
