"""Detecta colaboradores que superan 90, 120, 150 y 180 días (5.5.3)."""

from collections import defaultdict

from config.reglas_monitoreo import hitos_superados
from modulos.monitoreo.repositorio import RepositorioMonitoreo


def reporte_hitos(repo: RepositorioMonitoreo | None = None) -> list[dict]:
    repo = repo or RepositorioMonitoreo()
    acumulado = defaultdict(int)
    por_colaborador = {}
    for item in repo.incapacidades():
        acumulado[item.colaborador_id] += item.dias
        por_colaborador[item.colaborador_id] = item.colaborador

    filas = []
    for colaborador_id, dias in acumulado.items():
        hitos = hitos_superados(dias)
        if not hitos:
            continue
        colaborador = por_colaborador[colaborador_id]
        filas.append(
            {
                "colaborador": colaborador,
                "dias": dias,
                "hitos": hitos,
                "ultimo_hito": max(hitos),
            }
        )
    return sorted(filas, key=lambda f: f["dias"], reverse=True)
