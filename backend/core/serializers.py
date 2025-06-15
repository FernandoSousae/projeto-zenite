# backend/core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Fornecedor, NotaFiscal, ItemNotaFiscal, Recebimento, ItemRecebido, Material, PlanoCompra, ItemPlanoCompra, Defeito, InspecaoQualidade


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
    # Usando outros serializers para aninhar os dados completos
    plano_compra = PlanoCompraSerializer(read_only=True)
    nota_fiscal = NotaFiscalSerializer(read_only=True)
    itens_recebidos = ItemRecebidoSerializer(many=True, read_only=True)
    conferente_username = serializers.CharField(source='conferente.username', read_only=True)

    # Campos para receber os IDs na criação (writable)
    plano_compra_id = serializers.PrimaryKeyRelatedField(
        queryset=PlanoCompra.objects.all(), source='plano_compra', write_only=True
    )
    nota_fiscal_id = serializers.PrimaryKeyRelatedField(
        queryset=NotaFiscal.objects.all(), source='nota_fiscal', write_only=True
    )

    class Meta:
        model = Recebimento
        fields = [
            'id', 
            'plano_compra', 'plano_compra_id',  # plano_compra para leitura, _id para escrita
            'nota_fiscal', 'nota_fiscal_id',   # nota_fiscal para leitura, _id para escrita
            'conferente_username', 
            'data_recebimento', 
            'observacoes', 
            'itens_recebidos'
        ]

class ItemRecebidoCreateSerializer(serializers.Serializer):
    material_id = serializers.IntegerField()
    quantidade_contada = serializers.DecimalField(max_digits=10, decimal_places=2)

class DefeitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defeito
        fields = ['id', 'nome', 'descricao']


class InspecaoQualidadeSerializer(serializers.ModelSerializer):
    # Campos que são apenas para leitura (mostrados, mas não esperados na criação)
    revisor_username = serializers.CharField(source='revisor.username', read_only=True)
    recebimento_id = serializers.IntegerField(source='recebimento.id', read_only=True)

    # Campo que será usado para criar/associar o recebimento
    recebimento = serializers.PrimaryKeyRelatedField(
        queryset=Recebimento.objects.all(), write_only=True
    )

    class Meta:
        model = InspecaoQualidade
        fields = [
            'id', 
            'recebimento', # Campo de escrita (write-only)
            'recebimento_id', # Campo de leitura (read-only)
            'revisor_username', # Campo de leitura (read-only)
            'status', 
            'observacoes_gerais', 
            'created_at'
        ]
        read_only_fields = ['revisor_username']