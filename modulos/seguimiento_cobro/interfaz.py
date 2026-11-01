from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from config.estados import ESTADOS_COBRO, EstadoIncapacidad
from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda
from modulos.seguimiento_cobro.repositorio import RepositorioCobro
from modulos.seguimiento_cobro.servicio import ServicioCobro

bp = Blueprint("cobro", __name__, url_prefix="/cobro")
servicio = ServicioCobro()
repo = RepositorioCobro()


@bp.route("/")
@login_requerido
@requiere_permiso("cobro")
def bandeja():
    return render_template(
        "cobro.html",
        items=servicio.bandeja(),
        estados=ESTADOS_COBRO,
        formato_moneda=formato_moneda,
    )


@bp.route("/<int:incapacidad_id>", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("cobro")
def detalle(incapacidad_id):
    item = repo.obtener(incapacidad_id)
    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "estado":
            servicio.cambiar_estado(incapacidad_id, request.form["estado"], request.form.to_dict(), session.get("usuario"))
            flash("Estado de cobro actualizado.", "success")
        else:
            servicio.registrar_gestion(
                incapacidad_id,
                request.form.get("canal", "portal"),
                request.form.get("resultado", ""),
                session.get("usuario"),
                request.form.get("evidencia", ""),
            )
            flash("Gestión de cobro registrada.", "success")
        return redirect(url_for("cobro.detalle", incapacidad_id=incapacidad_id))
    return render_template(
        "cobro_detalle.html",
        item=item,
        gestiones=repo.gestiones(incapacidad_id),
        estados=[EstadoIncapacidad.TRANSCRITA, EstadoIncapacidad.COBRADA, EstadoIncapacidad.RECHAZADA, EstadoIncapacidad.PAGADA],
        formato_moneda=formato_moneda,
    )
