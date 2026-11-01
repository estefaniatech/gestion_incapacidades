"""Seguimiento diario/semanal de cobro (5.4 y pasos 8 a 11)."""

from datetime import date

from config.estados import EstadoIncapacidad
from core import auditoria
from core.models import GestionCobro
from modulos.seguimiento_cobro.repositorio import RepositorioCobro


class ServicioCobro:
    def __init__(self):
        self.repo = RepositorioCobro()

    def bandeja(self):
        return self.repo.transcritas()

    def cambiar_estado(self, incapacidad_id: int, estado: str, extra: dict, usuario: str):
        item = self.repo.obtener(incapacidad_id)
        item.estado = estado
        if estado == EstadoIncapacidad.RECHAZADA.value:
            item.motivo_rechazo = extra.get("motivo_rechazo", "")
        if estado == EstadoIncapacidad.COBRADA.value:
            if extra.get("fecha_promesa_pago"):
                item.fecha_promesa_pago = date.fromisoformat(extra["fecha_promesa_pago"])
        if estado == EstadoIncapacidad.PAGADA.value:
            item.fecha_pago = date.fromisoformat(extra["fecha_pago"]) if extra.get("fecha_pago") else date.today()
            item.valor_pagado_entidad = float(extra.get("valor_pagado_entidad") or item.valor_eps or 0)
        self.repo.guardar(item)
        auditoria.registrar("cobro", "incapacidad", item.id, f"Estado {estado}", dato_salud=False)
        self.registrar_gestion(incapacidad_id, "cambio_estado", f"Pasó a {estado}", usuario)
        return item

    def registrar_gestion(self, incapacidad_id: int, canal: str, resultado: str, usuario: str, evidencia: str = ""):
        fila = GestionCobro(
            incapacidad_id=incapacidad_id,
            canal=canal,
            resultado=resultado,
            evidencia=evidencia,
            usuario=usuario,
        )
        return self.repo.guardar(fila)
