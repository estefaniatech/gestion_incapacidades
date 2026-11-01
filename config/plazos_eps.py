"""Plazos de transcripción por entidad (numeral 5.2.1)."""

from datetime import date, timedelta

from config.estados import TipoIncapacidad

PLAZO_PATERNIDAD_DIAS = 30

PLAZOS_TRANSCRIPCION = {
    "SALUD TOTAL": {"unidad": "meses", "cantidad": 12, "accidente_transito_dias": 15},
    "NUEVA EPS": {"unidad": "meses", "cantidad": 12},
    "SOS": {"unidad": "meses", "cantidad": 12, "canal": "correo"},
    "SANITAS": {"unidad": "años", "cantidad": 3, "canal": "correo"},
    "FAMISANAR": {"unidad": "meses", "cantidad": 12, "canal": "correo"},
    "SURA EPS": {"unidad": "dias", "cantidad": 150},
    "ASMET SALUD": {"unidad": "meses", "cantidad": 12},
    "ARL SURA": {"unidad": "meses", "cantidad": 12},
}

ALIAS_ENTIDAD = {
    "salud total": "SALUD TOTAL",
    "nueva eps": "NUEVA EPS",
    "sos": "SOS",
    "sanitas": "SANITAS",
    "famisanar": "FAMISANAR",
    "sura": "SURA EPS",
    "sura eps": "SURA EPS",
    "asmet": "ASMET SALUD",
    "asmet salud": "ASMET SALUD",
    "arl sura": "ARL SURA",
}


def normalizar_entidad(nombre: str) -> str:
    clave = (nombre or "").strip().lower()
    return ALIAS_ENTIDAD.get(clave, (nombre or "").strip().upper())


def _sumar_plazo(inicio: date, regla: dict) -> date:
    unidad = regla["unidad"]
    cantidad = regla["cantidad"]
    if unidad == "dias":
        return inicio + timedelta(days=cantidad)
    if unidad == "meses":
        return inicio + timedelta(days=cantidad * 30)
    if unidad == "años":
        return inicio + timedelta(days=cantidad * 365)
    return inicio


def fecha_limite_transcripcion(
    entidad: str,
    fecha_inicio: date,
    tipo: str,
    fecha_nacimiento: date | None = None,
) -> date | None:
    if tipo == TipoIncapacidad.LICENCIA_PATERNIDAD.value:
        base = fecha_nacimiento or fecha_inicio
        return base + timedelta(days=PLAZO_PATERNIDAD_DIAS)

    clave = normalizar_entidad(entidad)
    regla = PLAZOS_TRANSCRIPCION.get(clave)
    if not regla:
        return None

    if tipo == TipoIncapacidad.ACCIDENTE_TRANSITO.value and regla.get("accidente_transito_dias"):
        return fecha_inicio + timedelta(days=regla["accidente_transito_dias"])

    return _sumar_plazo(fecha_inicio, regla)


def canal_transcripcion(entidad: str) -> str:
    clave = normalizar_entidad(entidad)
    regla = PLAZOS_TRANSCRIPCION.get(clave, {})
    return regla.get("canal", "portal")
