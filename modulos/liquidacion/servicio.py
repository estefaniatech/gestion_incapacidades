"""Liquidación 100% / 67% / 50% (numeral 5.5.2)."""

from config.reglas_pago import liquidar_dias
from modulos.liquidacion.repositorio import RepositorioLiquidacion


class ServicioLiquidacion:
    def __init__(self):
        self.repo = RepositorioLiquidacion()

    def aplicar(self, incapacidad):
        inicio_acumulado = max(1, (incapacidad.dias_acumulados or incapacidad.dias) - incapacidad.dias + 1)
        ibc_diario = round((incapacidad.ibc_snapshot or 0) / 30.0, 2)
        resultado = liquidar_dias(incapacidad.dias, ibc_diario, inicio_acumulado)
        incapacidad.valor_empresa = resultado["valor_empresa"]
        incapacidad.valor_eps = resultado["valor_eps"]
        self.repo.guardar(incapacidad)
        resultado["ibc_diario"] = ibc_diario
        return resultado

    def detalle(self, incapacidad_id: int):
        item = self.repo.obtener(incapacidad_id)
        inicio_acumulado = max(1, (item.dias_acumulados or item.dias) - item.dias + 1)
        ibc_diario = round((item.ibc_snapshot or 0) / 30.0, 2)
        return item, liquidar_dias(item.dias, ibc_diario, inicio_acumulado)
