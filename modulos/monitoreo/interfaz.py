from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.seguridad import login_requerido, requiere_permiso
from modulos.monitoreo.servicio import ServicioMonitoreo

bp = Blueprint("monitoreo", __name__, url_prefix="/monitoreo")
servicio = ServicioMonitoreo()


@bp.route("/")
@login_requerido
@requiere_permiso("monitoreo")
def panel():
    return render_template("monitoreo.html", panel=servicio.panel())


@bp.route("/concepto", methods=["POST"])
@login_requerido
@requiere_permiso("monitoreo")
def concepto():
    servicio.registrar_concepto(
        int(request.form["colaborador_id"]),
        request.form["resultado"],
        request.form.get("notas", ""),
        bool(request.form.get("enviado_afp")),
    )
    flash("Concepto de rehabilitación registrado y comunicado.", "success")
    return redirect(url_for("monitoreo.panel"))


@bp.route("/alertas/concepto", methods=["POST"])
@login_requerido
@requiere_permiso("monitoreo")
def alerta_concepto():
    enviados = servicio.alertar_sin_concepto()
    flash(f"Avisos enviados: {', '.join(enviados) or 'ninguno'}.", "info")
    return redirect(url_for("monitoreo.panel"))


@bp.route("/alertas/suspension", methods=["POST"])
@login_requerido
@requiere_permiso("monitoreo")
def alerta_suspension():
    enviados = servicio.alertar_suspension()
    flash(f"Suspensión de nómina comunicada a: {', '.join(enviados) or 'nadie'}.", "info")
    return redirect(url_for("monitoreo.panel"))


@bp.route("/reintegro", methods=["POST"])
@login_requerido
@requiere_permiso("monitoreo")
def reintegro():
    servicio.reintegro(
        colaborador_id=int(request.form["colaborador_id"]),
        valor=float(request.form["valor"]),
        incapacidad_id=int(request.form["incapacidad_id"]) if request.form.get("incapacidad_id") else None,
        notas=request.form.get("notas", ""),
    )
    flash("Reintegro de EPS a trabajador registrado.", "success")
    return redirect(url_for("monitoreo.panel"))
