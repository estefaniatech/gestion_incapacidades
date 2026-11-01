"""Hitos de monitoreo de incapacidades (numeral 5.5.3)."""

HITOS_DIAS = [90, 120, 150, 180]

DIA_CONCEPTO_REHABILITACION_EPS = 120
DIA_ENVIO_CONCEPTO_AFP = 150
DIA_SUSPENSION_NOMINA = 180


def hitos_superados(dias_acumulados: int) -> list[int]:
    return [h for h in HITOS_DIAS if dias_acumulados >= h]


def alerta_concepto_rehabilitacion(dias_acumulados: int, tiene_concepto: bool) -> str | None:
    if dias_acumulados >= DIA_CONCEPTO_REHABILITACION_EPS and not tiene_concepto:
        return "Solicitar concepto de rehabilitación a la EPS antes del día 120."
    if dias_acumulados >= DIA_ENVIO_CONCEPTO_AFP and not tiene_concepto:
        return "Notificar a EPS, ARL, AFP y trabajador: no hay concepto de rehabilitación."
    return None


def suspende_pago_nomina(dias_acumulados: int) -> bool:
    return dias_acumulados > DIA_SUSPENSION_NOMINA
