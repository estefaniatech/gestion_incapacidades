"""Registro de quién consultó o modificó información, especialmente datos de salud."""

from datetime import datetime

from core.database import db
from core.models import Auditoria
from core.seguridad import usuario_actual


def registrar(accion: str, entidad: str, entidad_id: int | None = None, detalle: str = "", dato_salud: bool = False):
    fila = Auditoria(
        usuario=usuario_actual() or "sistema",
        accion=accion,
        entidad=entidad,
        entidad_id=entidad_id,
        detalle=detalle,
        contiene_dato_salud=dato_salud,
        creado_en=datetime.utcnow(),
    )
    db.session.add(fila)
    db.session.commit()
    return fila
