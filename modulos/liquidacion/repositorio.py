from core.database import db
from core.models import Incapacidad


class RepositorioLiquidacion:
    def obtener(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def listar(self):
        return Incapacidad.query.order_by(Incapacidad.fecha_inicio.desc()).all()

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
