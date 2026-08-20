from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario del sistema de Bienestar Universitario.
    Extiende AbstractUser para reutilizar el sistema de autenticación
    y permisos de Django (login, sesiones, panel admin).
    """

    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cédula de ciudadanía"
        TI = "TI", "Tarjeta de identidad"
        CE = "CE", "Cédula de extranjería"
        PA = "PA", "Pasaporte"

    class Rol(models.TextChoices):
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"
        DOCENTE = "DOCENTE", "Docente"
        FUNCIONARIO = "FUNCIONARIO", "Funcionario"
        CONTRATISTA = "CONTRATISTA", "Contratista"
        BIENESTAR = "BIENESTAR", "Personal de Bienestar Universitario"

    tipo_documento = models.CharField(
        max_length=2, choices=TipoDocumento.choices, default=TipoDocumento.CC
    )
    numero_documento = models.CharField(max_length=20, unique=True)
    correo_institucional = models.EmailField(unique=True)
    programa_o_dependencia = models.CharField(max_length=150)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ESTUDIANTE)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    @property
    def es_personal_bienestar(self):
        return self.rol == self.Rol.BIENESTAR or self.is_staff
