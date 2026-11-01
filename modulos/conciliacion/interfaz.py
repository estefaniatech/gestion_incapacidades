from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda, periodo_aaaa_mm
from modulos.conciliacion.repositorio import RepositorioConciliacion
from modulos.conciliacion.servicio import ServicioConciliacion

bp = Blueprint("conciliacion", __name__, url_prefix="/conciliacion")
servicio = ServicioConciliacion()
repo = RepositorioConciliacion()


@bp.route("/", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("conciliacion")
def panel():
    if request.method == "POST":
        servicio.registrar_pago_entidad(
            int(request.form["incapacidad_id"]) if request.form.get("incapacidad_id") else None,
            request.form.get("entidad", ""),
            float(request.form.get("valor") or 0),
            request.form.get("periodo") or periodo_aaaa_mm(),
            request.form.get("notas", ""),
        )
        flash("Movimiento de conciliación registrado.", "success")
        return redirect(url_for("conciliacion.panel"))
    periodo, filas = servicio.listar(request.args.get("periodo"))
    return render_template(
        "conciliacion.html",
        periodo=periodo,
        filas=filas,
        pagadas=repo.pagadas(),
        formato_moneda=formato_moneda,
    )
