# backend/core/serializers.py
from rest_framework import serializers
from .models import PlanoCompra, ItemPlanoCompra, Material, Fornecedor

# 1. Criamos um serializer para os Itens
class ItemPlanoCompraSerializer(serializers.ModelSerializer):
    # Para mostrar o nome do material em vez de apenas o ID
    material_descricao = serializers.CharField(source='material.descricao', read_only=True)

    class Meta:
        model = ItemPlanoCompra
        fields = ['id', 'material', 'material_descricao', 'quantidade_prevista', 'preco_unitario', 'cor', 'grade_numeracao']

# 2. Modificamos o serializer do Plano de Compra
class PlanoCompraSerializer(serializers.ModelSerializer):
    # 3. Aninhamos o serializer de Itens aqui
    itens = ItemPlanoCompraSerializer(many=True, read_only=True)

    class Meta:
        model = PlanoCompra
        # É uma boa prática listar os campos explicitamente
        fields = ['id', 'codigo_plano', 'fornecedor', 'data_emissao', 'data_prevista_entrega', 'status', 'usuario_criador', 'created_at', 'updated_at', 'itens']

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'razao_social', 'nome_fantasia', 'cnpj']