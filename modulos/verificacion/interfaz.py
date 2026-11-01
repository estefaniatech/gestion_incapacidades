from flask import Blueprint, flash, redirect, render_template, request, url_for

from core.seguridad import enmascarar_diagnostico, login_requerido, requiere_permiso, rol_actual
from modulos.verificacion.repositorio import RepositorioVerificacion
from modulos.verificacion.servicio import ServicioVerificacion

bp = Blueprint("verificacion", __name__, url_prefix="/verificacion")
servicio = ServicioVerificacion()
repo = RepositorioVerificacion()


@bp.route("/<int:incapacidad_id>", methods=["GET", "POST"])
@login_requerido
@requiere_permiso("verificacion")
def detalle(incapacidad_id):
    item = repo.obtener(incapacidad_id)
    if request.method == "POST":
        if request.form.get("accion") == "adjuntar":
            archivo = request.files.get("archivo")
            doc_id = int(request.form["documento_id"])
            if archivo and archivo.filename:
                servicio.adjuntar(doc_id, archivo)
            else:
                servicio.marcar_sin_archivo(doc_id)
            flash("Documento marcado como recibido.", "success")
        elif request.form.get("accion") == "evaluar":
            resultado = servicio.evaluar(incapacidad_id)
            if resultado["completa"]:
                flash("Documentación completa. Puede transcribir.", "success")
            elif resultado["citar_coordinacion"]:
                flash("Segundo llamado: citar al colaborador con Coordinación de Administración de Personal.", "warning")
            else:
                flash(f"Faltan: {', '.join(resultado['faltantes'])}. Plazo: 3 días hábiles.", "warning")
        return redirect(url_for("verificacion.detalle", incapacidad_id=incapacidad_id))

    item.diagnostico_visible = enmascarar_diagnostico(item.diagnostico, rol_actual())
    return render_template("verificacion.html", item=item, docs=servicio.checklist(incapacidad_id))
