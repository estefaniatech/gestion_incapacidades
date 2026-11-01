from datetime import date

from config.estados import TipoIncapacidad
from config.plazos_eps import fecha_limite_transcripcion
from config.reglas_documentos import documentos_requeridos
from config.reglas_monitoreo import hitos_superados, suspende_pago_nomina
from config.reglas_pago import liquidar_dias
from core.utils import sumar_dias_habiles


def test_documentos_enfermedad_corta():
    docs = documentos_requeridos(TipoIncapacidad.ENFERMEDAD_GENERAL.value, 2)
    assert "certificado_incapacidad" in docs
    assert "epicrisis" not in docs


def test_documentos_transito():
    docs = documentos_requeridos(TipoIncapacidad.ACCIDENTE_TRANSITO.value, 5)
    assert "furips" in docs
    assert "epicrisis" in docs


def test_liquidacion_diez_dias():
    r = liquidar_dias(10, 100_000, 1)
    assert r["valor_empresa"] == 200_000.0
    assert round(r["valor_eps"], 2) == 536_000.0


def test_liquidacion_dia_181():
    r = liquidar_dias(1, 100_000, 181)
    assert r["tramite_trabajador_afp"] is True
    assert r["valor_eps"] == 0


def test_hitos():
    assert hitos_superados(89) == []
    assert hitos_superados(120) == [90, 120]
    assert suspende_pago_nomina(181) is True


def test_plazo_paternidad():
    limite = fecha_limite_transcripcion("SURA EPS", date(2026, 1, 1), TipoIncapacidad.LICENCIA_PATERNIDAD.value, date(2026, 1, 1))
    assert limite == date(2026, 1, 31)


def test_plazo_salud_total_transito():
    limite = fecha_limite_transcripcion("Salud Total", date(2026, 1, 1), TipoIncapacidad.ACCIDENTE_TRANSITO.value)
    assert limite == date(2026, 1, 16)


def test_dias_habiles():
    # viernes 2 ene 2026 + 3 hábiles = miércoles 7 (salta sábado y domingo)
    assert sumar_dias_habiles(date(2026, 1, 2), 3) == date(2026, 1, 7)
