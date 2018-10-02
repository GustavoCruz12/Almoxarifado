# Generated by Django 2.0.7 on 2018-09-26 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0001_initial'),
        ('users', '0009_auto_20180917_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='almoxarifado_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='secretaria.Almoxarifado'),
        ),
        migrations.AddField(
            model_name='user',
            name='departamento_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='secretaria.Departamento'),
        ),
    ]