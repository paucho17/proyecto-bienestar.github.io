import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Actividad(models.Model):
    """Actividad de Bienestar Universitario (funcionalidad 2 del alcance)."""

    class Estado(models.TextChoices):
        PROGRAMADA = "PROGRAMADA", "Programada"
        EN_CURSO = "EN_CURSO", "En curso"
        FINALIZADA = "FINALIZADA", "Finalizada"
        CANCELADA = "CANCELADA", "Cancelada"

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    lugar = models.CharField(max_length=200)
    cupo_maximo = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=15, choices=Estado.choices, default=Estado.PROGRAMADA
    )
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actividades_a_cargo",
        limit_choices_to={"rol": "BIENESTAR"},
        help_text="Personal de Bienestar responsable de la actividad.",
    )
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ["-fecha", "hora_inicio"]

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"

    @property
    def cupos_disponibles(self):
        inscritos = self.inscripciones.filter(
            estado__in=[Inscripcion.Estado.CONFIRMADA]
        ).count()
        return max(self.cupo_maximo - inscritos, 0)

    @property
    def tiene_cupo(self):
        return self.cupos_disponibles > 0


class Inscripcion(models.Model):
    """
    Relación usuario-actividad. Guarda también el código QR único del
    usuario para la actividad y el registro de asistencia (funcionalidades
    3, 4 y 5 del alcance). El QR se valida MANUALMENTE en esta entrega
    (ingresando el código), según lo definido en el análisis de viabilidad.
    """

    class Estado(models.TextChoices):
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        CANCELADA = "CANCELADA", "Cancelada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inscripciones"
    )
    actividad = models.ForeignKey(
        Actividad, on_delete=models.CASCADE, related_name="inscripciones"
    )
    # Se guarda como texto (CHAR) en vez de usar el tipo nativo UUID de la
    # base de datos: ese tipo solo existe en MariaDB 10.7+ y no en MySQL
    # estándar, lo que rompía la importación en XAMPP. Como CharField es
    # compatible con cualquier versión de MySQL/MariaDB.
    codigo_qr = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, unique=True
    )
    estado = models.CharField(
        max_length=12, choices=Estado.choices, default=Estado.CONFIRMADA
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    asistio = models.BooleanField(default=False)
    fecha_validacion_asistencia = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "actividad"], name="unica_inscripcion_por_usuario_actividad"
            )
        ]

    def __str__(self):
        return f"{self.usuario} -> {self.actividad}"

    def clean(self):
        if self.estado == self.Estado.CONFIRMADA and not self.pk:
            if not self.actividad.tiene_cupo:
                raise ValidationError("La actividad ya no tiene cupos disponibles.")

    def registrar_asistencia(self):
        """Validación manual del código QR: marca asistencia."""
        from django.utils import timezone

        self.asistio = True
        self.fecha_validacion_asistencia = timezone.now()
        self.save(update_fields=["asistio", "fecha_validacion_asistencia"])
