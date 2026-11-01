from datetime import datetime

from core.database import db
from core.models import DocumentoIncapacidad, Incapacidad


class RepositorioVerificacion:
    def obtener(self, incapacidad_id: int) -> Incapacidad | None:
        return Incapacidad.query.get(incapacidad_id)

    def documentos(self, incapacidad_id: int):
        return DocumentoIncapacidad.query.filter_by(incapacidad_id=incapacidad_id).all()

    def crear_documento(self, datos: dict):
        fila = DocumentoIncapacidad(**datos)
        db.session.add(fila)
        db.session.commit()
        return fila

    def marcar_recibido(self, documento_id: int, ruta: str | None):
        doc = DocumentoIncapacidad.query.get(documento_id)
        doc.recibido = True
        doc.ruta_archivo = ruta
        doc.fecha_recepcion = datetime.utcnow()
        db.session.commit()
        return doc

    def guardar(self, incapacidad: Incapacidad):
        db.session.add(incapacidad)
        db.session.commit()
        return incapacidad
