from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    SECRETARIA_CHOICES = (
        ('SAUDE', 'Saúde'),
        ('EDUCACAO', 'Educação'),
        ('FINANCA_ADMINISTRCAO', 'Finanças e Administração'),
        ('ESPORT_CULT_TURI', 'Esporte Cultura e Turismo'),
        ('ASSISTENCIA_SOCIAL', 'Assitência Social'),
        ('INFRA', 'Infra Estrutura'),
    )
    secretaria_user = CharField('Secretaria do Usuário', max_length=255, choices=SECRETARIA_CHOICES, blank=True, null=True)
    PROFILE_CHOICES = (
        ('USUARIO_COMUM', 'Usuário Comum'),
        ('USUARIO_ADMINISTRATIVO', 'Usuário Administrativo'),
        ('USUARIO_SECRETARIO', 'Usuário Secretario'),
    )
    profile_user = CharField('Profile de Usuário', max_length=255, choices=PROFILE_CHOICES, blank=True, null=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
