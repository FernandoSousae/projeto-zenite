from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    PlanoCompra, ItemPlanoCompra, Material, Fornecedor, 
    NotaFiscal, ItemNotaFiscal, Recebimento, ItemRecebido,
    Defeito, InspecaoQualidade, ItemInspecionadoDefeito
)


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class ItemPlanoCompraSerializer(serializers.ModelSerializer):
    material_descricao = serializers.CharField(source='material.descricao', read_only=True)
    class Meta:
        model = ItemPlanoCompra
        fields = ['id', 'material', 'material_descricao', 'quantidade_prevista', 'preco_unitario', 'cor', 'grade_numeracao']


class PlanoCompraSerializer(serializers.ModelSerializer):
    itens = ItemPlanoCompraSerializer(many=True, read_only=True)
    class Meta:
        model = PlanoCompra
        fields = ['id', 'codigo_plano', 'fornecedor', 'data_emissao', 'data_prevista_entrega', 'status', 'usuario_criador', 'created_at', 'updated_at', 'itens']


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'razao_social', 'nome_fantasia', 'cnpj']


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


# --- ORDEM CORRIGIDA AQUI ---

# DEFINIMOS PRIMEIRO O SERIALIZER DO "FILHO"
class ItemInspecionadoDefeitoSerializer(serializers.ModelSerializer):
    defeito_nome = serializers.CharField(source='defeito.nome', read_only=True)
    class Meta:
        model = ItemInspecionadoDefeito
        fields = ['id', 'defeito_nome', 'quantidade_defeituosa']


# AGORA PODEMOS USÁ-LO NO SERIALIZER DO "PAI"
class ItemRecebidoSerializer(serializers.ModelSerializer):
    material_descricao = serializers.CharField(source='material.descricao', read_only=True)
    defeitos_encontrados = ItemInspecionadoDefeitoSerializer(many=True, read_only=True)
    class Meta:
        model = ItemRecebido
        fields = ['id', 'material', 'material_descricao', 'quantidade_contada', 'defeitos_encontrados']


class RecebimentoSerializer(serializers.ModelSerializer):
    itens_recebidos = ItemRecebidoSerializer(many=True, read_only=True)
    conferente_username = serializers.CharField(source='conferente.username', read_only=True)
    plano_compra = PlanoCompraSerializer(read_only=True)
    nota_fiscal = NotaFiscalSerializer(read_only=True)

    # CAMPO CORRIGIDO E ESSENCIAL:
    inspecao_id = serializers.ReadOnlyField(source='inspecao.id')

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
            'plano_compra', 'plano_compra_id',
            'nota_fiscal', 'nota_fiscal_id',
            'conferente_username', 
            'data_recebimento', 
            'observacoes', 
            'itens_recebidos',
            'inspecao_id' # Garantir que está na lista de campos
        ]


class DefeitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defeito
        fields = ['id', 'nome', 'descricao']


class InspecaoQualidadeSerializer(serializers.ModelSerializer):
    revisor_username = serializers.CharField(source='revisor.username', read_only=True)
    recebimento = RecebimentoSerializer(read_only=True)
    recebimento_id = serializers.PrimaryKeyRelatedField(
        queryset=Recebimento.objects.all(), source='recebimento', write_only=True
    )
    class Meta:
        model = InspecaoQualidade
        fields = [
            'id', 'recebimento', 'recebimento_id', 'revisor_username', 
            'status', 'observacoes_gerais', 'created_at'
        ]
        read_only_fields = ['revisor_username']


class RegistrarDefeitoSerializer(serializers.Serializer):
    item_recebido_id = serializers.IntegerField()
    defeito_id = serializers.IntegerField()
    quantidade_defeituosa = serializers.DecimalField(max_digits=10, decimal_places=2)