"""Cálculos de probabilidades, sumas parciales y límites empíricos."""

from collections.abc import Sequence
from numbers import Real


def calcular_probabilidades(digitos: Sequence[int]) -> dict[str, float]:
    """Calcula p1, p2 y p3 a partir de los primeros ocho dígitos del RUT."""
    if len(digitos) != 8 or any(
        not isinstance(digito, int) or not 0 <= digito <= 9 for digito in digitos
    ):
        raise ValueError("Se requieren exactamente 8 dígitos entre 0 y 9.")

    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    return {
        "p1": (d1 + d3 + d5 + 1) * 2 / 100,
        "p2": (d2 + d4 + d6 + 1) * 3 / 100,
        "p3": (d7 + d8 + 1) * 4 / 100,
    }


def _validar_entrada(p: float, k: int) -> None:
    if not isinstance(p, Real) or not 0 < p < 1:
        raise ValueError("La probabilidad p debe estar entre 0 y 1.")
    if not isinstance(k, int) or k < 1:
        raise ValueError("k debe ser un entero positivo.")


def sumas_caso_a(p: float, k: int) -> list[float]:
    """Devuelve S1, ..., Sk para el caso A."""
    _validar_entrada(p, k)
    return [
        sum(i * (1 - p) ** (i - 1) * p for i in range(1, n + 1))
        for n in range(1, k + 1)
    ]


def sumas_caso_b(p: float, k: int) -> list[float]:
    """Devuelve S1, ..., Sk para el caso B."""
    _validar_entrada(p, k)
    return [
        sum((1 / i) * (1 - p) ** (i - 1) * p for i in range(1, n + 1))
        for n in range(1, k + 1)
    ]


def sumas_caso_c(p: float, k: int) -> list[float]:
    """Devuelve S1, ..., Sk para el caso C."""
    _validar_entrada(p, k)
    return [
        sum((i + 1) * (1 - p) ** (i - 1) * p for i in range(1, n + 1))
        for n in range(1, k + 1)
    ]


def calcular_limite(
    sumas_parciales: Sequence[float], tolerancia: float = 1e-6
) -> tuple[float, bool]:
    """Devuelve la última suma parcial y si el cambio final está bajo la tolerancia."""
    if not sumas_parciales:
        raise ValueError("Se requiere al menos una suma parcial.")
    if tolerancia <= 0:
        raise ValueError("La tolerancia debe ser positiva.")

    limite = float(sumas_parciales[-1])
    convergio = (
        len(sumas_parciales) > 1
        and abs(sumas_parciales[-1] - sumas_parciales[-2]) < tolerancia
    )
    return limite, convergio
