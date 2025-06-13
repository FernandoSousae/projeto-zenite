# core/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo Base para adicionar timestamps
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        abstract = True


class Fornecedor(BaseModel):
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=255, verbose_name="Nome Fantasia", blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True, verbose_name="CNPJ")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia or self.razao_social

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

class Material(BaseModel):
    UNIDADES_DE_MEDIDA = [
        ('m²', 'Metro Quadrado (m²)'),
        ('kg', 'Quilograma (kg)'),
        ('par', 'Par'),
        ('un', 'Unidade'),
    ]
    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="Código Interno")
    descricao = models.TextField(verbose_name="Descrição")
    unidade_medida = models.CharField(max_length=3, choices=UNIDADES_DE_MEDIDA, verbose_name="Unidade de Medida")

    def __str__(self):
        return f"{self.codigo_interno} - {self.descricao[:30]}"

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"

class PlanoCompra(BaseModel):
    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Parcial', 'Parcialmente Recebido'),
        ('Concluido', 'Concluído'),
        ('Cancelado', 'Cancelado'),
    ]
    codigo_plano = models.CharField(max_length=20, unique=True, verbose_name="Código do Plano")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name="Fornecedor")
    data_emissao = models.DateField(verbose_name="Data de Emissão")
    data_prevista_entrega = models.DateField(verbose_name="Data Prevista de Entrega")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Aberto')
    usuario_criador = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Criado por")

    def __str__(self):
        return f"{self.codigo_plano} - {self.fornecedor.nome_fantasia}"

    class Meta:
        verbose_name = "Plano de Compra"
        verbose_name_plural = "Planos de Compra"

class ItemPlanoCompra(models.Model): # Note que este não herda de BaseModel
    plano_compra = models.ForeignKey(PlanoCompra, on_delete=models.CASCADE, related_name="itens")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade_prevista = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qtd. Prevista")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    cor = models.CharField(max_length=50, blank=True, null=True)
    grade_numeracao = models.JSONField(blank=True, null=True, verbose_name="Grade de Numeração")

    def __str__(self):
        return f"Item {self.material.codigo_interno} do plano {self.plano_compra.codigo_plano}"

    class Meta:
        verbose_name = "Item do Plano de Compra"
        verbose_name_plural = "Itens dos Planos de Compra"

class NotaFiscal(BaseModel):
    numero = models.CharField(max_length=50, verbose_name="Número da NF")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name="Fornecedor")
    data_emissao = models.DateField(verbose_name="Data de Emissão da NF")
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total da NF")
    arquivo_xml = models.FileField(upload_to='notas_fiscais/', blank=True, null=True, verbose_name="Arquivo XML")

    def __str__(self):
        return f"NF {self.numero} - {self.fornecedor.nome_fantasia}"

    class Meta:
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        # Garante que um fornecedor não pode ter duas notas com o mesmo número
        unique_together = ('numero', 'fornecedor')

class ItemNotaFiscal(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="itens_nf")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.material.codigo_interno} da NF {self.nota_fiscal.numero}"
    
    class Meta:
        verbose_name = "Item da Nota Fiscal"
        verbose_name_plural = "Itens das Notas Fiscais"


class Recebimento(BaseModel):
    plano_compra = models.ForeignKey(PlanoCompra, on_delete=models.PROTECT, verbose_name="Plano de Compra Vinculado")
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.PROTECT, verbose_name="Nota Fiscal Vinculada")
    conferente = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Conferente")
    data_recebimento = models.DateTimeField(auto_now_add=True, verbose_name="Data do Recebimento")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"Recebimento do Plano {self.plano_compra.codigo_plano} em {self.data_recebimento.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Recebimento Físico"
        verbose_name_plural = "Recebimentos Físicos"

    def realizar_conciliacao(self):
        """
        Este método compara os itens do plano, da nota fiscal e do recebimento físico
        para encontrar divergências.
        """
        from .models import Material # Importação local para evitar importação circular

        # 1. Agrupar os dados de cada fonte por material.
        itens_plano = {item.material.id: item.quantidade_prevista for item in self.plano_compra.itens.all()}
        itens_nf = {item.material.id: item.quantidade for item in self.nota_fiscal.itens_nf.all()}
        itens_recebidos = {item.material.id: item.quantidade_contada for item in self.itens_recebidos.all()}

        # 2. Obter a lista de todos os materiais únicos e buscar seus objetos.
        todos_materiais_ids = set(itens_plano.keys()) | set(itens_nf.keys()) | set(itens_recebidos.keys())
        materiais_obj = {m.id: m for m in Material.objects.filter(id__in=todos_materiais_ids)}

        # 3. Iterar sobre cada material e comparar as quantidades.
        resultado_conciliacao = []
        for material_id in todos_materiais_ids:
            material = materiais_obj.get(material_id)
            
            # Usamos .get(chave, 0) para retornar 0 se o material não existir em uma das fontes.
            qtd_plano = itens_plano.get(material_id, 0)
            qtd_nf = itens_nf.get(material_id, 0)
            qtd_recebida = itens_recebidos.get(material_id, 0)

            # Se tudo bate, não há divergência para este item.
            if qtd_plano == qtd_nf == qtd_recebida:
                continue # Pula para o próximo material

            # Se chegamos aqui, há uma divergência. Vamos registrá-la.
            divergencia = {
                'material_codigo': material.codigo_interno,
                'material_descricao': material.descricao,
                'qtd_plano': qtd_plano,
                'qtd_nf': qtd_nf,
                'qtd_recebida': qtd_recebida,
                'tipo_divergencia': [] # Uma lista para armazenar os problemas
            }

            # Lógica para identificar os tipos de divergência
            if qtd_recebida > qtd_nf:
                divergencia['tipo_divergencia'].append('Recebido a mais que a NF')
            elif qtd_recebida < qtd_nf:
                divergencia['tipo_divergencia'].append('Recebido a menos que a NF')

            if qtd_nf != qtd_plano:
                divergencia['tipo_divergencia'].append('NF diferente do Plano de Compra')
            
            if qtd_recebida > 0 and qtd_plano == 0:
                 divergencia['tipo_divergencia'].append('Item não consta no Plano de Compra')

            resultado_conciliacao.append(divergencia)

        return resultado_conciliacao

class ItemRecebido(models.Model):
    recebimento = models.ForeignKey(Recebimento, on_delete=models.CASCADE, related_name="itens_recebidos")
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade_contada = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantidade_contada} x {self.material.codigo_interno} no recebimento {self.recebimento.id}"

    class Meta:
        verbose_name = "Item Recebido"
        verbose_name_plural = "Itens Recebidos"