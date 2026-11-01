from flask import Blueprint, render_template

from core.seguridad import login_requerido, requiere_permiso
from core.utils import formato_moneda
from modulos.liquidacion.repositorio import RepositorioLiquidacion
from modulos.liquidacion.servicio import ServicioLiquidacion

bp = Blueprint("liquidacion", __name__, url_prefix="/liquidacion")
servicio = ServicioLiquidacion()
repo = RepositorioLiquidacion()


@bp.route("/")
@login_requerido
@requiere_permiso("liquidacion")
def listar():
    return render_template("liquidacion.html", items=repo.listar(), formato_moneda=formato_moneda)


@bp.route("/<int:incapacidad_id>")
@login_requerido
@requiere_permiso("liquidacion")
def detalle(incapacidad_id):
    item, resultado = servicio.detalle(incapacidad_id)
    return render_template("liquidacion_detalle.html", item=item, resultado=resultado, formato_moneda=formato_moneda)
