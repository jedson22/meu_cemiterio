from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('quadra/<int:q_id>/', views.detalhe_quadra, name='detalhe_quadra'),
    path('lote/<int:q_id>/<int:l_id>/', views.detalhe_lote, name='detalhe_lote'),
    path('lote/<int:q_id>/<int:l_id>/excluir/', views.excluir_lote, name='excluir_lote'),
    path('config/', views.config, name='config'),
    path('exportar/', views.exportar, name='exportar'),
]