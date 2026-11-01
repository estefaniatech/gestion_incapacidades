"""Documentos obligatorios por tipo de incapacidad (numeral 5.1.2)."""

from config.estados import TipoIncapacidad

CERTIFICADO = "certificado_incapacidad"
EPICRISIS = "epicrisis"
FURIPS = "furips"
CERTIFICADO_NACIDO_VIVO = "certificado_nacido_vivo"
REGISTRO_CIVIL = "registro_civil"
DOCUMENTO_IDENTIDAD = "documento_identidad"
DOCUMENTO_IDENTIDAD_MADRE = "documento_identidad_madre"
SEMANAS_GESTACION = "semanas_gestacion"

DOCUMENTOS_BASE = {
    TipoIncapacidad.ENFERMEDAD_GENERAL: [CERTIFICADO, EPICRISIS],
    TipoIncapacidad.ACCIDENTE_TRANSITO: [CERTIFICADO, EPICRISIS, FURIPS],
    TipoIncapacidad.ACCIDENTE_LABORAL: [CERTIFICADO, EPICRISIS],
    TipoIncapacidad.LICENCIA_MATERNIDAD: [
        CERTIFICADO,
        EPICRISIS,
        SEMANAS_GESTACION,
        CERTIFICADO_NACIDO_VIVO,
        REGISTRO_CIVIL,
        DOCUMENTO_IDENTIDAD,
    ],
    TipoIncapacidad.LICENCIA_PATERNIDAD: [
        EPICRISIS,
        SEMANAS_GESTACION,
        CERTIFICADO_NACIDO_VIVO,
        REGISTRO_CIVIL,
        DOCUMENTO_IDENTIDAD_MADRE,
    ],
}

EPICRISIS_OBLIGATORIA_SIEMPRE = {
    TipoIncapacidad.ACCIDENTE_TRANSITO,
    TipoIncapacidad.ACCIDENTE_LABORAL,
    TipoIncapacidad.LICENCIA_MATERNIDAD,
    TipoIncapacidad.LICENCIA_PATERNIDAD,
}


def documentos_requeridos(tipo: str, dias: int, ya_transcrita_eps: bool = False) -> list[str]:
    """Devuelve la lista de documentos exigidos según el caso.

    Epicrisis es obligatoria si la incapacidad supera dos días, o si es
    accidente de tránsito/trabajo o licencia. Si la EPS ya transcribió,
    la epicrisis no es necesaria en enfermedad general / accidente laboral.
    """
    tipo_enum = TipoIncapacidad(tipo)
    docs = list(DOCUMENTOS_BASE[tipo_enum])

    if tipo_enum == TipoIncapacidad.ENFERMEDAD_GENERAL and dias <= 2:
        docs = [d for d in docs if d != EPICRISIS]

    if ya_transcrita_eps and tipo_enum in {
        TipoIncapacidad.ENFERMEDAD_GENERAL,
        TipoIncapacidad.ACCIDENTE_LABORAL,
    }:
        docs = [d for d in docs if d != EPICRISIS]

    if tipo_enum == TipoIncapacidad.ENFERMEDAD_GENERAL and dias > 2:
        if EPICRISIS not in docs:
            docs.append(EPICRISIS)

    return docs


def etiqueta_documento(codigo: str) -> str:
    return {
        CERTIFICADO: "Certificado de incapacidad (original)",
        EPICRISIS: "Epicrisis o soporte de atención médica",
        FURIPS: "FURIPS",
        CERTIFICADO_NACIDO_VIVO: "Certificado de nacido vivo",
        REGISTRO_CIVIL: "Registro civil",
        DOCUMENTO_IDENTIDAD: "Fotocopia del documento de identidad",
        DOCUMENTO_IDENTIDAD_MADRE: "Fotocopia del documento de identidad de la madre",
        SEMANAS_GESTACION: "Documento con semanas de gestación al parto",
    }.get(codigo, codigo)
