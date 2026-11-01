from core.database import db
from core.models import Colaborador, Incapacidad


class RepositorioRecepcion:
    def crear_colaborador(self, datos: dict) -> Colaborador:
        existente = Colaborador.query.filter_by(documento=datos["documento"]).first()
        if existente:
            for k, v in datos.items():
                setattr(existente, k, v)
            db.session.commit()
            return existente
        fila = Colaborador(**datos)
        db.session.add(fila)
        db.session.commit()
        return fila

    def obtener_colaborador(self, colaborador_id: int) -> Colaborador | None:
        return Colaborador.query.get(colaborador_id)

    def buscar_documento(self, documento: str) -> Colaborador | None:
        return Colaborador.query.filter_by(documento=documento).first()

    def listar_colaboradores(self):
        return Colaborador.query.order_by(Colaborador.apellidos).all()

    def crear_incapacidad(self, datos: dict) -> Incapacidad:
        fila = Incapacidad(**datos)
        db.session.add(fila)
        db.session.commit()
        return fila

    def listar_recientes(self, limite=50):
        return Incapacidad.query.order_by(Incapacidad.fecha_recepcion.desc()).limit(limite).all()

    def obtener(self, incapacidad_id: int) -> Incapacidad | None:
        return Incapacidad.query.get(incapacidad_id)
