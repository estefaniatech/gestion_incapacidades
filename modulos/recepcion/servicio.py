"""Recepción de incapacidades y canales (numeral 5.1.1)."""

from datetime import date

from config.estados import EstadoIncapacidad, Origen, TipoIncapacidad
from config.plazos_eps import fecha_limite_transcripcion
from core import auditoria, notificaciones
from core.utils import dias_entre
from modulos.liquidacion.servicio import ServicioLiquidacion
from modulos.recepcion.repositorio import RepositorioRecepcion
from modulos.verificacion.servicio import ServicioVerificacion


class ServicioRecepcion:
    def __init__(self):
        self.repo = RepositorioRecepcion()
        self.verificacion = ServicioVerificacion()
        self.liquidacion = ServicioLiquidacion()

    def registrar(self, payload: dict, usuario: str) -> Incapacidad:
        colaborador = self._resolver_colaborador(payload)
        tipo = payload["tipo"]
        fecha_inicio = _a_fecha(payload["fecha_inicio"])
        fecha_fin = _a_fecha(payload["fecha_fin"])
        dias = dias_entre(fecha_inicio, fecha_fin)
        origen = Origen.LABORAL.value if tipo == TipoIncapacidad.ACCIDENTE_LABORAL.value else Origen.COMUN.value
        acumulado = self._acumulado(colaborador.id, fecha_inicio) + dias

        datos = {
            "colaborador_id": colaborador.id,
            "tipo": tipo,
            "origen": origen,
            "entidad": payload.get("entidad") or colaborador.eps or "",
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "dias": dias,
            "dias_acumulados": acumulado,
            "diagnostico": payload.get("diagnostico", ""),
            "canal_recepcion": payload.get("canal_recepcion", "gestion_humana"),
            "fisica_recibida": bool(payload.get("fisica_recibida")),
            "ya_transcrita_eps": bool(payload.get("ya_transcrita_eps")),
            "estado": EstadoIncapacidad.RECIBIDA.value,
            "ibc_snapshot": colaborador.ibc_mensual,
            "observaciones": payload.get("observaciones", ""),
            "creado_por": usuario,
            "fecha_limite_transcripcion": fecha_limite_transcripcion(
                payload.get("entidad") or colaborador.eps or "",
                fecha_inicio,
                tipo,
                _a_fecha(payload["fecha_nacimiento"]) if payload.get("fecha_nacimiento") else None,
            ),
        }
        incapacidad = self.repo.crear_incapacidad(datos)
        self.liquidacion.aplicar(incapacidad)
        self.verificacion.inicializar_documentos(incapacidad)
        notificaciones.aviso_jefe_reemplazo(colaborador, incapacidad)
        auditoria.registrar("crear", "incapacidad", incapacidad.id, "Recepción de incapacidad", dato_salud=True)
        return incapacidad

    def _resolver_colaborador(self, payload: dict):
        if payload.get("colaborador_id"):
            return self.repo.obtener_colaborador(int(payload["colaborador_id"]))
        return self.repo.crear_colaborador(
            {
                "documento": payload["documento"],
                "nombres": payload["nombres"],
                "apellidos": payload["apellidos"],
                "cargo": payload.get("cargo", ""),
                "area": payload.get("area", ""),
                "email": payload.get("email", ""),
                "email_jefe": payload.get("email_jefe", ""),
                "nombre_jefe": payload.get("nombre_jefe", ""),
                "eps": payload.get("eps", payload.get("entidad", "")),
                "arl": payload.get("arl", ""),
                "afp": payload.get("afp", ""),
                "ibc_mensual": float(payload.get("ibc_mensual") or 0),
            }
        )

    def _acumulado(self, colaborador_id: int, fecha_inicio: date) -> int:
        from core.models import Incapacidad

        previas = Incapacidad.query.filter_by(colaborador_id=colaborador_id).all()
        return sum(i.dias for i in previas if i.fecha_inicio <= fecha_inicio)

    def listar(self):
        return self.repo.listar_recientes()


def _a_fecha(valor):
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(valor)
