from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey, BooleanField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from secretaria.models import (Secretaria, Almoxarifado, Departamento)

class User(AbstractUser):
    secretaria_user = ForeignKey(Secretaria, related_name="Secretaria", on_delete=False, null=True)
    departamento_user = ForeignKey(Departamento, on_delete=False, null=True)
    almoxarifado_user = ForeignKey(Almoxarifado, on_delete=False, null=True)
    
    # Nivél de permissao do usuario
    usuario_padrao = BooleanField(default=True, blank=True, null=True)
    usuario_secretario = BooleanField(default=False, blank=True, null=True)
    usuario_administrativo = BooleanField(default=False, blank=True, null=True)
    usuario_entrega = BooleanField(default=False, blank=True, null=True)

    name = CharField(_("Nome Completo"), blank=True, max_length=255, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
