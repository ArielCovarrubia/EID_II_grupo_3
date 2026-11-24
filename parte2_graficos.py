"""Visualización de las sumas parciales del proyecto."""

from __future__ import annotations

from collections.abc import Callable, Mapping

import matplotlib.pyplot as plt


def generar_graficos(
    probabilidades: Mapping[str, float],
    funciones_sumas: Mapping[str, Callable[[float, int], list[float]]],
    k_max: int = 40,
) -> None:
    """Genera un gráfico por cada caso y muestra las figuras."""
    for caso, funcion in funciones_sumas.items():
        figura, eje = plt.subplots()
        for nombre, probabilidad in probabilidades.items():
            valores = funcion(probabilidad, k_max)
            eje.plot(range(1, k_max + 1), valores, label=nombre)
            eje.axhline(valores[-1], linestyle=":", alpha=0.7)
        eje.set_title("Sumas parciales - " + caso)
        eje.set_xlabel("k")
        eje.set_ylabel("S_k")
        eje.grid(True, alpha=0.3)
        eje.legend()
        figura.tight_layout()
    plt.show()
