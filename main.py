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
K_GRAFICO = 50
K_LIMITE = 1000
CAPACIDAD_MAXIMA = 10
RUT_ELEGIDO = "224630840"


def obtener_digitos_rut() -> list[int]:
    """Obtiene los primeros ocho dígitos del RUT seleccionado."""
    if len(RUT_ELEGIDO) != 9 or not RUT_ELEGIDO.isdigit():
        raise ValueError("RUT_ELEGIDO debe contener 8 dígitos y su dígito verificador.")
    return [int(digito) for digito in RUT_ELEGIDO[:8]]


def imprimir_tablas(
    probabilidades: Mapping[str, float],
    sumas_graficadas: Mapping[str, Mapping[str, list[float]]],
) -> None:
    """Imprime las tres tablas de sumas parciales para k de 1 a 10."""
    columnas = tuple(probabilidades)
    # Encabezado con nombre y valor numérico de cada probabilidad
    encabezado_probs = "\t".join(
        f"{clave}={probabilidades[clave]:.4f}" for clave in columnas
    )
    for caso, nombre in NOMBRES_CASOS.items():
        print(f"\n{nombre}")
        print(f"k\t{encabezado_probs}")
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


def imprimir_recomendacion(
    limites: Mapping[str, Mapping[str, float]],
    convergencias: Mapping[str, Mapping[str, bool]],
) -> None:
    """Recomienda la combinación convergente con menor límite que respete C_max."""
    combinaciones = [
        (caso, probabilidad, limite, convergencias[caso][probabilidad])
        for caso, limites_caso in limites.items()
        for probabilidad, limite in limites_caso.items()
    ]
    viables = [
        combinacion
        for combinacion in combinaciones
        if combinacion[2] <= CAPACIDAD_MAXIMA and combinacion[3]
    ]

    print("\nRecomendación")
    if viables:
        caso, probabilidad, limite, _ = min(viables, key=lambda opcion: opcion[2])
        margen = CAPACIDAD_MAXIMA - limite
        print(
            f"Elegir {NOMBRES_CASOS[caso]} con {probabilidad}: "
            f"el reporte empírico la marca CONVERGE con k = {K_LIMITE}, y su "
            f"límite aproximado ({limite:.6f}) es el menor entre las "
            f"combinaciones convergentes que cumplen C_max = {CAPACIDAD_MAXIMA}, "
            f"con un margen de {margen:.6f}."
        )
    else:
        convergentes = [
            combinacion for combinacion in combinaciones if combinacion[3]
        ]
        if convergentes:
            caso, probabilidad, limite, _ = min(
                convergentes, key=lambda opcion: opcion[2]
            )
            print(
                f"Ninguna combinación convergente cumple C_max = "
                f"{CAPACIDAD_MAXIMA}. La menor aproximación de límite entre las "
                f"convergentes es {limite:.6f} en {NOMBRES_CASOS[caso]} con "
                f"{probabilidad}; supera la capacidad, por lo que no se recomienda."
            )
        else:
            print(
                f"No se puede recomendar una combinación: no se confirmó la "
                f"convergencia de ninguna serie hasta k = {K_LIMITE}."
            )


def main() -> None:
    digitos_rut = obtener_digitos_rut()
    rut_formateado = f"{RUT_ELEGIDO[:2]}.{RUT_ELEGIDO[2:5]}.{RUT_ELEGIDO[5:8]}-{RUT_ELEGIDO[8]}"
    print(f"RUT utilizado: {rut_formateado}")
    probabilidades = calcular_probabilidades(digitos_rut)
    print(
        "\nProbabilidades: "
        + ", ".join(f"{clave}={valor:.4f}" for clave, valor in probabilidades.items())
    )

    sumas_graficadas, limites, convergencias = calcular_resultados(probabilidades)
    imprimir_tablas(probabilidades, sumas_graficadas)
    imprimir_reporte(limites, convergencias)
    imprimir_viabilidad(limites)
    imprimir_recomendacion(limites, convergencias)
    graficar_sumatorias(sumas_graficadas, limites)


if __name__ == "__main__":
    main()
