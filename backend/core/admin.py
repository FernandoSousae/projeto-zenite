from django.contrib import admin
from .models import (
    Fornecedor, Material, PlanoCompra, ItemPlanoCompra,
    NotaFiscal, ItemNotaFiscal, Recebimento, ItemRecebido,
    Defeito, InspecaoQualidade, ItemInspecionadoDefeito
)

# -----------------------------------------------------------------------------
# INLINES - Para editar itens dentro de seus "pais"
# -----------------------------------------------------------------------------
class ItemPlanoCompraInline(admin.TabularInline):
    model = ItemPlanoCompra
    fields = ('material', 'quantidade_prevista', 'preco_unitario', 'cor', 'grade_numeracao')
    extra = 1

class ItemNotaFiscalInline(admin.TabularInline):
    model = ItemNotaFiscal
    fields = ('material', 'quantidade', 'valor_unitario')
    extra = 1

class ItemRecebidoInline(admin.TabularInline):
    model = ItemRecebido
    fields = ('material', 'quantidade_contada')
    extra = 1

# -----------------------------------------------------------------------------
# MODEL ADMINS - Para customizar as páginas principais dos modelos
# -----------------------------------------------------------------------------
@admin.register(PlanoCompra)
class PlanoCompraAdmin(admin.ModelAdmin):
    inlines = [ItemPlanoCompraInline]
    list_display = ('codigo_plano', 'fornecedor', 'data_prevista_entrega', 'status', 'created_at')
    list_filter = ('status', 'fornecedor')
    search_fields = ('codigo_plano', 'fornecedor__nome_fantasia')

@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    inlines = [ItemNotaFiscalInline]
    list_display = ('numero', 'fornecedor', 'data_emissao', 'valor_total')
    list_filter = ('fornecedor',)
    search_fields = ('numero', 'fornecedor__nome_fantasia')

@admin.register(Recebimento)
class RecebimentoAdmin(admin.ModelAdmin):
    inlines = [ItemRecebidoInline]
    list_display = ('__str__', 'plano_compra', 'nota_fiscal', 'conferente', 'data_recebimento')
    list_filter = ('conferente', 'data_recebimento')
    search_fields = ('plano_compra__codigo_plano', 'nota_fiscal__numero')

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('codigo_interno', 'descricao')
    list_display = ('codigo_interno', 'descricao', 'unidade_medida')
    list_filter = ('unidade_medida',)

# --- Configuração CORRIGIDA para o Módulo de Qualidade ---

@admin.register(Defeito)
class DefeitoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'created_at')
    search_fields = ('nome',)

@admin.register(InspecaoQualidade)
class InspecaoQualidadeAdmin(admin.ModelAdmin):
    # A linha 'inlines' foi REMOVIDA daqui, pois causava o erro.
    list_display = ('id', 'recebimento', 'revisor', 'status', 'created_at')
    list_filter = ('status', 'revisor')
    search_fields = ('recebimento__id',)

# A classe ItemInspecionadoDefeitoInline foi REMOVIDA.
# Em seu lugar, registramos o modelo de forma independente.
@admin.register(ItemInspecionadoDefeito)
class ItemInspecionadoDefeitoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'item_recebido', 'defeito', 'quantidade_defeituosa')
    list_filter = ('defeito',)