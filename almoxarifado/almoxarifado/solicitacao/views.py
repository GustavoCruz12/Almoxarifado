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

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (Solicitacao, Materiais_Solicitacao)

from .render import Render

from .forms import (SolicitacaoForm, MateriaisFormSet, MateriaisFormSetUP)

from secretaria.models import Almoxarifado

from almoxarifado.users.models import User



#############################
## Parte do usuário inicio ##
#############################

class SolicitacaoCreate(LoginRequiredMixin, CreateView):
    model = Solicitacao
    context_object_name = 'solicitacao_list'
    template_name = 'solicitacao/solicitacao_create.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super(SolicitacaoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['materiais'] = MateriaisFormSet(self.request.POST,)
        else:
            data['materiais'] = MateriaisFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        materiais = context['materiais']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                self.object.user = self.request.user
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
    template_name = 'solicitacao/solicitacao_sec_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoSecretarioList, self).get_context_data(**kwargs)
        
        return context



#######################################
##   Parte Administrativa do sistema ##
#######################################


class SolicitacaoAdminstrativoList(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'administrativo/solicitacao_administrativo_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAdminstrativoList, self).get_context_data(**kwargs)
        context['solicitacoesE'] = Solicitacao.objects.filter(status='True', requisicao_processamento='False').order_by('-data_emissao')
        context['solicitacoesA'] = Solicitacao.objects.filter(status='True', requisicao_processamento='True').order_by('-data_emissao')
        return context


class SolicitacaoAdministrativoDetail(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = 'administrativo/solicitacao_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoAdministrativoDetail, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context


class SolicitacaoCreateUpdate(LoginRequiredMixin, UpdateView):
    model = Solicitacao
    template_name = 'administrativo/solicitacao_update.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('listaAdministrativo')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCreateUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['materiais'] = MateriaisFormSetUP(self.request.POST, instance=self.object)
        else:
            context['materiais'] = MateriaisFormSetUP(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        materiais = context['materiais']
        with transaction.atomic():
           self.object = form.save()
           if materiais.is_valid():
               materiais.intance = self.object
               materiais.save()
        return super (SolicitacaoCreateUpdate, self).form_valid(form)

###########################################################
##   Parte Administrativa do sistema separação e entrega ##
###########################################################

class SolicitacaoListEntrega(LoginRequiredMixin, ListView):
    model = Solicitacao
    template_name = 'administrativo/solicitacao_entrega_list.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoListEntrega, self).get_context_data(**kwargs)
        context["solicitacoesS"] = Solicitacao.objects.filter(status='True', requisicao_processamento='True', requisicao_recebido='False', requisicao_transito='False').order_by('-data_emissao')
        context["solicitacoesE"] = Solicitacao.objects.filter(status='True', requisicao_processamento='True', requisicao_transito='True')
        context["solicitacoesF"] = Solicitacao.objects.filter(status='True', requisicao_recebido='True').order_by('-data_emissao')
        return context
    
class SolicitacaoDetailEntrega(LoginRequiredMixin, DetailView):
    model = Solicitacao
    template_name = 'administrativo/solicitacao_entrega.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoDetailEntrega, self).get_context_data(**kwargs)
        context['solicitacoes'] = Solicitacao.objects.all()
        context['materiais'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context

class SolicitacaoCreateEntrega(LoginRequiredMixin, UpdateView):
    model = Solicitacao
    template_name = 'administrativo/entrega_update.html'
    form_class = SolicitacaoForm
    success_url = reverse_lazy('entregaLista')

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoCreateEntrega, self).get_context_data(**kwargs)
        context['materiaisList'] = Materiais_Solicitacao.objects.all().filter(relacionamento_solicitacao_id=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        with transaction.atomic():
           self.object = form.save()
        return super (SolicitacaoCreateEntrega, self).form_valid(form)

class PdfRequisicao(View):
    
    def get(self, request):
        solicitacoes = Solicitacao.objects.all()
        materiais = Materiais_Solicitacao.objects.all()
        params = {
            'solicitacao': solicitacoes,
            'materiais': materiais,
            'request': request
        }
        return Render.render('pdf.html', params)