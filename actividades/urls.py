from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_actividades, name="lista_actividades"),
    path("<int:actividad_id>/inscribirse/", views.inscribirse, name="inscribirse"),
    path("inscripcion/<int:inscripcion_id>/qr/", views.mi_qr, name="mi_qr"),
    path("inscripcion/<int:inscripcion_id>/qr/imagen/", views.imagen_qr, name="imagen_qr"),
    path("validar-asistencia/", views.validar_asistencia, name="validar_asistencia"),
]
