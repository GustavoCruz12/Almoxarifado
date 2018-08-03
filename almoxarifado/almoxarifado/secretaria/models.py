from django.db import models


class Secretaria(models.Model):
    nome_secretaria = models.CharField('Nome da Secretaria', max_length=255)

    class Meta:
        verbose_name = 'Secretaria'
        verbose_name_plural = 'Secretarias'

    def __str__(self):
        return self.nome_secretaria


class Almoxarifado(models.Model):
    ROLE_CHOICES = (
        (1, 'Central'),
        (2, 'Saúde'),
        (3, 'Cozinha Piloto'),
        (4, 'DAES'),
        (5, 'Oficina'),
        (6, 'Educação'),
    )
    tipo_almoxarifado = models.PositiveSmallIntegerField('Almoxarifado', choices=ROLE_CHOICES)
    descricao_almoxarifado = models.CharField('Descrição do Almoxarifado', max_length=255)

    class Meta:
        verbose_name = 'Almoxarifado'
        verbose_name_plural = 'Almoxarifados'

    def __str__(self):
        return self.descricao_almoxarifado


class Departamento(models.Model):
    nome_departamento = models.CharField('Nome do Departamento', max_length=255)
    centro_custo = models.FloatField('Centro de Custo')
    secretaria_relacionamento = models.ForeignKey(Secretaria, on_delete=models.CASCADE)
    almoxarifado_relacionamento = models.ForeignKey(Almoxarifado, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nome_departamento
