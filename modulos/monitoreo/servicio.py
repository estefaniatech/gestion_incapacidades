from config.reglas_monitoreo import suspende_pago_nomina
from modulos.monitoreo import comunicaciones, rehabilitacion, reintegros
from modulos.monitoreo.hitos import reporte_hitos
from modulos.monitoreo.repositorio import RepositorioMonitoreo


class ServicioMonitoreo:
    def __init__(self):
        self.repo = RepositorioMonitoreo()

    def panel(self):
        hitos = reporte_hitos(self.repo)
        return {
            "hitos": hitos,
            "pendientes_concepto": rehabilitacion.pendientes_concepto(self.repo),
            "suspender_nomina": [h for h in hitos if suspende_pago_nomina(h["dias"])],
            "reintegros": self.repo.reintegros(),
        }

    def registrar_concepto(self, colaborador_id, resultado, notas, enviado_afp):
        fila = rehabilitacion.registrar_concepto(colaborador_id, resultado, notas, enviado_afp)
        from core.models import Colaborador

        colaborador = Colaborador.query.get(colaborador_id)
        comunicaciones.comunicar_concepto(colaborador, resultado)
        return fila

    def alertar_sin_concepto(self):
        return comunicaciones.notificar_sin_concepto()

    def alertar_suspension(self):
        enviados = []
        for fila in self.panel()["suspender_nomina"]:
            comunicaciones.comunicar_suspension_nomina(fila["colaborador"], fila["dias"])
            enviados.append(fila["colaborador"].nombre_completo)
        return enviados

    def reintegro(self, **kwargs):
        return reintegros.registrar_reintegro(**kwargs)
