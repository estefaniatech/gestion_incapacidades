"""Modelos de datos del trámite de incapacidades."""

from datetime import datetime

from core.database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(40), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activo

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Colaborador(db.Model):
    __tablename__ = "colaboradores"

    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(30), unique=True, nullable=False)
    nombres = db.Column(db.String(120), nullable=False)
    apellidos = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(120))
    area = db.Column(db.String(120))
    email = db.Column(db.String(200))
    email_jefe = db.Column(db.String(200))
    nombre_jefe = db.Column(db.String(200))
    eps = db.Column(db.String(80))
    arl = db.Column(db.String(80))
    afp = db.Column(db.String(80))
    ibc_mensual = db.Column(db.Float, default=0)
    activo = db.Column(db.Boolean, default=True)

    incapacidades = db.relationship("Incapacidad", backref="colaborador", lazy=True)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def ibc_diario(self):
        return round((self.ibc_mensual or 0) / 30.0, 2)


class Incapacidad(db.Model):
    __tablename__ = "incapacidades"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)
    origen = db.Column(db.String(20), default="comun")
    entidad = db.Column(db.String(80), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    dias_acumulados = db.Column(db.Integer, default=0)
    diagnostico = db.Column(db.String(250))
    canal_recepcion = db.Column(db.String(40))
    fisica_recibida = db.Column(db.Boolean, default=False)
    ya_transcrita_eps = db.Column(db.Boolean, default=False)
    estado = db.Column(db.String(40), default="recibida")
    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_limite_transcripcion = db.Column(db.Date)
    numero_radicado = db.Column(db.String(80))
    fecha_transcripcion = db.Column(db.Date)
    motivo_rechazo = db.Column(db.String(500))
    ibc_snapshot = db.Column(db.Float, default=0)
    valor_empresa = db.Column(db.Float, default=0)
    valor_eps = db.Column(db.Float, default=0)
    valor_pagado_entidad = db.Column(db.Float, default=0)
    fecha_pago = db.Column(db.Date)
    fecha_promesa_pago = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    llamados_documentacion = db.Column(db.Integer, default=0)
    creado_por = db.Column(db.String(80))

    documentos = db.relationship("DocumentoIncapacidad", backref="incapacidad", lazy=True, cascade="all, delete-orphan")


class DocumentoIncapacidad(db.Model):
    __tablename__ = "documentos_incapacidad"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    tipo_documento = db.Column(db.String(80), nullable=False)
    obligatorio = db.Column(db.Boolean, default=True)
    recibido = db.Column(db.Boolean, default=False)
    ruta_archivo = db.Column(db.String(400))
    fecha_recepcion = db.Column(db.DateTime)


class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"))
    destinatario = db.Column(db.String(200), nullable=False)
    asunto = db.Column(db.String(250), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    canal = db.Column(db.String(40), default="correo")
    enviada_en = db.Column(db.DateTime, default=datetime.utcnow)


class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False)
    accion = db.Column(db.String(80), nullable=False)
    entidad = db.Column(db.String(80), nullable=False)
    entidad_id = db.Column(db.Integer)
    detalle = db.Column(db.Text)
    contiene_dato_salud = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class GestionCobro(db.Model):
    __tablename__ = "gestiones_cobro"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    canal = db.Column(db.String(80))
    resultado = db.Column(db.String(250))
    evidencia = db.Column(db.String(400))
    usuario = db.Column(db.String(80))


class RequerimientoCartera(db.Model):
    __tablename__ = "requerimientos_cartera"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.Text)
    usuario = db.Column(db.String(80))


class ProcesoJuridico(db.Model):
    __tablename__ = "procesos_juridicos"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    tipo_accion = db.Column(db.String(80))
    causal = db.Column(db.String(250))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    decision = db.Column(db.String(80))
    texto = db.Column(db.Text)
    usuario = db.Column(db.String(80))


class ConciliacionPago(db.Model):
    __tablename__ = "conciliaciones"

    id = db.Column(db.Integer, primary_key=True)
    periodo = db.Column(db.String(7), nullable=False)
    entidad = db.Column(db.String(80))
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"))
    valor_entidad = db.Column(db.Float, default=0)
    valor_interno = db.Column(db.Float, default=0)
    diferencia = db.Column(db.Float, default=0)
    identificado = db.Column(db.Boolean, default=True)
    notas = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)


class ConceptoRehabilitacion(db.Model):
    __tablename__ = "conceptos_rehabilitacion"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    resultado = db.Column(db.String(40))
    fecha_emision = db.Column(db.Date)
    enviado_afp = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text)


class ReintegroEPS(db.Model):
    __tablename__ = "reintegros_eps"

    id = db.Column(db.Integer, primary_key=True)
    colaborador_id = db.Column(db.Integer, db.ForeignKey("colaboradores.id"), nullable=False)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"))
    valor = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date)
    notas = db.Column(db.Text)


class NovedadNomina(db.Model):
    __tablename__ = "novedades_nomina"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    tipo_novedad = db.Column(db.String(80))
    valor = db.Column(db.Float, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    enviada = db.Column(db.Boolean, default=False)


class ReporteAusentismo(db.Model):
    __tablename__ = "reportes_ausentismo"

    id = db.Column(db.Integer, primary_key=True)
    periodo = db.Column(db.String(7), nullable=False)
    generado_en = db.Column(db.DateTime, default=datetime.utcnow)
    enviado_sgsst = db.Column(db.Boolean, default=False)
    contenido = db.Column(db.Text)


class ArchivoFisico(db.Model):
    __tablename__ = "archivo_fisico"

    id = db.Column(db.Integer, primary_key=True)
    incapacidad_id = db.Column(db.Integer, db.ForeignKey("incapacidades.id"), nullable=False)
    entidad = db.Column(db.String(80))
    ubicacion = db.Column(db.String(250))
    epicrisis_destruida = db.Column(db.Boolean, default=False)
    enviado_gestion_documental = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
