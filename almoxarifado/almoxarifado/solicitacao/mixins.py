
from django.views.generic.base import View
from django.http import HttpResponse
from .render import Render


class RenderPDF(Render):

    params: dict = None
    template: str = None
    email: bool = False
    to: str = None


class RenderPDFMixin(RenderPDF, View):

    def get(self, request, *args, **kwargs):
        if self.email is False:
            ### always add request object ###
            self.params['request'] = request
            return Render.render(self.template, self.params)
        else:
            ### process email ####
            return HttpResponse("Email")