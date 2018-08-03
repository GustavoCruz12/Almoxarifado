from django.db import models
import random
from secretaria.models import (Departamento,)


def numero_solicitacao():
    return str(random.randint(10000, 99999))


class Movimentacao(models.Model):
    ROLE_CHOICES = (
        (1, 'Requisição'),
        (2, 'Devolução'),
    )
    tipo_movimentacao = models.PositiveSmallIntegerField('Tipo de Movimentação', choices=ROLE_CHOICES)
    movimentacao_descricao = models.CharField('Descrição de Movimentação', max_length=255)

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
 
    def __str__(self):
        return self.movimentacao_descricao


class Solicitacao(models.Model):
    ROLE_CHOICES = (
        (1, 'Aberta'),
        (2, 'Fechada'),
    )
    aberta_fechada = models.PositiveSmallIntegerField('Status da Solicitação', choices=ROLE_CHOICES, default='Aberta'),
    data_emissao = models.DateField(auto_now_add=True)
    descricao_solicitacao = models.CharField('Descrição da Solicitacao', max_length=255)
    numero_descricao = models.CharField(default=numero_solicitacao, max_length=255)
    movimentacao_relacionamento = models.ForeignKey(Movimentacao, on_delete=models.CASCADE)
    departamento_relacionamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    requisicao_enviado = models.BooleanField(default=False)
    requisicao_processamento = models.BooleanField(default=False)
    requisicao_transito = models.BooleanField(default=False)
    requisicao_recebido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'

    def __str__(self):
        return self.descricao_solicitacao


class Unidade(models.Model):
    UNIDADE_CHOICES = (
        ('M²', 'm²'),
        ('KG', 'kg'),
        ('UN', 'un'),
        ('M', 'm'),
        ('CM', 'cm'),
        ('MM', 'mm'),
    )
    tipo_unidade = models.CharField('Tipo de Unidade', choices=UNIDADE_CHOICES, max_length=255, blank=True, null=True)
    unidade_descricao = models.CharField('Descrição Unidade', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return str(self.tipo_unidade)

 
class Materiais(models.Model):
    descricao_material = models.CharField('Descrição do Material', max_length=255)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

    def __str__(self):
        return self.descricao_material


class Materiais_Solicitacao(models.Model):
    descricao_material = models.CharField('Descrição do Material', max_length=255, null=True, blank=True)
    quantidade_material = models.FloatField('Quantidade de Material', null=False, blank=False)
    quantidade_aprovada = models.FloatField('Quantidade Aprovada', blank=True, null=True)
    relacionamento_materiais = models.ForeignKey(Materiais, 'Relacionamento com Materiais')
    relacionamento_solicitacao = models.ForeignKey(Solicitacao, 'Relacionamento com Solicitacao')
    unidade_relacionamento = models.ForeignKey(Unidade, 'Relacionamento com a unidade')

    class Meta:
        verbose_name = 'Material da Solicitação'
        verbose_name_plural = 'Material das Solicitações'

    def __str__(self):
        return str(self.relacionamento_materiais)