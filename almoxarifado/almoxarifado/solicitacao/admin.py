from django.contrib import admin
from .models import (Movimentacao, Solicitacao, Unidade, Materiais,
                     Materiais_Solicitacao)


class Materiais_SolicitacaoAdmin(admin.TabularInline):
    model = Materiais_Solicitacao
    extra = 1


class SolicitacaoAdmin(admin.ModelAdmin):
    model = Solicitacao

    inlines = [
        Materiais_SolicitacaoAdmin,
    ]


admin.site.register(Movimentacao)
admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(Unidade)
admin.site.register(Materiais)
admin.site.register(Materiais_Solicitacao)