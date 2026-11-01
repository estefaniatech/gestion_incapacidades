"""Pagos de EPS a trabajadores con más de 180 días."""

from datetime import date

from core.models import ReintegroEPS
from modulos.monitoreo.repositorio import RepositorioMonitoreo


def registrar_reintegro(colaborador_id: int, valor: float, incapacidad_id: int | None = None, notas: str = ""):
    repo = RepositorioMonitoreo()
    fila = ReintegroEPS(
        colaborador_id=colaborador_id,
        incapacidad_id=incapacidad_id,
        valor=float(valor),
        fecha=date.today(),
        notas=notas,
    )
    return repo.guardar_reintegro(fila)
