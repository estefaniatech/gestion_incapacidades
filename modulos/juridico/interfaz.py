from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from core.seguridad import login_requerido, requiere_permiso
from modulos.juridico.repositorio import RepositorioJuridico
from modulos.juridico.servicio import ServicioJuridico

bp = Blueprint("juridico", __name__, url_prefix="/juridico")
servicio = ServicioJuridico()
repo = RepositorioJuridico()


@bp.route("/")
@login_requerido
@requiere_permiso("juridico")
def bandeja():
    return render_template("juridico.html", items=servicio.bandeja())


@bp.route("/<int:incapacidad_id>", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("juridico")
def detalle(incapacidad_id):
    item = repo.obtener(incapacidad_id)
    if request.method == "POST":
        if request.form.get("accion") == "decidir":
            servicio.decidir(incapacidad_id, request.form["decision"])
            flash("Decisión jurídica registrada.", "success")
        else:
            servicio.actuar(
                incapacidad_id,
                request.form["tipo_accion"],
                request.form.get("causal", ""),
                session.get("usuario"),
            )
            flash("Actuación jurídica generada.", "success")
        return redirect(url_for("juridico.detalle", incapacidad_id=incapacidad_id))
    return render_template("juridico_detalle.html", item=item, procesos=repo.procesos(incapacidad_id))
