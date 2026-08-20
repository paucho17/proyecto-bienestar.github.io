import io

import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Actividad, Inscripcion


def es_personal_bienestar(user):
    return user.is_authenticated and (user.is_staff or getattr(user, "rol", None) == "BIENESTAR")


@login_required
def lista_actividades(request):
    """Consulta de actividades disponibles (funcionalidad 4)."""
    actividades = Actividad.objects.exclude(estado=Actividad.Estado.CANCELADA)
    return render(request, "actividades/lista_actividades.html", {"actividades": actividades})


@login_required
def inscribirse(request, actividad_id):
    """Inscripción de participantes en actividades (funcionalidad 5)."""
    actividad = get_object_or_404(Actividad, pk=actividad_id)

    if not actividad.tiene_cupo:
        messages.error(request, "Esta actividad ya no tiene cupos disponibles.")
        return redirect("lista_actividades")

    inscripcion, creada = Inscripcion.objects.get_or_create(
        usuario=request.user, actividad=actividad
    )
    if creada:
        messages.success(request, "Inscripción realizada. Tu código QR está disponible abajo.")
    else:
        messages.info(request, "Ya estabas inscrito en esta actividad.")

    return redirect("mi_qr", inscripcion_id=inscripcion.id)


@login_required
def mi_qr(request, inscripcion_id):
    """Muestra el código QR (identificador único) de una inscripción."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id, usuario=request.user)
    return render(request, "actividades/mi_qr.html", {"inscripcion": inscripcion})


@login_required
def imagen_qr(request, inscripcion_id):
    """Genera la imagen PNG del código QR único de la inscripción."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id, usuario=request.user)
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(str(inscripcion.codigo_qr))
    qr.make(fit=True)
    imagen = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@user_passes_test(es_personal_bienestar)
def validar_asistencia(request):
    """
    Validación MANUAL del código QR (se ingresa el código como texto).
    El escaneo por cámara queda fuera del alcance de esta entrega.
    """
    inscripcion = None
    if request.method == "POST":
        codigo = request.POST.get("codigo_qr", "").strip()
        try:
            inscripcion = Inscripcion.objects.get(codigo_qr=codigo)
            if inscripcion.asistio:
                messages.info(request, "Esta asistencia ya había sido registrada.")
            else:
                inscripcion.registrar_asistencia()
                messages.success(
                    request,
                    f"Asistencia registrada para {inscripcion.usuario} en {inscripcion.actividad}.",
                )
        except (Inscripcion.DoesNotExist, ValueError):
            messages.error(request, "Código QR inválido o no encontrado.")

    return render(request, "actividades/validar_asistencia.html", {"inscripcion": inscripcion})
