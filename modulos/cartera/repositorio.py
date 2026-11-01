from datetime import date, timedelta

from core.database import db
from core.models import Incapacidad, RequerimientoCartera


class RepositorioCartera:
    def candidatas(self):
        limite = date.today() - timedelta(days=180)
        return Incapacidad.query.filter(
            Incapacidad.estado.in_(["cobrada", "transcrita"]),
            Incapacidad.fecha_transcripcion != None,  # noqa: E711
            Incapacidad.fecha_transcripcion <= limite,
        ).all()

    def pendientes_pago(self):
        return Incapacidad.query.filter(Incapacidad.estado.in_(["cobrada", "en_cartera"])).all()

    def requerimientos(self, incapacidad_id: int):
        return RequerimientoCartera.query.filter_by(incapacidad_id=incapacidad_id).all()

    def obtener(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
