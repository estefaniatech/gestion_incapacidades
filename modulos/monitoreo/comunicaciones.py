"""Avisos a EPS, ARL, AFP y trabajador (numeral 5.5.3)."""

from core import notificaciones
from modulos.monitoreo.rehabilitacion import pendientes_concepto


def notificar_sin_concepto():
    enviados = []
    for fila in pendientes_concepto():
        colaborador = fila["colaborador"]
        cuerpo = (
            f"El colaborador {colaborador.nombre_completo} acumula {fila['dias']} días de incapacidad "
            "y no se ha expedido el concepto de rehabilitación. Se notifica a EPS, ARL, AFP y trabajador."
        )
        destinatarios = [
            colaborador.email or colaborador.nombre_completo,
            colaborador.eps or "EPS",
            colaborador.arl or "ARL",
            colaborador.afp or "AFP",
        ]
        for dest in destinatarios:
            notificaciones.enviar(dest, "Ausencia de concepto de rehabilitación", cuerpo)
        enviados.append(colaborador.nombre_completo)
    return enviados


def comunicar_concepto(colaborador, resultado: str):
    cuerpo = (
        f"Se comunica el concepto de rehabilitación ({resultado}) del colaborador "
        f"{colaborador.nombre_completo}."
    )
    for dest in [colaborador.email, colaborador.eps, colaborador.arl, colaborador.afp]:
        if dest:
            notificaciones.enviar(dest, f"Concepto de rehabilitación: {resultado}", cuerpo)


def comunicar_suspension_nomina(colaborador, dias: int):
    cuerpo = (
        f"Señor(a) {colaborador.nombre_completo}: su incapacidad supera {dias} días. "
        "Se suspende el pago por nómina. Debe gestionar el reconocimiento ante su fondo de pensiones."
    )
    notificaciones.enviar(colaborador.email or colaborador.nombre_completo, "Suspensión de pago por nómina (>180 días)", cuerpo)
