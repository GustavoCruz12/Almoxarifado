from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    View,
)
from .models import * 
from .mixins import RenderPDFMixin


class Pdf(RenderPDFMixin):

    template = "pdf.html"
    params = {
        'solicitacoes': Solicitacao.objects.all(),
    }