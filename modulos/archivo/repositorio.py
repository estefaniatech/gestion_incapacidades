from core.database import db
from core.models import ArchivoFisico, DocumentoIncapacidad, Incapacidad


class RepositorioArchivo:
    def pagadas(self):
        return Incapacidad.query.filter(Incapacidad.estado.in_(["pagada", "archivada"])).all()

    def por_incapacidad(self, incapacidad_id: int):
        return ArchivoFisico.query.filter_by(incapacidad_id=incapacidad_id).first()

    def documentos(self, incapacidad_id: int):
        return DocumentoIncapacidad.query.filter_by(incapacidad_id=incapacidad_id).all()

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
