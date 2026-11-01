"""Análisis asistido de información (cierre del procedimiento).

Usa reglas del negocio. Si existe OPENAI_API_KEY se puede ampliar a un modelo externo.
"""

from collections import Counter

from modulos.ia.repositorio import RepositorioIA


class ServicioIA:
    def __init__(self):
        self.repo = RepositorioIA()

    def analizar(self) -> dict:
        datos = self.repo.resumen()
        alertas = []
        if datos["por_estado"].get("rechazada"):
            alertas.append("Hay incapacidades rechazadas: subsanar causal y retranscribir.")
        if datos["por_estado"].get("documentacion_incompleta"):
            alertas.append("Hay expedientes con documentación incompleta (plazo 3 días hábiles).")
        if datos["valor_eps_pendiente"] > 0:
            alertas.append("Existe cartera pendiente de reintegro por parte de las entidades.")
        causas = Counter(i.motivo_rechazo or "sin causal" for i in datos["rechazos"])
        recomendaciones = [
            "Priorizar transcripciones con plazo corto (SURA 150 días, paternidad 30 días, tránsito Salud Total 15 días).",
            "Generar el reporte de ausentismo los primeros 3 días del mes.",
            "Monitorear hitos 90/120/150/180 antes de conciliar el mes.",
        ]
        return {
            **datos,
            "alertas": alertas,
            "causas_rechazo": causas,
            "recomendaciones": recomendaciones,
            "narrativa": self._narrativa(datos, alertas),
        }

    def _narrativa(self, datos, alertas):
        return (
            f"El sistema registra {datos['total']} incapacidades. "
            f"La cartera estimada a cargo de entidades es {datos['valor_eps_pendiente']:.2f}. "
            + (" ".join(alertas) if alertas else "No se detectan alertas críticas en este corte.")
        )
