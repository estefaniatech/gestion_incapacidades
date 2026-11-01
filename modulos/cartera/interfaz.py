from flask import Blueprint, flash, redirect, render_template, session, url_for

from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda
from modulos.cartera.servicio import ServicioCartera

bp = Blueprint("cartera", __name__, url_prefix="/cartera")
servicio = ServicioCartera()


@bp.route("/")
@login_requerido
@requiere_permiso("cartera")
def panel():
    return render_template("cartera.html", panel=servicio.panel(), formato_moneda=formato_moneda)


@bp.route("/<int:incapacidad_id>/requerimiento", methods=["POST"])
@login_requerido
@requiere_permiso("cartera")
def requerimiento(incapacidad_id):
    servicio.requerimiento(incapacidad_id, session.get("usuario"))
    flash("Requerimiento de cobro persuasivo generado.", "success")
    return redirect(url_for("cartera.panel"))


@bp.route("/<int:incapacidad_id>/juridico", methods=["POST"])
@login_requerido
@requiere_permiso("cartera")
def juridico(incapacidad_id):
    try:
        servicio.trasladar_juridico(incapacidad_id)
        flash("Expediente trasladado a jurídica.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("cartera.panel"))
