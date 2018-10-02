from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    View,
)
from django.shortcuts import render, redirect, get_object_or_404

from django.db import transaction

from django.contrib import messages

from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import (Solicitacao, Materiais_Solicitacao, Materiais)

from .forms import (SolicitacaoForm, MateriaisFormSet, MateriaisFormSetUP, MateriaisForm, MateriaisFormSetUPSEC)

from .render import Render

from secretaria.models import Almoxarifado, Departamento

from almoxarifado.users.models import User

from almoxarifado.users.forms import UserCreationForm



class PaginaInicialSistema(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = "solicitacao/pagina_inicial.html"

    def get_context_data(self, **kwargs):
        context = super(PaginaInicialSistema, self).get_context_data(**kwargs)
        context['user_is_adm'] = self.request.user.groups.filter(name='administrativo_permissao').exists()
        return context        

#############################
## Parte do usuário inicio ##
#############################

class UsuarioCreate(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'usuario/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('listaSolicitacao')


class SolicitacaoCreate(LoginRequiredMixin, CreateView):
    model = Solicitacao
    context_object_name = 'solicitacao_list'
    template_name = 'solicitacao/solicitacao_create.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('listaSolicitacao')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['materiais'] = MateriaisFormSetUP(self.request.POST)
        else:
            context['materiais'] = MateriaisFormSetUP()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        materiais = context['materiais']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save(commit=False)
                self.object.user = self.request.user       
                self.object.almoxarifado_relacionamento = self.request.user.almoxarifado_user
                self.object.departamento_relacionamento = self.request.user.departamento_user
                self.object.save()
            if materiais.is_valid():
                materiais.instance = self.object
                materiais.save()

        return super(SolicitacaoCreate, self).form_valid(form)
 

class SolicitacaoList(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'solicitacao/solicitacao_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoList, self).get_context_data(**kwargs)
        user = self.request.user
        context['solicitacoesA'] = Solicitacao.objects.filter(status='True', user=self.request.user).order_by('-data_emissao')
        context['solicitacoesF'] = Solicitacao.objects.filter(status='False').order_by('-data_emissao')
        return context


class SolicitacaoDetail(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = 'solicitacao/solicitacao_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDetail, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context


class SolicitacaoDelete(LoginRequiredMixin, DeleteView):
    model = Solicitacao
    template_name = 'solicitacao/solicitacao_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('listaSolicitacao')

#######################################
##   Parte do Encarregado do setor   ##
#######################################


class SolicitacaoSecretarioList(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'secretario/solicitacao_sec_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoSecretarioList, self).get_context_data(**kwargs)
        user_id = self.request.user
        sec_id = user_id.secretaria_user_id
        context['solicitacoesE'] = Solicitacao.objects.filter(departamento_relacionamento__secretaria_relacionamento_id = sec_id).filter(requisicao_secretario='False')
        context['solicitacoesA'] = Solicitacao.objects.filter(departamento_relacionamento__secretaria_relacionamento_id = sec_id).filter(requisicao_secretario='True')
        return context

class SolicitacaoSecretarioDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'secretario_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'secretario/solicitacao_sec_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoSecretarioDetail, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context

class SolicitacaoSecretarioUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'secretario_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'secretario/solicitacao_sec_update.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('secretarioLista')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoSecretarioUpdate, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        # context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        if self.request.POST:
            context['materiais'] = MateriaisFormSetUPSEC(self.request.POST, instance=self.object)
        else:
            context['materiais'] = MateriaisFormSetUPSEC(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        materiais = context['materiais']
        with transaction.atomic():
            self.object = form.save()

            if materiais.is_valid():
                materiais.instance = self.object
                materiais.save()
        return super(SolicitacaoSecretarioUpdate, self).form_valid(form)

#######################################
##   Parte Administrativa do sistema ##
#######################################

class SolicitacaoAdminstrativoList(PermissionRequiredMixin, ListView):
    permission_required = 'administrativo_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_administrativo_list.html'
    

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAdminstrativoList, self).get_context_data(**kwargs)
        context['solicitacoesE'] = Solicitacao.objects.filter(status='True', requisicao_processamento='False').filter(requisicao_secretario='True').order_by('-data_emissao')
        context['solicitacoesA'] = Solicitacao.objects.filter(status='True', requisicao_processamento='True').filter(requisicao_secretario='True').order_by('-data_emissao')
        return context


class SolicitacaoAdministrativoDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'administrativo_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_administrativo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAdministrativoDetail, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context


class SolicitacaoCreateUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'administrativo_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_administrativo_update.html'
    form_class = SolicitacaoForm

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCreateUpdate, self).get_context_data(**kwargs)
        context['materiaisList'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        if self.request.POST:
            context['materiais'] = MateriaisFormSet(self.request.POST, instance=self.object)
        else:
            context['materiais'] = MateriaisFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        materiais = context['materiais']
        with transaction.atomic():
            self.object = form.save()

            if materiais.is_valid():
                materiais.instance = self.object
                materiais.save()
        return super(SolicitacaoCreateUpdate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalheAdministrativo', args=(self.object.pk,))


###########################################################
##   Parte Administrativa do sistema separação e entrega ##
###########################################################

class SolicitacaoListEntrega(PermissionRequiredMixin, ListView):
    permission_required = 'entrega_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_entrega_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoListEntrega, self).get_context_data(**kwargs)
        context["solicitacoesS"] = Solicitacao.objects.filter(status='True', requisicao_processamento='True', requisicao_recebido='False', requisicao_transito='False').order_by('-data_emissao')
        context["solicitacoesE"] = Solicitacao.objects.filter(status='True', requisicao_processamento='True', requisicao_transito='True').order_by('-data_emissao')
        context["solicitacoesF"] = Solicitacao.objects.filter(status='True', requisicao_recebido='True').order_by('-data_emissao')
        return context
    
class SolicitacaoDetailEntrega(PermissionRequiredMixin, DetailView):
    permission_required = 'entrega_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_entrega_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDetailEntrega, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context

class SolicitacaoCreateEntrega(PermissionRequiredMixin, UpdateView):
    permission_required = 'entrega_permissao'
    raise_exception = True
    model = Solicitacao
    template_name = 'administrativo/solicitacao_entrega_update.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('entregaLista')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCreateEntrega, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)        
        return context


#############################################
##   Parte Administrativa do sistema itens ##
#############################################


class MateriaisCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'administrativo_permissao'
    raise_exception = True
    model = Materiais
    context_object_name = 'material_create'
    template_name = 'administrativo/administrativo_material_create.html'
    form_class = MateriaisForm
    success_url = reverse_lazy('home')

class MateriaisList(PermissionRequiredMixin, ListView):
    permission_required = 'administrativo_permissao'
    raise_exception = True
    model = Materiais
    template_name = 'administrativo/administrativo_material_list.html'

    def get_context_data(self, **kwargs):
        context = super(MateriaisList, self).get_context_data(**kwargs)
        context["MateriaisSaude"] = Materiais.objects.filter(almoxarifado_relacionamento__descricao_almoxarifado = "Saúde" ) 
        context["MateriaisEducacao"] = Materiais.objects.filter(almoxarifado_relacionamento__descricao_almoxarifado = "Educação" )
        context["MateriaisDaes"] = Materiais.objects.filter(almoxarifado_relacionamento__descricao_almoxarifado = "DAES" )
        context["MateriaisOficina"] = Materiais.objects.filter(almoxarifado_relacionamento__descricao_almoxarifado = "Oficina" )
        context["MateriaisCozinha"] = Materiais.objects.filter(almoxarifado_relacionamento__descricao_almoxarifado = "Cozinha" )        
        return context
    

