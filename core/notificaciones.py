"""Envío de avisos al colaborador, jefe, EPS, SG-SST y áreas internas.

Cada correo se registra en la bandeja interna (base de datos) y, si hay un
servidor SMTP configurado (ver config/settings.py), también se envía de verdad,
con adjuntos opcionales.
"""

import logging
import mimetypes
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from config import settings
from config.settings import PLANTILLAS_DIR
from core.database import db
from core.models import Notificacion


def cargar_plantilla(nombre: str, **campos) -> str:
    ruta = PLANTILLAS_DIR / nombre
    texto = ruta.read_text(encoding="utf-8") if ruta.exists() else ""
    for clave, valor in campos.items():
        texto = texto.replace("{{" + clave + "}}", str(valor))
    return texto


def _enviar_smtp(destinatario: str, asunto: str, cuerpo: str, adjuntos: list) -> None:
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = settings.SMTP_REMITENTE
    msg["To"] = destinatario
    msg.set_content(cuerpo)

    for adjunto in adjuntos:
        if isinstance(adjunto, (str, Path)):
            ruta = Path(adjunto)
            datos, nombre = ruta.read_bytes(), ruta.name
        else:  # (nombre, bytes) para archivos generados en memoria
            nombre, datos = adjunto
        tipo, _ = mimetypes.guess_type(nombre)
        principal, _, sub = (tipo or "application/octet-stream").partition("/")
        msg.add_attachment(datos, maintype=principal, subtype=sub, filename=nombre)

    if settings.SMTP_PORT == 465:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, 465, context=ssl.create_default_context(), timeout=20) as smtp:
            smtp.login(settings.SMTP_USUARIO, settings.SMTP_CLAVE)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(settings.SMTP_USUARIO, settings.SMTP_CLAVE)
            smtp.send_message(msg)


def enviar(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    incapacidad_id: int | None = None,
    canal: str = "correo",
    adjuntos: list | None = None,
):
    """Registra el aviso y, si hay SMTP y un correo válido, lo envía.

    `adjuntos`: rutas de archivo o tuplas (nombre, bytes).
    Un fallo de envío no interrumpe el flujo del procedimiento.
    """
    adjuntos = adjuntos or []
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

    if canal == "correo" and settings.SMTP_HOST and "@" in destinatario:
        try:
            _enviar_smtp(destinatario, asunto, cuerpo, adjuntos)
        except Exception:
            logging.getLogger(__name__).exception("No se pudo enviar el correo a %s", destinatario)
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