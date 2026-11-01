"""Cobro jurídico: derecho de petición y tutela (5.4.2)."""

from config.estados import EstadoIncapacidad
from core import auditoria, notificaciones
from core.models import ProcesoJuridico
from modulos.juridico.repositorio import RepositorioJuridico


class ServicioJuridico:
    def __init__(self):
        self.repo = RepositorioJuridico()

    def bandeja(self):
        return self.repo.bandeja()

    def actuar(self, incapacidad_id: int, tipo_accion: str, causal: str, usuario: str):
        item = self.repo.obtener(incapacidad_id)
        texto = notificaciones.cargar_plantilla(
            "derecho_peticion.txt",
            colaborador=item.colaborador.nombre_completo,
            entidad=item.entidad,
            causal=causal,
            tipo_accion=tipo_accion,
            radicado=item.numero_radicado or "N/A",
        )
        fila = ProcesoJuridico(
            incapacidad_id=incapacidad_id,
            tipo_accion=tipo_accion,
            causal=causal,
            texto=texto,
            usuario=usuario,
            decision="en_tramite",
        )
        self.repo.guardar(fila)
        item.estado = EstadoIncapacidad.EN_JURIDICO.value
        self.repo.guardar(item)
        notificaciones.enviar(item.entidad, tipo_accion.replace("_", " ").title(), texto, item.id)
        auditoria.registrar("juridico", "incapacidad", item.id, tipo_accion)
        return fila

    def decidir(self, incapacidad_id: int, decision: str):
        item = self.repo.obtener(incapacidad_id)
        if decision == "baja":
            item.estado = EstadoIncapacidad.DADA_DE_BAJA.value
        elif decision == "recuperar":
            item.estado = EstadoIncapacidad.EN_JURIDICO.value
        self.repo.guardar(item)
        return item
