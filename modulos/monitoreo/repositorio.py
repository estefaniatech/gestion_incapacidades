from core.database import db
from core.models import Colaborador, ConceptoRehabilitacion, Incapacidad, ReintegroEPS


class RepositorioMonitoreo:
    def incapacidades(self):
        return Incapacidad.query.all()

    def colaboradores(self):
        return Colaborador.query.filter_by(activo=True).all()

    def concepto(self, colaborador_id: int):
        return (
            ConceptoRehabilitacion.query.filter_by(colaborador_id=colaborador_id)
            .order_by(ConceptoRehabilitacion.id.desc())
            .first()
        )

    def guardar_concepto(self, fila):
        db.session.add(fila)
        db.session.commit()
        return fila

    def guardar_reintegro(self, fila):
        db.session.add(fila)
        db.session.commit()
        return fila

    def reintegros(self):
        return ReintegroEPS.query.order_by(ReintegroEPS.fecha.desc()).all()
