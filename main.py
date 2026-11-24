"""Punto de entrada e integración del proyecto MATE1133."""

from __future__ import annotations

from parte1_datos import (
    calcular_limite,
    calcular_probabilidades,
    sumas_caso_a,
    sumas_caso_b,
    sumas_caso_c,
)
from parte2_graficos import generar_graficos


FUNCIONES_SUMAS = {
    "Caso A - WiFi": sumas_caso_a,
    "Caso B - Fibra": sumas_caso_b,
    "Caso C - Red móvil": sumas_caso_c,
}


def leer_digitos() -> list[int]:
    while True:
        entrada = input("Ingrese los primeros 8 dígitos del RUT: ").strip().replace(".", "")
        if entrada.isdigit() and len(entrada) == 8:
            return [int(digito) for digito in entrada]
        print("Entrada inválida: deben ser exactamente 8 dígitos.")


def imprimir_tabla(probabilidades: dict[str, float], k_max: int = 10) -> None:
    for nombre, funcion in FUNCIONES_SUMAS.items():
        print(f"\n{nombre}")
        print("k\t" + "\t".join(probabilidades))
        valores = {clave: funcion(probabilidad, k_max) for clave, probabilidad in probabilidades.items()}
        for k in range(k_max):
            print(f"{k + 1}\t" + "\t".join(f"{valores[clave][k]:.6f}" for clave in probabilidades))


def imprimir_reporte(probabilidades: dict[str, float], capacidad_maxima: float = 10) -> None:
    print("\nReporte de convergencia y viabilidad")
    for nombre, funcion in FUNCIONES_SUMAS.items():
        print(f"\n{nombre}")
        for clave, probabilidad in probabilidades.items():
            limite, convergio = calcular_limite(funcion(probabilidad))
            estado = "CUMPLE" if limite <= capacidad_maxima else "NO CUMPLE"
            print(f"{clave}: {'CONVERGE' if convergio else 'NO CONVERGE'}; límite={limite:.6f}; {estado}")


def main() -> None:
    probabilidades = calcular_probabilidades(leer_digitos())
    print("\nProbabilidades:", ", ".join(f"{clave}={valor:.4f}" for clave, valor in probabilidades.items()))
    imprimir_tabla(probabilidades)
    imprimir_reporte(probabilidades)
    generar_graficos(probabilidades, FUNCIONES_SUMAS)


if __name__ == "__main__":
    main()
