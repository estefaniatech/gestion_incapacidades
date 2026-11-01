"""Días hábiles, fechas y helpers de presentación."""

from datetime import date, timedelta


def es_fin_de_semana(dia: date) -> bool:
    return dia.weekday() >= 5


def sumar_dias_habiles(inicio: date, dias: int) -> date:
    actual = inicio
    restantes = dias
    while restantes > 0:
        actual += timedelta(days=1)
        if not es_fin_de_semana(actual):
            restantes -= 1
    return actual


def dias_entre(inicio: date, fin: date) -> int:
    return (fin - inicio).days + 1


def periodo_aaaa_mm(dia: date | None = None) -> str:
    dia = dia or date.today()
    return dia.strftime("%Y-%m")


def formato_moneda(valor: float | None) -> str:
    valor = valor or 0
    return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
