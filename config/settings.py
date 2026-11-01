"""Configuración general de la aplicación."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ARCHIVOS_DIR = BASE_DIR / "archivos_digitales"
REPORTES_DIR = BASE_DIR / "reportes"
PLANTILLAS_DIR = BASE_DIR / "plantillas"
DOCS_DIR = BASE_DIR / "docs"

DATA_DIR.mkdir(exist_ok=True)
ARCHIVOS_DIR.mkdir(exist_ok=True)
REPORTES_DIR.mkdir(exist_ok=True)

SECRET_KEY = "cambiar-en-produccion-gestion-incapacidades"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{(DATA_DIR / 'incapacidades.db').as_posix()}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

EMPRESA_NOMBRE = "Organización"
CORREO_ADMIN_PERSONAL = "administracion.personal@empresa.com"
CORREO_SG_SST = "sgsst@empresa.com"
CORREO_TESORERIA = "tesoreria@empresa.com"
CORREO_CONTABILIDAD = "contabilidad@empresa.com"
CORREO_CARTERA = "cartera@empresa.com"
CORREO_JURIDICO = "juridico@empresa.com"

DIAS_ENTREGA_DOCUMENTOS = 2
DIAS_HABILES_DOCUMENTACION_FALTANTE = 3
DIAS_PRESCRIPCION_PAGO_ENTIDAD = 365 * 3
DIAS_COBRO_PERSUASIVO_TRASLADO = 180
REQUERIMIENTOS_MINIMOS_CARTERA = 2
DIA_REPORTE_AUSENTISMO = 3

CANALES_RECEPCION = [
    "recepcion",
    "oficinas_principales",
    "lider_comercial",
    "correo_electronico",
    "gestion_humana",
]

EPS_TRANSCRIPCION_CORREO = ["SOS", "SANITAS", "FAMISANAR"]
