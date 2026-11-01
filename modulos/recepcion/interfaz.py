from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from config.estados import TipoIncapacidad
from config.settings import CANALES_RECEPCION
from core.seguridad import login_requerido, requiere_permiso
from modulos.recepcion.repositorio import RepositorioRecepcion
from modulos.recepcion.servicio import ServicioRecepcion

bp = Blueprint("recepcion", __name__, url_prefix="/recepcion")
servicio = ServicioRecepcion()
repo = RepositorioRecepcion()


@bp.route("/")
@login_requerido
@requiere_permiso("recepcion")
def listar():
    return render_template("recepcion_lista.html", items=servicio.listar())


@bp.route("/nueva", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("recepcion")
def nueva():
    if request.method == "POST":
        try:
            incapacidad = servicio.registrar(request.form.to_dict(), session.get("usuario"))
            flash(f"Incapacidad #{incapacidad.id} recibida. Verifique la documentación.", "success")
            return redirect(url_for("verificacion.detalle", incapacidad_id=incapacidad.id))
        except Exception as exc:
            flash(str(exc), "danger")
    return render_template(
        "recepcion_form.html",
        tipos=list(TipoIncapacidad),
        canales=CANALES_RECEPCION,
        colaboradores=repo.listar_colaboradores(),
    )
