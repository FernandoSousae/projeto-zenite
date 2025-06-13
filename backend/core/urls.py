# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Cria um roteador
router = DefaultRouter()
# Registra nosso ViewSet com o roteador, definindo o prefixo da URL
router.register(r'planos-compra', views.PlanoCompraViewSet, basename='planocompra')

# Nossas URLs agora são compostas pelas rotas geradas pelo roteador
# e pelo nosso endpoint customizado que já existia.
urlpatterns = [
    path('', include(router.urls)),
    path('recebimentos/<int:recebimento_id>/conciliar/', views.conciliar_recebimento, name='conciliar-recebimento'),
]