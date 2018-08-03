from django.contrib import admin
from .models import (Secretaria, Departamento, Almoxarifado)

# class SecretariaInlineAdmin(admin.StackedInline):
#     model = Secretaria
#     extra = 1
#     can_delete = True

#     def get_extra (self, request, obj=None, **kwargs):
#         if obj:
#             return 0
#         return self.extra

# class SolicitacaoAdmin(admin.ModelAdmin):
#     inlines = [
#         SecretariaInlineAdmin,
#     ]

admin.site.register(Secretaria)
admin.site.register(Departamento)
admin.site.register(Almoxarifado)