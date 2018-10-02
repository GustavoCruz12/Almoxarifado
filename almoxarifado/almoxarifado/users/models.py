from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from secretaria.models import (Secretaria, Almoxarifado, Departamento)

class User(AbstractUser):
    secretaria_user = ForeignKey(Secretaria, related_name="Secretaria", on_delete=False)
    departamento_user = ForeignKey(Departamento, on_delete=False)
    almoxarifado_user = ForeignKey(Almoxarifado, on_delete=False)
    name = CharField(_("Nome Completo"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
