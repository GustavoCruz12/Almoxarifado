from django import forms
from django.forms import inlineformset_factory, ModelForm
from django_select2.forms import ModelSelect2Widget
from .models import (Solicitacao, Movimentacao, Materiais, Materiais_Solicitacao, Unidade)
from secretaria.models import (Departamento, Secretaria, Almoxarifado)


class DepartamentoForm(forms.ModelForm):
    nome_secretaria = forms.ModelChoiceField(
        queryset=Secretaria.objects.all(),
        label=u"Secretaria",
        widget=ModelSelect2Widget(
            model=Secretaria,
            search_fields=['nome_secretaria__icontains']
        )
    )
    nome_departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label=u"Departamento",
        widget=ModelSelect2Widget(
            model=Departamento,
            search_fields=['nome_departamento__icontains'],
            dependent_fields={'nome_secretaria': 'Secretaria'},
            max_results=500,
        )
    )


class SecretariaForm(forms.ModelForm):

    class Meta:
        model = Secretaria
        fields = ['nome_secretaria']


class SolicitacaoForm(forms.ModelForm):

    class Meta:
        model = Solicitacao
        fields = [
            'movimentacao_relacionamento',
            'almoxarifado_relacionamento',
            'departamento_relacionamento',
            'requisicao_processamento',
            'requisicao_transito',
        ]


class Material_SolicitacaoForm(ModelForm):

    class Meta:
        model = Materiais_Solicitacao
        exclude = ['quantidade_material', 'unidade_relacionamento', 'relacionamento_materiais']
        

    
MateriaisFormSet = inlineformset_factory(Solicitacao, Materiais_Solicitacao, form=Material_SolicitacaoForm, extra=0, can_delete=False)
MateriaisFormSetUP = inlineformset_factory(Solicitacao, Materiais_Solicitacao, fields=('quantidade_material', 'quantidade_aprovada', 'unidade_relacionamento', 'relacionamento_materiais'), extra=1)

class MateriaisForm(forms.ModelForm):

    class Meta:
        model = Materiais
        fields = [
            'descricao_material',
            'codigo_material'
        ]


class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = [
            'tipo_unidade',
            'unidade_descricao'
        ]


class MovimentacaoForm(forms.ModelForm):

    class Meta:
        model = Movimentacao
        fields = [
            'tipo_movimentacao',
            'movimentacao_descricao',
        ]