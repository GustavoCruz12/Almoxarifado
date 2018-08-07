# Generated by Django 2.0.7 on 2018-08-07 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacao', '0014_solicitacao_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiais_solicitacao',
            name='relacionamento_materiais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitacao.Materiais'),
        ),
        migrations.AlterField(
            model_name='materiais_solicitacao',
            name='relacionamento_solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitacao.Solicitacao'),
        ),
        migrations.AlterField(
            model_name='materiais_solicitacao',
            name='unidade_relacionamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitacao.Unidade'),
        ),
    ]
