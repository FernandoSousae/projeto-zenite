# core/admin.py

from django.contrib import admin
from .models import Fornecedor, Material, PlanoCompra, ItemPlanoCompra

# -----------------------------------------------------------------------------
# 1. Definimos a classe "Inline" para os Itens
# -----------------------------------------------------------------------------
class ItemPlanoCompraInline(admin.TabularInline):
    """
    Permite adicionar e editar Itens do Plano de Compra diretamente na página do
    Plano de Compra. 'TabularInline' mostra os itens em formato de tabela.
    """
    model = ItemPlanoCompra
    # Campos que aparecerão na tabela de itens
    fields = ('material', 'quantidade_prevista', 'preco_unitario', 'cor', 'grade_numeracao')
    # Quantas linhas em branco extras aparecerão por padrão
    extra = 1

# -----------------------------------------------------------------------------
# 2. Definimos a classe "Admin" principal para o Plano de Compra
# -----------------------------------------------------------------------------
@admin.register(PlanoCompra)
class PlanoCompraAdmin(admin.ModelAdmin):
    """
    Customiza a aparência e o comportamento do modelo PlanoCompra na área admin.
    """
    # Inclui a tabela de itens definida acima na página de edição do Plano de Compra
    inlines = [ItemPlanoCompraInline]
    # Melhora a visualização da lista de todos os planos de compra
    list_display = ('codigo_plano', 'fornecedor', 'data_prevista_entrega', 'status', 'created_at')
    # Adiciona filtros na barra lateral direita
    list_filter = ('status', 'fornecedor')
    # Adiciona um campo de busca
    search_fields = ('codigo_plano', 'fornecedor__nome_fantasia')


# -----------------------------------------------------------------------------
# 3. Registramos os outros modelos de forma simples
# -----------------------------------------------------------------------------
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('codigo_interno', 'descricao')


# Nota: Não precisamos mais registrar o ItemPlanoCompra separadamente,
# pois ele agora é gerenciado através do PlanoCompraAdmin.
# A linha admin.site.register(ItemPlanoCompra) foi removida.