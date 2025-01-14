#!/usr/bin/python3
# -*- coding: utf-8 -*-

##################################################
# Autora: Patricia del Carmen Vaca Rubio         #
# Cuestionario individual 1. Integral definida   #
# Versión: Secuencial                            #
##################################################

from time import time


def f(x: int) -> int:
    """
    Definición de la función a partir de la cual queremos calcular
    la integral definida.

    Arg:
        - x (int): valor de la variable independiente.
    Returns:
        - int: valor de la variable dependiente.
    """
    return x**2 + 2*x + 1


def main():

    print(f"Este programa realizará la integral definida de la función"
          " f(x)=x^2+2x+1 mediante la aproximación de los rectángulos entre"
          " unos ciertos intervalos a y b y un número de pasos indicado por"
          " usted.")

    # Se piden al usuario los valores del intervalo de integración (a-b) y el
    # número de divisiones del área a calcular
    a = float(input("A continuación, introduzca el límite inferior del intervalo,"
                  " a: "))
    b = float(input("El límite superior del intervalo, b: "))
    n = int(input("El número de pasos o divisiones en que quiere dividir el"
                  " área a calcular (un número entero): "))

    t0 = time()
    area_total = 0  # Almacenará la suma total de las áreas de cada subdivisión
    Dx = (b-a) / n  # Longitud/distancia de cada paso
    for i in range(n):  # Iteramos sobre cada paso
        # Cálculo del área de un rectángulo (base por altura)
        subarea_i = Dx * f(a)
        area_total += subarea_i
        a = a + Dx  # Actualizamos el valor de a para el siguiente paso
    t1 = time()

    tiempo_ejecucion = t1 - t0

    print("La integral definida de la función en el intervalo a-b dado, es:",
          abs(area_total))
    print(f"El tiempo de ejecución para {n} pasos ha sido"
          f" {tiempo_ejecucion:.8f} segundos.")


if __name__ == "__main__":
    try:
        main()
        input("\nPulse <Intro> para salir.")
    except Exception as e:
        # Avisamos al usuario de cualquier posible error
        print("Se ha producido un error inesperado:", e)
        input("\nPulse <Intro> para salir.")
