from core.database import db
from core.models import Incapacidad, NovedadNomina


class RepositorioNomina:
    def listar(self):
        return NovedadNomina.query.order_by(NovedadNomina.fecha.desc()).all()

    def por_incapacidad(self, incapacidad_id: int):
        return NovedadNomina.query.filter_by(incapacidad_id=incapacidad_id).all()

    def obtener_incapacidad(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
