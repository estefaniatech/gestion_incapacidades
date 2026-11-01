"""Novedades de nómina a partir de incapacidades transcritas."""

from core import auditoria
from core.models import NovedadNomina
from modulos.nomina.repositorio import RepositorioNomina


class ServicioNomina:
    def __init__(self):
        self.repo = RepositorioNomina()

    def generar(self, incapacidad_id: int):
        item = self.repo.obtener_incapacidad(incapacidad_id)
        if self.repo.por_incapacidad(incapacidad_id):
            return self.repo.por_incapacidad(incapacidad_id)[0]
        fila = NovedadNomina(
            incapacidad_id=incapacidad_id,
            tipo_novedad=item.tipo,
            valor=item.valor_empresa,
            enviada=True,
        )
        self.repo.guardar(fila)
        auditoria.registrar("nomina", "incapacidad", incapacidad_id, "Novedad de nómina")
        return fila

    def listar(self):
        return self.repo.listar()
