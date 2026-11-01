"""Transcripción ante EPS/ARL (numeral 5.2 y 5.2.1)."""

from datetime import date

from config.estados import EstadoIncapacidad
from config.plazos_eps import canal_transcripcion
from core import auditoria
from modulos.transcripcion.repositorio import RepositorioTranscripcion


class ServicioTranscripcion:
    def __init__(self):
        self.repo = RepositorioTranscripcion()

    def pendientes(self):
        items = self.repo.pendientes()
        hoy = date.today()
        for item in items:
            item.canal = canal_transcripcion(item.entidad)
            item.vence_pronto = bool(item.fecha_limite_transcripcion and item.fecha_limite_transcripcion <= hoy)
        return items

    def radicar(self, incapacidad_id: int, numero_radicado: str, fecha: date | None = None):
        item = self.repo.obtener(incapacidad_id)
        if item.estado not in {
            EstadoIncapacidad.DOCUMENTACION_COMPLETA.value,
            EstadoIncapacidad.RECHAZADA.value,
        }:
            raise ValueError("Solo se transcribe con documentación completa o tras un rechazo subsanado.")
        item.numero_radicado = numero_radicado
        item.fecha_transcripcion = fecha or date.today()
        item.estado = EstadoIncapacidad.TRANSCRITA.value
        item.motivo_rechazo = None
        self.repo.guardar(item)
        auditoria.registrar("transcribir", "incapacidad", item.id, f"Radicado {numero_radicado}")
        return item
