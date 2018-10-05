from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from almoxarifado.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",
                                    "secretaria_user",
                                    "departamento_user",
                                    "almoxarifado_user",
                                    "usuario_padrao",
                                    "usuario_secretario",
                                    "usuario_administrativo",
                                    "usuario_entrega",
                                    )}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser", "secretaria_user"]
    search_fields = ["name"]
