"""Envío de avisos al colaborador, jefe, EPS, SG-SST y áreas internas.

En este entorno los correos se registran en base de datos (bandeja interna).
"""

from datetime import datetime
from pathlib import Path

from config.settings import PLANTILLAS_DIR
from core.database import db
from core.models import Notificacion


def cargar_plantilla(nombre: str, **campos) -> str:
    ruta = PLANTILLAS_DIR / nombre
    texto = ruta.read_text(encoding="utf-8") if ruta.exists() else ""
    for clave, valor in campos.items():
        texto = texto.replace("{{" + clave + "}}", str(valor))
    return texto


def enviar(destinatario: str, asunto: str, cuerpo: str, incapacidad_id: int | None = None, canal: str = "correo"):
    nota = Notificacion(
        incapacidad_id=incapacidad_id,
        destinatario=destinatario,
        asunto=asunto,
        cuerpo=cuerpo,
        canal=canal,
        enviada_en=datetime.utcnow(),
    )
    db.session.add(nota)
    db.session.commit()
    return nota


def aviso_documentacion_faltante(colaborador, faltantes: list[str], incapacidad_id: int, llamado: int):
    cuerpo = cargar_plantilla(
        "aviso_documentacion_faltante.txt",
        colaborador=colaborador.nombre_completo,
        faltantes=", ".join(faltantes),
        llamado=str(llamado),
        dias="3",
    )
    asunto = f"Documentación faltante de incapacidad (llamado {llamado})"
    enviar(colaborador.email or colaborador.nombre_completo, asunto, cuerpo, incapacidad_id)
    if colaborador.email_jefe:
        enviar(colaborador.email_jefe, asunto, cuerpo, incapacidad_id)


def aviso_jefe_reemplazo(colaborador, incapacidad):
    cuerpo = (
        f"El colaborador {colaborador.nombre_completo} reportó una incapacidad "
        f"del {incapacidad.fecha_inicio} al {incapacidad.fecha_fin} ({incapacidad.dias} días). "
        "Debe gestionar el reemplazo para garantizar la continuidad."
    )
    dest = colaborador.email_jefe or colaborador.nombre_jefe or "jefe"
    enviar(dest, "Aviso de incapacidad y reemplazo", cuerpo, incapacidad.id)
