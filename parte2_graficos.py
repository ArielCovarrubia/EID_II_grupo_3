"""Genera los gráficos de sumas parciales de los casos A, B y C."""

from collections.abc import Mapping, Sequence
from numbers import Real

import matplotlib.pyplot as plt


CASOS = {
    "A": "Caso A — WiFi estándar",
    "B": "Caso B — Fibra con reintentos decrecientes",
    "C": "Caso C — Red móvil con copia extra",
}
PROBABILIDADES = ("p1", "p2", "p3")


def graficar_sumatorias(
    sumas_parciales: Mapping[str, Mapping[str, Sequence[Real]]],
    limites: Mapping[str, Mapping[str, Real]],
) -> None:
    """Muestra un gráfico por caso a partir de sus sumas y límites."""
    _validar_entradas(sumas_parciales, limites)

    colores = {"p1": "tab:blue", "p2": "tab:orange", "p3": "tab:green"}
    for caso, titulo in CASOS.items():
        figura, eje = plt.subplots(figsize=(9, 5.5))

        for probabilidad in PROBABILIDADES:
            valores = sumas_parciales[caso][probabilidad]
            ks = range(1, len(valores) + 1)
            color = colores[probabilidad]
            limite = float(limites[caso][probabilidad])

            eje.plot(ks, valores, color=color, linewidth=2,
                     label=f"{probabilidad} — suma parcial")
            eje.axhline(limite, color=color, linestyle=":", linewidth=1.5,
                        label=f"{probabilidad} — límite ≈ {limite:.6g}")

        eje.set_title(titulo)
        eje.set_xlabel("Número de términos acumulados, k")
        eje.set_ylabel(r"Suma parcial $S_k$")
        eje.set_xlim(left=1)
        eje.grid(True, linestyle="--", alpha=0.35)
        eje.legend()
        figura.tight_layout()

    plt.show()


def _validar_entradas(sumas_parciales: Mapping, limites: Mapping) -> None:
    """Comprueba que estén las tres curvas y sus límites."""
    for caso in CASOS:
        if caso not in sumas_parciales or caso not in limites:
            raise ValueError(f"Faltan datos o límites para el caso {caso}.")
        for probabilidad in PROBABILIDADES:
            if probabilidad not in sumas_parciales[caso] or probabilidad not in limites[caso]:
                raise ValueError(
                    f"Faltan la curva o el límite de {probabilidad} para el caso {caso}."
                )
            valores = sumas_parciales[caso][probabilidad]
            if not valores:
                raise ValueError(f"La curva {caso}/{probabilidad} no contiene valores.")
            if not isinstance(limites[caso][probabilidad], Real):
                raise TypeError(f"El límite de {caso}/{probabilidad} debe ser numérico.")
