"""Integra los cálculos, tablas, reporte de viabilidad y gráficos."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from parte1_datos import (
    calcular_limite,
    calcular_probabilidades,
    sumas_caso_a,
    sumas_caso_b,
    sumas_caso_c,
)
from parte2_graficos import graficar_sumatorias


FUNCIONES_SUMAS: dict[str, Callable[[float, int], list[float]]] = {
    "A": sumas_caso_a,
    "B": sumas_caso_b,
    "C": sumas_caso_c,
}
NOMBRES_CASOS = {
    "A": "Caso A - WiFi estándar",
    "B": "Caso B - Fibra con reintentos decrecientes",
    "C": "Caso C - Red móvil con copia extra",
}
K_TABLA = 10
K_GRAFICO = 40
K_LIMITE = 1000
CAPACIDAD_MAXIMA = 10


def leer_digitos() -> list[int]:
    """Solicita los primeros ocho dígitos del RUT y valida la entrada."""
    while True:
        entrada = input("Ingrese los primeros 8 dígitos del RUT: ").strip().replace(".", "")
        if entrada.isdigit() and len(entrada) == 8:
            return [int(digito) for digito in entrada]
        print("Entrada inválida: deben ser exactamente 8 dígitos.")


def imprimir_tablas(
    probabilidades: Mapping[str, float],
    sumas_graficadas: Mapping[str, Mapping[str, list[float]]],
) -> None:
    """Imprime las tres tablas de sumas parciales para k de 1 a 10."""
    columnas = tuple(probabilidades)
    for caso, nombre in NOMBRES_CASOS.items():
        print(f"\n{nombre}")
        print("k\t" + "\t".join(columnas))
        for indice in range(K_TABLA):
            valores = (
                f"{sumas_graficadas[caso][probabilidad][indice]:.6f}"
                for probabilidad in columnas
            )
            print(f"{indice + 1}\t" + "\t".join(valores))


def calcular_resultados(
    probabilidades: Mapping[str, float],
) -> tuple[
    dict[str, dict[str, list[float]]],
    dict[str, dict[str, float]],
    dict[str, dict[str, bool]],
]:
    """Calcula las curvas para gráficos y los límites aproximados."""
    sumas_graficadas: dict[str, dict[str, list[float]]] = {}
    limites: dict[str, dict[str, float]] = {}
    convergencias: dict[str, dict[str, bool]] = {}

    for caso, funcion in FUNCIONES_SUMAS.items():
        sumas_graficadas[caso] = {}
        limites[caso] = {}
        convergencias[caso] = {}
        for clave, probabilidad in probabilidades.items():
            sumas_graficadas[caso][clave] = funcion(probabilidad, K_GRAFICO)
            sumas_largas = funcion(probabilidad, K_LIMITE)
            limite, convergio = calcular_limite(sumas_largas)
            limites[caso][clave] = limite
            convergencias[caso][clave] = convergio

    return sumas_graficadas, limites, convergencias


def imprimir_reporte(
    limites: Mapping[str, Mapping[str, float]],
    convergencias: Mapping[str, Mapping[str, bool]],
) -> None:
    """Muestra convergencia aproximada y límites de las nueve combinaciones."""
    print(f"\nReporte de convergencia (límite aproximado con k = {K_LIMITE})")
    for caso, nombre in NOMBRES_CASOS.items():
        print(f"\n{nombre}")
        print("Probabilidad\tLímite\t\tConvergencia")
        for probabilidad, limite in limites[caso].items():
            converge = "CONVERGE" if convergencias[caso][probabilidad] else "NO CONVERGE"
            print(f"{probabilidad}\t\t{limite:.6f}\t\t{converge}")


def imprimir_viabilidad(limites: Mapping[str, Mapping[str, float]]) -> None:
    """Imprime la tabla de cumplimiento para C_max."""
    probabilidades = tuple(next(iter(limites.values())))
    print(f"\nTabla de viabilidad (C_max = {CAPACIDAD_MAXIMA})")
    print("Caso\t" + "\t".join(probabilidades))
    for caso in NOMBRES_CASOS:
        estados = (
            "CUMPLE" if limites[caso][probabilidad] <= CAPACIDAD_MAXIMA else "NO CUMPLE"
            for probabilidad in probabilidades
        )
        print(f"{caso}\t" + "\t".join(estados))


def imprimir_recomendacion(limites: Mapping[str, Mapping[str, float]]) -> None:
    """Recomienda una combinación con menor límite que respete C_max."""
    combinaciones = [
        (caso, probabilidad, limite)
        for caso, limites_caso in limites.items()
        for probabilidad, limite in limites_caso.items()
    ]
    viables = [
        combinacion
        for combinacion in combinaciones
        if combinacion[2] <= CAPACIDAD_MAXIMA
    ]

    print("\nRecomendación")
    if viables:
        caso, probabilidad, limite = min(viables, key=lambda opcion: opcion[2])
        margen = CAPACIDAD_MAXIMA - limite
        print(
            f"Elegir {NOMBRES_CASOS[caso]} con {probabilidad}: "
            f"su límite aproximado ({limite:.6f}) es el menor entre las "
            f"combinaciones que cumplen C_max = {CAPACIDAD_MAXIMA}, "
            f"con un margen de {margen:.6f}."
        )
    else:
        caso, probabilidad, limite = min(combinaciones, key=lambda opcion: opcion[2])
        print(
            f"Ninguna combinación cumple C_max = {CAPACIDAD_MAXIMA}. "
            f"La menor aproximación de límite es {limite:.6f} en "
            f"{NOMBRES_CASOS[caso]} con {probabilidad}; aun así supera la capacidad, "
            "por lo que se debe revisar el requisito antes de recomendarla."
        )


def main() -> None:
    probabilidades = calcular_probabilidades(leer_digitos())
    print(
        "\nProbabilidades: "
        + ", ".join(f"{clave}={valor:.4f}" for clave, valor in probabilidades.items())
    )

    sumas_graficadas, limites, convergencias = calcular_resultados(probabilidades)
    imprimir_tablas(probabilidades, sumas_graficadas)
    imprimir_reporte(limites, convergencias)
    imprimir_viabilidad(limites)
    imprimir_recomendacion(limites)
    graficar_sumatorias(sumas_graficadas, limites)


if __name__ == "__main__":
    main()
