from core.database import db
from core.models import Incapacidad, ReporteAusentismo


class RepositorioAusentismo:
    def del_periodo(self, periodo: str):
        return [i for i in Incapacidad.query.all() if i.fecha_inicio.strftime("%Y-%m") == periodo]

    def guardar_reporte(self, fila):
        db.session.add(fila)
        db.session.commit()
        return fila

    def reportes(self):
        return ReporteAusentismo.query.order_by(ReporteAusentismo.generado_en.desc()).all()
