"""Cálculos matemáticos del proyecto MATE1133."""

from __future__ import annotations

from collections.abc import Callable, Sequence


def calcular_probabilidades(digitos: Sequence[int]) -> dict[str, float]:
    """Calcula p1, p2 y p3 a partir de los primeros ocho dígitos del RUT."""
    if len(digitos) != 8 or any(digito < 0 or digito > 9 for digito in digitos):
        raise ValueError("Se requieren exactamente 8 dígitos entre 0 y 9.")

    return {
        "p1": (digitos[0] + digitos[2] + digitos[4] + 1) * 2 / 100,
        "p2": (digitos[1] + digitos[3] + digitos[5] + 1) * 3 / 100,
        "p3": (digitos[6] + digitos[7] + 1) * 4 / 100,
    }


def _calcular_sumas(
    p: float, termino: Callable[[int], float], k_max: int
) -> list[float]:
    if not 0 < p <= 1:
        raise ValueError("La probabilidad debe estar entre 0 y 1.")
    if k_max < 1:
        raise ValueError("k_max debe ser positivo.")

    sumas: list[float] = []
    acumulada = 0.0
    for i in range(1, k_max + 1):
        acumulada += termino(i) * (1 - p) ** (i - 1) * p
        sumas.append(acumulada)
    return sumas


def sumas_caso_a(p: float, k_max: int = 1000) -> list[float]:
    """Calcula S_k^A para el caso WiFi."""
    return _calcular_sumas(p, lambda i: float(i), k_max)


def sumas_caso_b(p: float, k_max: int = 1000) -> list[float]:
    """Calcula S_k^B para el caso Fibra."""
    return _calcular_sumas(p, lambda i: 1 / i, k_max)


def sumas_caso_c(p: float, k_max: int = 1000) -> list[float]:
    """Calcula S_k^C para el caso Red móvil."""
    return _calcular_sumas(p, lambda i: float(i + 1), k_max)


def calcular_limite(sumas: Sequence[float], tolerancia: float = 1e-6) -> tuple[float, bool]:
    """Obtiene el último valor y si la sucesión converge con la tolerancia dada."""
    if not sumas:
        raise ValueError("Se requiere al menos una suma parcial.")
    convergio = any(abs(actual - anterior) < tolerancia for anterior, actual in zip(sumas, sumas[1:]))
    return sumas[-1], convergio
