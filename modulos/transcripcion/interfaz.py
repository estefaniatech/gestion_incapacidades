from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.seguridad import login_requerido, requiere_permiso
from modulos.transcripcion.servicio import ServicioTranscripcion

bp = Blueprint("transcripcion", __name__, url_prefix="/transcripcion")
servicio = ServicioTranscripcion()


@bp.route("/")
@login_requerido
@requiere_permiso("transcripcion")
def listar():
    return render_template("transcripcion.html", items=servicio.pendientes())


@bp.route("/<int:incapacidad_id>/radicar", methods=["POST"])
@login_requerido
@requiere_permiso("transcripcion")
def radicar(incapacidad_id):
    try:
        servicio.radicar(incapacidad_id, request.form["numero_radicado"])
        flash("Incapacidad transcrita / radicada.", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("transcripcion.listar"))
