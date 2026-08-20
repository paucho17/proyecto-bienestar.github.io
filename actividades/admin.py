from django.contrib import admin

from .models import Actividad, Inscripcion


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ("codigo_qr", "fecha_inscripcion", "fecha_validacion_asistencia")
    fields = (
        "usuario",
        "estado",
        "codigo_qr",
        "asistio",
        "fecha_validacion_asistencia",
    )


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "fecha",
        "hora_inicio",
        "lugar",
        "cupo_maximo",
        "cupos_disponibles",
        "estado",
        "responsable",
    )
    list_filter = ("estado", "fecha")
    search_fields = ("nombre", "lugar", "descripcion")
    date_hierarchy = "fecha"
    inlines = [InscripcionInline]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "actividad",
        "estado",
        "codigo_qr",
        "asistio",
        "fecha_inscripcion",
    )
    list_filter = ("estado", "asistio", "actividad")
    search_fields = (
        "usuario__username",
        "usuario__numero_documento",
        "actividad__nombre",
        "codigo_qr",
    )
    readonly_fields = ("codigo_qr", "fecha_inscripcion", "fecha_validacion_asistencia")
    actions = ["marcar_asistencia"]

    @admin.action(description="Registrar asistencia (validación manual de QR)")
    def marcar_asistencia(self, request, queryset):
        for inscripcion in queryset:
            inscripcion.registrar_asistencia()
        self.message_user(request, f"Asistencia registrada para {queryset.count()} inscripción(es).")
