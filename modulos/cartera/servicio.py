"""Cobro persuasivo (5.4.1 y paso 15)."""

from config.estados import EstadoIncapacidad
from config.settings import REQUERIMIENTOS_MINIMOS_CARTERA
from core import auditoria, notificaciones
from core.models import RequerimientoCartera
from modulos.cartera.repositorio import RepositorioCartera


class ServicioCartera:
    def __init__(self):
        self.repo = RepositorioCartera()

    def panel(self):
        return {
            "candidatas_180": self.repo.candidatas(),
            "pendientes": self.repo.pendientes_pago(),
        }

    def requerimiento(self, incapacidad_id: int, usuario: str):
        item = self.repo.obtener(incapacidad_id)
        existentes = self.repo.requerimientos(incapacidad_id)
        numero = len(existentes) + 1
        texto = notificaciones.cargar_plantilla(
            "requerimiento_cobro.txt",
            colaborador=item.colaborador.nombre_completo,
            entidad=item.entidad,
            dias=item.dias,
            valor=item.valor_eps,
            numero=numero,
        )
        fila = RequerimientoCartera(
            incapacidad_id=incapacidad_id,
            numero=numero,
            texto=texto,
            usuario=usuario,
        )
        self.repo.guardar(fila)
        item.estado = EstadoIncapacidad.EN_CARTERA.value
        self.repo.guardar(item)
        notificaciones.enviar(item.entidad, f"Requerimiento de cobro #{numero}", texto, item.id)
        auditoria.registrar("cartera", "incapacidad", item.id, f"Requerimiento {numero}")
        return fila

    def trasladar_juridico(self, incapacidad_id: int):
        item = self.repo.obtener(incapacidad_id)
        reqs = self.repo.requerimientos(incapacidad_id)
        if len(reqs) < REQUERIMIENTOS_MINIMOS_CARTERA:
            raise ValueError("Deben existir al menos dos requerimientos de cobro persuasivo.")
        item.estado = EstadoIncapacidad.EN_JURIDICO.value
        self.repo.guardar(item)
        auditoria.registrar("traslado", "incapacidad", item.id, "Traslado a jurídico")
        return item
