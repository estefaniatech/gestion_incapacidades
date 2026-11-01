"""Roles y protección de datos de salud (historia clínica / diagnóstico)."""

from functools import wraps

from flask import abort, flash, redirect, session, url_for

from config.estados import Rol

ROLES_DATOS_SALUD = {
    Rol.ADMIN.value,
    Rol.AUXILIAR_GH.value,
    Rol.SG_SST.value,
}

ROLES_GESTION = {
    Rol.ADMIN.value,
    Rol.AUXILIAR_GH.value,
    Rol.RECEPCIONISTA.value,
}

PERMISOS = {
    "recepcion": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value, Rol.RECEPCIONISTA.value, Rol.LIDER.value, Rol.COLABORADOR.value},
    "verificacion": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
    "transcripcion": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
    "liquidacion": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value, Rol.TESORERIA.value},
    "monitoreo": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value, Rol.SG_SST.value},
    "cobro": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
    "cartera": {Rol.ADMIN.value, Rol.CARTERA.value, Rol.AUXILIAR_GH.value},
    "juridico": {Rol.ADMIN.value, Rol.JURIDICO.value},
    "conciliacion": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value, Rol.CONTABILIDAD.value, Rol.TESORERIA.value},
    "nomina": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
    "ausentismo": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value, Rol.SG_SST.value},
    "archivo": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
    "ia": {Rol.ADMIN.value, Rol.AUXILIAR_GH.value},
}


def usuario_actual():
    return session.get("usuario")


def rol_actual():
    return session.get("rol")


def login_requerido(vista):
    @wraps(vista)
    def _decorada(*args, **kwargs):
        if not session.get("usuario"):
            flash("Debe iniciar sesión.", "warning")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return _decorada


def requiere_permiso(modulo: str):
    def decorador(vista):
        @wraps(vista)
        def _decorada(*args, **kwargs):
            if not session.get("usuario"):
                flash("Debe iniciar sesión.", "warning")
                return redirect(url_for("login"))
            permitidos = PERMISOS.get(modulo, set())
            if session.get("rol") not in permitidos and session.get("rol") != Rol.ADMIN.value:
                abort(403)
            return vista(*args, **kwargs)

        return _decorada

    return decorador


def puede_ver_diagnostico(rol: str | None = None) -> bool:
    rol = rol or rol_actual()
    return rol in ROLES_DATOS_SALUD


def enmascarar_diagnostico(texto: str | None, rol: str | None = None) -> str:
    if not texto:
        return ""
    if puede_ver_diagnostico(rol):
        return texto
    return "[dato de salud restringido]"
