# Generated by Django 2.0.7 on 2018-09-10 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacao', '0009_auto_20180910_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solicitacao',
            options={'permissions': (('administrativo_permissao', 'administrativo permissao'), ('entrega_permissao', 'entrega permissao')), 'verbose_name': 'Solicitação', 'verbose_name_plural': 'Solicitações'},
        ),
    ]
