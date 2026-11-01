"""Porcentajes de reconocimiento (numeral 5.5.2).

Días 1-2: 100% IBC a cargo de la empresa.
Días 3-90: 67% IBC a cargo de la EPS.
Días 91-180: 50% IBC a cargo de la EPS.
Desde el día 181: el trabajador tramita ante AFP o EPS.
"""

from dataclasses import dataclass

PORCENTAJE_EMPRESA = 1.00
PORCENTAJE_EPS_3_90 = 0.67
PORCENTAJE_EPS_91_180 = 0.50

DIA_LIMITE_EMPRESA = 2
DIA_LIMITE_EPS_67 = 90
DIA_LIMITE_EPS_50 = 180


@dataclass
class TramoPago:
    dia_desde: int
    dia_hasta: int | None
    porcentaje: float
    pagador: str
    descripcion: str


TRAMOS = [
    TramoPago(1, 2, PORCENTAJE_EMPRESA, "empresa", "Días 1-2: 100% IBC a cargo de la empresa"),
    TramoPago(3, 90, PORCENTAJE_EPS_3_90, "eps", "Días 3-90: 67% IBC a cargo de la EPS"),
    TramoPago(91, 180, PORCENTAJE_EPS_91_180, "eps", "Días 91-180: 50% IBC a cargo de la EPS"),
    TramoPago(181, None, 0.0, "trabajador_afp", "Desde día 181: trámite del trabajador ante AFP o EPS"),
]


def tramo_para_dia_acumulado(dia: int) -> TramoPago:
    for tramo in TRAMOS:
        hasta = tramo.dia_hasta if tramo.dia_hasta is not None else 10**9
        if tramo.dia_desde <= dia <= hasta:
            return tramo
    return TRAMOS[-1]


def liquidar_dias(dias: int, ibc_diario: float, dia_acumulado_inicio: int = 1) -> dict:
    """Liquida una incapacidad de `dias` calendario sobre IBC diario.

    `dia_acumulado_inicio` permite continuar un acumulado de prórrogas.
    """
    valor_empresa = 0.0
    valor_eps = 0.0
    detalle = []

    for i in range(dias):
        dia_abs = dia_acumulado_inicio + i
        tramo = tramo_para_dia_acumulado(dia_abs)
        valor = round(ibc_diario * tramo.porcentaje, 2)
        if tramo.pagador == "empresa":
            valor_empresa += valor
        elif tramo.pagador == "eps":
            valor_eps += valor
        detalle.append(
            {
                "dia": dia_abs,
                "porcentaje": tramo.porcentaje,
                "pagador": tramo.pagador,
                "valor": valor,
            }
        )

    return {
        "valor_empresa": round(valor_empresa, 2),
        "valor_eps": round(valor_eps, 2),
        "valor_total_reconocido": round(valor_empresa + valor_eps, 2),
        "detalle": detalle,
        "tramite_trabajador_afp": any(d["pagador"] == "trabajador_afp" for d in detalle),
    }
