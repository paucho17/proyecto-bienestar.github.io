from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Panel administrativo para el CRUD de usuarios.
    Cubre el requerimiento 'Gestión de usuarios (CRUD desde panel
    administrativo)' identificado como complejidad baja / viabilidad alta.
    """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "numero_documento",
        "correo_institucional",
        "rol",
        "programa_o_dependencia",
        "is_active",
    )
    list_filter = ("rol", "tipo_documento", "is_active", "is_staff")
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "numero_documento",
        "correo_institucional",
    )
    ordering = ("last_name", "first_name")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Información institucional",
            {
                "fields": (
                    "tipo_documento",
                    "numero_documento",
                    "correo_institucional",
                    "programa_o_dependencia",
                    "rol",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Información institucional",
            {
                "fields": (
                    "tipo_documento",
                    "numero_documento",
                    "correo_institucional",
                    "programa_o_dependencia",
                    "rol",
                )
            },
        ),
    )
