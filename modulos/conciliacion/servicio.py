"""Conciliación con tesorería y contabilidad (5.5, 5.5.1, pasos 12 y 13)."""

from core import auditoria, notificaciones
from core.models import ConciliacionPago
from core.utils import periodo_aaaa_mm
from modulos.conciliacion.repositorio import RepositorioConciliacion


class ServicioConciliacion:
    def __init__(self):
        self.repo = RepositorioConciliacion()

    def registrar_pago_entidad(self, incapacidad_id: int | None, entidad: str, valor: float, periodo: str | None, notas: str):
        periodo = periodo or periodo_aaaa_mm()
        valor_interno = 0.0
        identificado = False
        if incapacidad_id:
            from core.models import Incapacidad

            item = Incapacidad.query.get(incapacidad_id)
            valor_interno = item.valor_eps or 0
            identificado = True
            entidad = entidad or item.entidad
        diferencia = round(float(valor) - valor_interno, 2)
        fila = ConciliacionPago(
            periodo=periodo,
            entidad=entidad,
            incapacidad_id=incapacidad_id,
            valor_entidad=float(valor),
            valor_interno=valor_interno,
            diferencia=diferencia,
            identificado=identificado,
            notas=notas,
        )
        self.repo.guardar(fila)
        if not identificado:
            notificaciones.enviar(
                "contabilidad@empresa.com",
                "Saldo no identificado en conciliación",
                f"Entidad {entidad} reportó ${valor} en {periodo} sin cruce interno.",
            )
        auditoria.registrar("conciliar", "conciliacion", fila.id, periodo)
        return fila

    def listar(self, periodo: str | None = None):
        periodo = periodo or periodo_aaaa_mm()
        return periodo, self.repo.por_periodo(periodo)
