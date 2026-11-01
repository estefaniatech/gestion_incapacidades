from core.database import db
from core.models import GestionCobro, Incapacidad


class RepositorioCobro:
    def transcritas(self):
        return Incapacidad.query.filter(
            Incapacidad.estado.in_(["transcrita", "cobrada", "rechazada"])
        ).all()

    def obtener(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def gestiones(self, incapacidad_id: int):
        return GestionCobro.query.filter_by(incapacidad_id=incapacidad_id).order_by(GestionCobro.fecha.desc()).all()

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
