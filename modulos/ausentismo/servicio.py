"""Reporte de ausentismo a SG-SST los primeros 3 días de cada mes (paso 6)."""

from datetime import date

from config.settings import CORREO_SG_SST
from core import notificaciones
from core.models import ReporteAusentismo
from core.utils import periodo_aaaa_mm
from modulos.ausentismo.repositorio import RepositorioAusentismo


class ServicioAusentismo:
    def __init__(self):
        self.repo = RepositorioAusentismo()

    def generar(self, periodo: str | None = None):
        periodo = periodo or periodo_aaaa_mm()
        items = self.repo.del_periodo(periodo)
        lineas = [
            f"{i.colaborador.nombre_completo};{i.tipo};{i.fecha_inicio};{i.fecha_fin};{i.dias};{i.entidad}"
            for i in items
        ]
        contenido = "colaborador;tipo;inicio;fin;dias;entidad\n" + "\n".join(lineas)
        reporte = ReporteAusentismo(periodo=periodo, contenido=contenido, enviado_sgsst=True)
        self.repo.guardar_reporte(reporte)
        notificaciones.enviar(
            CORREO_SG_SST,
            f"Reporte de ausentismo {periodo}",
            f"Se adjunta el informe de {len(items)} incapacidades del periodo {periodo}.\n\n{contenido}",
        )
        return reporte

    def listar(self):
        return self.repo.reportes()

    def dentro_de_plazo(self) -> bool:
        return date.today().day <= 3
