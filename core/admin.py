# core/admin.py

from django.contrib import admin
from .models import Fornecedor, Material, PlanoCompra, ItemPlanoCompra # Importamos nossos modelos

# Registramos os modelos para que apareçam na área administrativa
admin.site.register(Fornecedor)
admin.site.register(Material)
admin.site.register(PlanoCompra)
admin.site.register(ItemPlanoCompra)