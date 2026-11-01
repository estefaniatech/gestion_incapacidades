"""Estados del trámite (numeral 5.4) y del flujo interno."""

from enum import Enum


class EstadoIncapacidad(str, Enum):
    RECIBIDA = "recibida"
    DOCUMENTACION_INCOMPLETA = "documentacion_incompleta"
    DOCUMENTACION_COMPLETA = "documentacion_completa"
    TRANSCRITA = "transcrita"
    COBRADA = "cobrada"
    RECHAZADA = "rechazada"
    PAGADA = "pagada"
    EN_CARTERA = "en_cartera"
    EN_JURIDICO = "en_juridico"
    DADA_DE_BAJA = "dada_de_baja"
    ARCHIVADA = "archivada"


class TipoIncapacidad(str, Enum):
    ENFERMEDAD_GENERAL = "enfermedad_general"
    ACCIDENTE_TRANSITO = "accidente_transito"
    ACCIDENTE_LABORAL = "accidente_laboral"
    LICENCIA_MATERNIDAD = "licencia_maternidad"
    LICENCIA_PATERNIDAD = "licencia_paternidad"


class Origen(str, Enum):
    COMUN = "comun"
    LABORAL = "laboral"


class Rol(str, Enum):
    ADMIN = "admin"
    AUXILIAR_GH = "auxiliar_gh"
    RECEPCIONISTA = "recepcionista"
    LIDER = "lider"
    COLABORADOR = "colaborador"
    TESORERIA = "tesoreria"
    CONTABILIDAD = "contabilidad"
    CARTERA = "cartera"
    JURIDICO = "juridico"
    SG_SST = "sgsst"


ESTADOS_COBRO = {
    EstadoIncapacidad.TRANSCRITA: "Transcrita formalmente en la entidad y en verificación.",
    EstadoIncapacidad.COBRADA: "Verificada y aprobada; pendiente de pago a la organización.",
    EstadoIncapacidad.RECHAZADA: "No admitida; se debe subsanar y retranscribir.",
    EstadoIncapacidad.PAGADA: "La entidad realizó el pago correspondiente.",
}
