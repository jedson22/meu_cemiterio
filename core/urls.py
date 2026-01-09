from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quadra/<int:quadra_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('quadra/<int:quadra_id>/novo_lote/', views.criar_lote, name='criar_lote'),
    path('lote/<int:lote_id>/', views.detalhe_lote, name='detalhe_lote'),
    path('gaveta/<int:gaveta_id>/adicionar/', views.adicionar_falecido, name='adicionar_falecido'),
    
    # Rota para o botão de exumar
    path('falecido/<int:falecido_id>/exumar/', views.exumar_falecido, name='exumar_falecido'),
]
