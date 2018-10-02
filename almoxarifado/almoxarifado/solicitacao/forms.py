from django import forms
from django.forms import inlineformset_factory, ModelForm
from django_select2.forms import ModelSelect2Widget
from .models import (Solicitacao, Movimentacao, Materiais, Materiais_Solicitacao, Unidade)
from secretaria.models import (Departamento, Secretaria, Almoxarifado)


class SolicitacaoForm(forms.ModelForm):

    class Meta:
        model = Solicitacao
        fields = [
            'movimentacao_relacionamento',
            
            'requisicao_processamento',
            'requisicao_transito',
            'requisicao_secretario',
        ]


class Material_SolicitacaoForm(ModelForm):

    class Meta:
        model = Materiais_Solicitacao
        exclude = ['quantidade_material', 
                   'unidade_relacionamento', 
                   'relacionamento_materiais']
        

    
MateriaisFormSet = inlineformset_factory(Solicitacao, Materiais_Solicitacao, form=Material_SolicitacaoForm, extra=0, can_delete=False)
MateriaisFormSetUP = inlineformset_factory(Solicitacao, Materiais_Solicitacao, fields=('quantidade_material', 'quantidade_aprovada', 'unidade_relacionamento', 'relacionamento_materiais'), extra=1)
MateriaisFormSetUPSEC = inlineformset_factory(Solicitacao, Materiais_Solicitacao, fields=('quantidade_material', 'unidade_relacionamento', 'relacionamento_materiais'), extra=0)

class MateriaisForm(forms.ModelForm):

    class Meta:
        model = Materiais
        fields = [
            'descricao_material',
            'codigo_material',
            'almoxarifado_relacionamento',
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