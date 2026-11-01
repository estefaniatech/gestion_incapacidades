from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.seguridad import login_requerido, requiere_permiso
from modulos.archivo.repositorio import RepositorioArchivo
from modulos.archivo.servicio import ServicioArchivo

bp = Blueprint("archivo", __name__, url_prefix="/archivo")
servicio = ServicioArchivo()
repo = RepositorioArchivo()


@bp.route("/", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("archivo")
def panel():
    if request.method == "POST":
        iid = int(request.form["incapacidad_id"])
        if request.form.get("accion") == "destruir":
            servicio.destruir_epicrisis(iid)
            flash("Epicrisis marcada para destrucción. No reposa en el archivo.", "warning")
        else:
            servicio.archivar(iid, request.form.get("ubicacion", "Estante general"))
            flash("Enviada a gestión documental.", "success")
        return redirect(url_for("archivo.panel"))
    return render_template("archivo.html", items=repo.pagadas())
