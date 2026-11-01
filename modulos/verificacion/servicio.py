"""Verificación documental (numeral 5.1.2)."""

from pathlib import Path

from werkzeug.utils import secure_filename

from config.estados import EstadoIncapacidad
from config.reglas_documentos import documentos_requeridos, etiqueta_documento
from config.settings import ARCHIVOS_DIR, DIAS_HABILES_DOCUMENTACION_FALTANTE
from core import auditoria, notificaciones
from core.utils import sumar_dias_habiles
from modulos.verificacion.repositorio import RepositorioVerificacion


class ServicioVerificacion:
    def __init__(self):
        self.repo = RepositorioVerificacion()

    def inicializar_documentos(self, incapacidad):
        existentes = {d.tipo_documento for d in self.repo.documentos(incapacidad.id)}
        for codigo in documentos_requeridos(incapacidad.tipo, incapacidad.dias, incapacidad.ya_transcrita_eps):
            if codigo not in existentes:
                self.repo.crear_documento(
                    {
                        "incapacidad_id": incapacidad.id,
                        "tipo_documento": codigo,
                        "obligatorio": True,
                        "recibido": False,
                    }
                )

    def checklist(self, incapacidad_id: int):
        docs = self.repo.documentos(incapacidad_id)
        return [
            {
                "id": d.id,
                "codigo": d.tipo_documento,
                "etiqueta": etiqueta_documento(d.tipo_documento),
                "recibido": d.recibido,
                "ruta": d.ruta_archivo,
            }
            for d in docs
        ]

    def adjuntar(self, documento_id: int, archivo) -> None:
        nombre = secure_filename(archivo.filename)
        destino = ARCHIVOS_DIR / f"{documento_id}_{nombre}"
        archivo.save(destino)
        self.repo.marcar_recibido(documento_id, str(destino))

    def marcar_sin_archivo(self, documento_id: int):
        self.repo.marcar_recibido(documento_id, None)

    def evaluar(self, incapacidad_id: int) -> dict:
        incapacidad = self.repo.obtener(incapacidad_id)
        docs = self.repo.documentos(incapacidad_id)
        faltantes = [etiqueta_documento(d.tipo_documento) for d in docs if d.obligatorio and not d.recibido]
        if faltantes:
            incapacidad.estado = EstadoIncapacidad.DOCUMENTACION_INCOMPLETA.value
            incapacidad.llamados_documentacion = (incapacidad.llamados_documentacion or 0) + 1
            self.repo.guardar(incapacidad)
            notificaciones.aviso_documentacion_faltante(
                incapacidad.colaborador, faltantes, incapacidad.id, incapacidad.llamados_documentacion
            )
            auditoria.registrar("verificar", "incapacidad", incapacidad.id, f"Faltantes: {faltantes}")
            plazo = sumar_dias_habiles(incapacidad.fecha_recepcion.date(), DIAS_HABILES_DOCUMENTACION_FALTANTE)
            return {
                "completa": False,
                "faltantes": faltantes,
                "llamado": incapacidad.llamados_documentacion,
                "plazo_habiles": plazo,
                "citar_coordinacion": incapacidad.llamados_documentacion >= 2,
            }

        incapacidad.estado = EstadoIncapacidad.DOCUMENTACION_COMPLETA.value
        self.repo.guardar(incapacidad)
        auditoria.registrar("verificar", "incapacidad", incapacidad.id, "Documentación completa")
        return {"completa": True, "faltantes": [], "llamado": 0, "citar_coordinacion": False}
