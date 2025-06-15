"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # A rota para a área administrativa do Django
    path('admin/', admin.site.urls),

    # A rota que direciona para as URLs do nosso app 'core'
    # (ex: /api/fornecedores/, /api/planos-compra/)
    path('api/', include('core.urls')),

    # A NOVA LINHA: cria as páginas de login e logout que a
    # interface web da API (Browsable API) precisa para funcionar.
    path('api-auth/', include('rest_framework.urls')),
]