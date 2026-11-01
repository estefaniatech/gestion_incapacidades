from core.database import db
from core.models import Incapacidad, ProcesoJuridico


class RepositorioJuridico:
    def bandeja(self):
        return Incapacidad.query.filter(Incapacidad.estado.in_(["en_juridico", "rechazada"])).all()

    def obtener(self, incapacidad_id: int):
        return Incapacidad.query.get(incapacidad_id)

    def procesos(self, incapacidad_id: int):
        return ProcesoJuridico.query.filter_by(incapacidad_id=incapacidad_id).all()

    def guardar(self, item):
        db.session.add(item)
        db.session.commit()
        return item
