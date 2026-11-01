from flask import Blueprint, render_template

from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda
from modulos.ia.servicio import ServicioIA

bp = Blueprint("ia", __name__, url_prefix="/ia")
servicio = ServicioIA()


@bp.route("/")
@login_requerido
@requiere_permiso("ia")
def panel():
    return render_template("ia.html", analisis=servicio.analizar(), formato_moneda=formato_moneda)
