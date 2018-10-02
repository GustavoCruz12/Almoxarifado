from django.db import models
import datetime
import random
from secretaria.models import (Departamento,)
from almoxarifado.users.models import User
from secretaria.models import Almoxarifado

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    ABERTA = True
    FECHADA = False
    STATUS_CHOICES = (
        (ABERTA , 'Aberta'),
        (FECHADA, 'fechada'),
    ) 
    status = models.BooleanField('Status da Solicitação', choices=STATUS_CHOICES, default=ABERTA)
    data_emissao = models.DateField(auto_now_add=True)
    numero_descricao = models.CharField(max_length=32, unique=True)
    movimentacao_relacionamento = models.ForeignKey(Movimentacao, on_delete=models.CASCADE)
    almoxarifado_relacionamento = models.ForeignKey(Almoxarifado, on_delete=models.CASCADE)
    departamento_relacionamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    requisicao_enviado = models.BooleanField(default=False, blank=True)
    requisicao_secretario = models.BooleanField(default=False, blank=True)
    requisicao_processamento = models.BooleanField(default=False, blank=True)
    requisicao_transito = models.BooleanField(default=False, blank=True)
    requisicao_recebido = models.BooleanField(default=False, blank=True)
    
    class Meta:
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'
        permissions = (
            ('administrativo_permissao', 'administrativo permissao'),
            ('entrega_permissao', 'entrega permissao'),
            ('secretario_permissao', 'secretario permissao'),
        )

    def __str__(self):
        return self.numero_descricao

    def save(self, *args, **kwargs):
        super (Solicitacao, self).save(*args, **kwargs)
        ano_corrente = datetime.datetime.now()
        if not self.numero_descricao:
            self.numero_descricao = f"{ano_corrente.year}00{self.id}"
            self.save



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
    descricao_material = models.CharField('Descrição do Material', max_length=100)
    codigo_material = models.IntegerField(blank=False, null=False)
    almoxarifado_relacionamento = models.ForeignKey(Almoxarifado, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

    def __str__(self):
        return self.descricao_material


class Materiais_Solicitacao(models.Model):
    quantidade_material = models.FloatField('Quantidade de Material', null=False, blank=False)
    quantidade_aprovada = models.FloatField('Quantidade Aprovada', blank=True, null=True)
    relacionamento_materiais = models.ForeignKey(Materiais, on_delete=models.CASCADE)
    relacionamento_solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    unidade_relacionamento = models.ForeignKey(Unidade, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Material da Solicitação'
        verbose_name_plural = 'Material das Solicitações'

    def __str__(self):
        return str(self.relacionamento_materiais)