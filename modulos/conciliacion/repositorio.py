from core.database import db
from core.models import ConciliacionPago, Incapacidad


class RepositorioConciliacion:
    def pagadas(self):
        return Incapacidad.query.filter_by(estado="pagada").all()

    def por_periodo(self, periodo: str):
        return ConciliacionPago.query.filter_by(periodo=periodo).all()

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
