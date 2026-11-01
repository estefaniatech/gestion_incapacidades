from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.models import Incapacidad
from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda
from modulos.nomina.servicio import ServicioNomina

bp = Blueprint("nomina", __name__, url_prefix="/nomina")
servicio = ServicioNomina()


@bp.route("/", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("nomina")
def panel():
    if request.method == "POST":
        servicio.generar(int(request.form["incapacidad_id"]))
        flash("Novedad de nómina generada.", "success")
        return redirect(url_for("nomina.panel"))
    return render_template(
        "nomina.html",
        novedades=servicio.listar(),
        incapacidades=Incapacidad.query.all(),
        formato_moneda=formato_moneda,
    )
