# backend/core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Fornecedor, NotaFiscal, ItemNotaFiscal, Recebimento, ItemRecebido, Material, PlanoCompra, ItemPlanoCompra


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

class UserSerializer(serializers.ModelSerializer):
    # Vamos buscar os nomes dos grupos aos quais o usuário pertence
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class ItemNotaFiscalSerializer(serializers.ModelSerializer):
    material_descricao = serializers.CharField(source='material.descricao', read_only=True)
    class Meta:
        model = ItemNotaFiscal
        fields = ['id', 'material', 'material_descricao', 'quantidade', 'valor_unitario']

class NotaFiscalSerializer(serializers.ModelSerializer):
    itens_nf = ItemNotaFiscalSerializer(many=True, read_only=True)
    class Meta:
        model = NotaFiscal
        fields = ['id', 'numero', 'fornecedor', 'data_emissao', 'valor_total', 'arquivo_xml', 'itens_nf']

class ItemRecebidoSerializer(serializers.ModelSerializer):
    material_descricao = serializers.CharField(source='material.descricao', read_only=True)
    class Meta:
        model = ItemRecebido
        fields = ['id', 'material', 'material_descricao', 'quantidade_contada']

class RecebimentoSerializer(serializers.ModelSerializer):
    itens_recebidos = ItemRecebidoSerializer(many=True, read_only=True)
    class Meta:
        model = Recebimento
        fields = ['id', 'plano_compra', 'nota_fiscal', 'conferente', 'data_recebimento', 'observacoes', 'itens_recebidos']