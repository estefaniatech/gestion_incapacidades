from core.database import db
from core.models import Incapacidad


class RepositorioTranscripcion:
    def pendientes(self):
        return Incapacidad.query.filter(
            Incapacidad.estado.in_(["documentacion_completa", "rechazada"])
        ).order_by(Incapacidad.fecha_inicio).all()

    def obtener(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
