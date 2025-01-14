#!/usr/bin/python3
# -*- coding: utf-8 -*-

##################################################
# Autora: Patricia del Carmen Vaca Rubio         #
# Cuestionario individual 1. Integral definida   #
# Versión: Procesos                              #
##################################################

from time import time
from multiprocessing import Process


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


class CalcularSubareaProceso(Process):
    """
    Clase que hereda las propiedades de la clase 'Process' del módulo
    'multiprocessing' y que además nos permite calcular el área de los
    rectángulos de cada paso de los que se encargará el proceso.

    Args:
        ini (float): límite inferior del intervalo de integración del proceso.
        fin (float): límite superior del intervalo de integración del proceso.
        n_por_proceso (int): número de pasos de los que se encarga el proceso.
    """

    def __init__(self, ini: float, fin: float, n_por_proceso: int):
        Process.__init__(self)
        self.ini = ini
        self.fin = fin
        self.n = n_por_proceso
        self.subarea = 0  # área total de los rectángulos calculados por el proceso

    def run(self):  # Cálculo del área de un rectángulo (base por altura)
        # Longitud/distancia de cada paso
        Dx_paso = (self.fin - self.ini) / self.n
        for i in range(self.n):  # número de pasos que le corresponde a cada proceso
            inicio_paso = self.ini + i * Dx_paso
            self.subarea += Dx_paso * f(inicio_paso)


def main():

    print(f"\tEste programa realizará la integral definida de la función"
          " f(x)=x^2+2x+1 mediante la aproximación de los rectángulos entre"
          " unos ciertos intervalos a y b y un número de pasos y procesos de"
          " ejecución indicados por usted.")

    # Se piden al usuario los valores del intervalo de integración (a-b), el
    # número de divisiones del área a calcular y el número de procesos
    a = float(input("A continuación, introduzca el límite inferior del intervalo,"
                    " a: "))
    b = float(input("El límite superior del intervalo, b: "))
    n = int(input("El número de pasos o divisiones en que quiere dividir el"
                  " área a calcular (un número entero): "))
    num_procesos = int(
        input("El número de procesos que quiere emplear (un número entero): "))

    # Validación para asegurarse de que el número de pasos es al menos igual
    # al número de procesos
    if n < num_procesos:
        print("Error: El número de pasos no puede ser menor que el número de procesos.")
        return

    # Distancia total que abarca cada proceso
    Dx_proceso = (b-a) / num_procesos
    lista_procesos = []

    t0 = time()
    for i in range(num_procesos):
        # Distintos valores de a y b según el intervalo del que se ocupa
        # cada proceso
        p = CalcularSubareaProceso(
            a + i * Dx_proceso, a + (i + 1) * Dx_proceso, n // num_procesos)
        lista_procesos.append(p)
        p.start()

    for proceso in lista_procesos:
        # Esperamos así a que todos los procesos hijos terminen su ejecución
        proceso.join()

    # Sumar todas las subáreas una vez que los procesos han terminado
    area_total = sum(proceso.subarea for proceso in lista_procesos)
    t1 = time()

    tiempo_ejecucion = t1 - t0

    print(f"La integral definida de la función en el intervalo a-b dado para {n}"
          f" pasos y {num_procesos} procesos es:", abs(area_total))
    print(f"El tiempo de ejecución ha sido de {tiempo_ejecucion:.8f} segundos.")


if __name__ == "__main__":
    try:
        main()
        input("\nPulse <Intro> para salir.")
    except Exception as e:
        if type(e) != FileNotFoundError:
            # Avisamos al usuario de cualquier posible error
            print("Se ha producido un error inesperado:", e)
            input("\nPulse <Intro> para salir.")
