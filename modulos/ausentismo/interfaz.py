from flask import Blueprint, flash, redirect, render_template, url_for

from core.seguridad import login_requerido, requiere_permiso
from modulos.ausentismo.servicio import ServicioAusentismo

bp = Blueprint("ausentismo", __name__, url_prefix="/ausentismo")
servicio = ServicioAusentismo()


@bp.route("/", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("ausentismo")
def panel():
    from flask import request

    if request.method == "POST":
        servicio.generar()
        flash("Reporte de ausentismo enviado a SG-SST.", "success")
        return redirect(url_for("ausentismo.panel"))
    return render_template("ausentismo.html", reportes=servicio.listar(), a_tiempo=servicio.dentro_de_plazo())
