"""Concepto de rehabilitación antes del día 120 y envío al AFP antes del 150."""

from datetime import date

from config.reglas_monitoreo import DIA_CONCEPTO_REHABILITACION_EPS, DIA_ENVIO_CONCEPTO_AFP
from core.models import ConceptoRehabilitacion
from modulos.monitoreo.hitos import reporte_hitos
from modulos.monitoreo.repositorio import RepositorioMonitoreo


def pendientes_concepto(repo: RepositorioMonitoreo | None = None) -> list[dict]:
    repo = repo or RepositorioMonitoreo()
    pendientes = []
    for fila in reporte_hitos(repo):
        if fila["dias"] < DIA_CONCEPTO_REHABILITACION_EPS:
            continue
        concepto = repo.concepto(fila["colaborador"].id)
        if concepto:
            continue
        pendientes.append(
            {
                **fila,
                "solicitar_eps": True,
                "enviar_afp": fila["dias"] >= DIA_ENVIO_CONCEPTO_AFP,
            }
        )
    return pendientes


def registrar_concepto(colaborador_id: int, resultado: str, notas: str = "", enviado_afp: bool = False):
    repo = RepositorioMonitoreo()
    fila = ConceptoRehabilitacion(
        colaborador_id=colaborador_id,
        resultado=resultado,
        fecha_emision=date.today(),
        enviado_afp=enviado_afp,
        notas=notas,
    )
    return repo.guardar_concepto(fila)
