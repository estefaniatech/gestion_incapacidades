"""Archivo físico por entidad y fecha; destrucción de epicrisis (5.3 y paso 16)."""

from config.estados import EstadoIncapacidad
from config.reglas_documentos import EPICRISIS
from core import auditoria
from core.models import ArchivoFisico
from modulos.archivo.repositorio import RepositorioArchivo


class ServicioArchivo:
    def __init__(self):
        self.repo = RepositorioArchivo()

    def archivar(self, incapacidad_id: int, ubicacion: str):
        item = Incapacidad_get(incapacidad_id)
        fila = self.repo.por_incapacidad(incapacidad_id) or ArchivoFisico(incapacidad_id=incapacidad_id)
        fila.entidad = item.entidad
        fila.ubicacion = ubicacion
        fila.enviado_gestion_documental = True
        self.repo.guardar(fila)
        item.estado = EstadoIncapacidad.ARCHIVADA.value
        self.repo.guardar(item)
        auditoria.registrar("archivar", "incapacidad", item.id, ubicacion)
        return fila

    def destruir_epicrisis(self, incapacidad_id: int):
        from core.models import Incapacidad

        item = Incapacidad.query.get(incapacidad_id)
        for doc in self.repo.documentos(incapacidad_id):
            if doc.tipo_documento == EPICRISIS:
                doc.ruta_archivo = None
                doc.recibido = True
                self.repo.guardar(doc)
        fila = self.repo.por_incapacidad(incapacidad_id) or ArchivoFisico(
            incapacidad_id=incapacidad_id, entidad=item.entidad
        )
        fila.epicrisis_destruida = True
        self.repo.guardar(fila)
        auditoria.registrar("destruir_epicrisis", "incapacidad", incapacidad_id, "Historia clínica no reposa en archivo", dato_salud=True)
        return fila


def Incapacidad_get(incapacidad_id: int):
    from core.models import Incapacidad

    return Incapacidad.query.get(incapacidad_id)
