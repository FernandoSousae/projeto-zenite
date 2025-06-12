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