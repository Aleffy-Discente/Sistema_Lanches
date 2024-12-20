from django.urls import path
from api_lanches import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:id>/', views.cliente_detalhado, name='cliente_detalhado'),
    path('clientes/<int:id>/historico/', views.historico_pedidos, name='historico_pedidos'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/<int:id>/', views.produto_detalhado, name='produto_detalhado'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:id>/', views.pedido_detalhado, name='pedido_detalhado'),
]
