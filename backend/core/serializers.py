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

    # CAMPO PARA ESCRITA (write)
    material_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItemRecebido
        fields = ['id', 'material', 'material_descricao', 'quantidade_contada', 'defeitos_encontrados', 'material_id']
        read_only_fields = ['material', 'defeitos_encontrados']


class RecebimentoSerializer(serializers.ModelSerializer):
    # --- CAMPOS PARA LEITURA (read_only) ---
    conferente_username = serializers.CharField(source='conferente.username', read_only=True)
    plano_compra = PlanoCompraSerializer(read_only=True)
    nota_fiscal = NotaFiscalSerializer(read_only=True)
    inspecao_id = serializers.ReadOnlyField(source='inspecao.id')
    itens_recebidos = ItemRecebidoSerializer(many=True, read_only=True)

    # --- CAMPOS PARA ESCRITA (write_only) ---
    plano_compra_id = serializers.PrimaryKeyRelatedField(
        queryset=PlanoCompra.objects.all(), source='plano_compra', write_only=True
    )
    nota_fiscal_id = serializers.PrimaryKeyRelatedField(
        queryset=NotaFiscal.objects.all(), source='nota_fiscal', write_only=True, required=False, allow_null=True
    )
    # Este é o nosso novo campo para receber os itens do formulário
    itens_a_receber = ItemRecebidoSerializer(many=True, write_only=True)

    class Meta:
        model = Recebimento
        fields = [
            'id', 
            'plano_compra', 'plano_compra_id',
            'nota_fiscal', 'nota_fiscal_id',
            'conferente_username', 
            'data_recebimento', 
            'observacoes', 
            'itens_recebidos',   # para ler
            'itens_a_receber',   # para escrever
            'inspecao_id'
        ]

    def create(self, validated_data):
        # Agora pegamos os itens do nosso novo campo 'itens_a_receber'
        itens_data = validated_data.pop('itens_a_receber')

        # Removemos os outros campos de escrita para passar para o create do Recebimento
        validated_data.pop('plano_compra')
        validated_data.pop('nota_fiscal', None) # Usamos .pop com default para o campo não obrigatório

        # Criamos o recebimento
        recebimento = Recebimento.objects.create(**validated_data, conferente=self.context['request'].user)

        # Criamos os itens recebidos
        for item_data in itens_data:
            # O 'material_id' que definimos no ItemRecebidoSerializer será usado aqui
            ItemRecebido.objects.create(recebimento=recebimento, **item_data)

        return recebimento


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