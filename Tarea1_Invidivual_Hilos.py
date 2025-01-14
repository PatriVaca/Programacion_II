#!/usr/bin/python3
# -*- coding: utf-8 -*-

##################################################
# Autora: Patricia del Carmen Vaca Rubio         #
# Cuestionario individual 1. Integral definida   #
# Versión: Hilos                                 #
##################################################

from time import time
from threading import Thread


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


class CalcularSubareaHilo(Thread):
    """
    Clase que hereda las propiedades de la clase 'Thread' del módulo 'threading'
    y que además nos permite calcular el área de los rectángulos de cada paso
    de los que se encargará el hilo.

    Args:
        ini (float): límite inferior del intervalo de integración del hilo.
        fin (float): límite superior del intervalo de integración del hilo.
        n_por_hilo (int): número de pasos de los que se encarga el hilo.
    """

    def __init__(self, ini: float, fin: float, n_por_hilo: int):
        Thread.__init__(self)
        self.ini = ini
        self.fin = fin
        self.n = n_por_hilo
        self.subarea = 0  # área total de los rectángulos calculados por el hilo

    def run(self):  # Cálculo del área de un rectángulo (base por altura)
        Dx_paso = (self.fin - self.ini) / self.n # Longitud/distancia de cada paso
        for i in range(self.n):  # número de pasos que le corresponde a cada hilo
            inicio_paso = self.ini + i * Dx_paso
            self.subarea += Dx_paso * f(inicio_paso)


def main():
    print(f"\tEste programa realizará la integral definida de la función"
          " f(x)=x^2+2x+1 mediante la aproximación de los rectángulos entre"
          " unos ciertos intervalos a y b y un número de pasos e hilos de"
          " ejecución indicados por usted.")

    # Se piden al usuario los valores del intervalo de integración (a-b), el
    # número de divisiones del área a calcular y el número de hilos
    a = float(input("A continuación, introduzca el límite inferior del intervalo,"
                    " a: "))
    b = float(input("El límite superior del intervalo, b: "))
    n = int(input("El número de pasos o divisiones en que quiere dividir el"
                  " área a calcular (un número entero): "))
    num_hilos = int(
        input("El número de hilos que quiere emplear (un número entero): "))

    # Validación para asegurarse de que el número de pasos es al menos igual
    # al número de hilos
    if n < num_hilos:
        print("Error: El número de pasos no puede ser menor que el número de hilos.")
        return

    Dx_hilo = (b-a) / num_hilos  # Distancia total que abarca cada hilo
    lista_hilos = []

    t0 = time()
    for i in range(num_hilos):
        # Distintos valores de inicio según el intervalo del que se ocupa cada hilo
        hilo = CalcularSubareaHilo(
            a + i * Dx_hilo, a + (i + 1) * Dx_hilo, n // num_hilos)
        lista_hilos.append(hilo)
        hilo.start()

    for hilo in lista_hilos:
        # Esperamos así a que todos los hilos hijos terminen su ejecución
        hilo.join()

    # Sumamos todas las subáreas calculadas una vez que los hilos han terminado
    area_total = sum(hilo.subarea for hilo in lista_hilos)
    t1 = time()

    tiempo_ejecucion = t1 - t0

    print(f"La integral definida de la función en el intervalo a-b dado para {n}"
          f" pasos y {num_hilos} hilos es:", abs(area_total))
    print(
        f"El tiempo de ejecución ha sido de {tiempo_ejecucion:.8f} segundos.")


if __name__ == "__main__":
    try:
        main()
        input("\nPulse <Intro> para salir.")
    except Exception as e:
        # Avisamos al usuario de cualquier posible error
        if type(e) != FileNotFoundError:
            print("Se ha producido un error inesperado:", e)
            input("\nPulse <Intro> para salir.")
