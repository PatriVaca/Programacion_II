#!/usr/bin/python3
# -*- coding: utf-8 -*-

##################################################
# Autora: Patricia del Carmen Vaca Rubio         #
# Cuestionario individual 2. Mejora de imágenes  #
# Versión: Paralelización con procesos           #
##################################################

import sys
from time import time
from multiprocessing import Process, Value, Array


def readfile(filename: str):
    try:
        with open(filename, "r") as fin:
            magic_number = fin.readline().strip()

            if magic_number != "P3":
                print(f"El archivo {filename} no es un PPM ASCII válido.")
                sys.exit(1)

            width, height = map(int, fin.readline().strip().split())
            max_value = int(fin.readline().strip())

            pixels = []
            lines = fin.readlines()  # sin el header ya
            for line in lines:
                pixels.extend(list(map(int, line.split())))

            pixels_array = Array("i", pixels, lock=False)

    except FileNotFoundError:
        print(
            f"Error. El archivo {filename} no se encuentra en su directorio actual.")
        sys.exit(1)
    except Exception as e:
        print(f"Ha ocurrido un error de tipo: ", e)
        sys.exit(1)

    return width, height, max_value, pixels_array


def find_min_max(start, end, pixels_array, global_min_red, global_max_red,
                 global_min_green, global_max_green, global_min_blue, global_max_blue):

    red_channel_fragment = pixels_array[start: end: 3]
    green_channel_fragment = pixels_array[start + 1: end: 3]
    blue_channel_fragment = pixels_array[start + 2: end: 3]

    # Canal rojo
    local_min_red = min(red_channel_fragment)
    local_max_red = max(red_channel_fragment)

    if local_min_red < global_min_red.value:
        global_min_red.value = local_min_red

    if local_max_red > global_max_red.value:
        global_max_red.value = local_max_red

    # Canal verde
    local_min_green = min(green_channel_fragment)
    local_max_green = max(green_channel_fragment)

    if local_min_green < global_min_green.value:
        global_min_green.value = local_min_green

    if local_max_green > global_max_green.value:
        global_max_green.value = local_max_green

    # Canal azul
    local_min_blue = min(blue_channel_fragment)
    local_max_blue = max(blue_channel_fragment)

    if local_min_blue < global_min_blue.value:
        global_min_blue.value = local_min_blue

    if local_max_blue > global_max_blue.value:
        global_max_blue.value = local_max_blue


def normalize_pixels(start, end, pixels_array, global_min_red, global_max_red,
                     global_min_green, global_max_green, global_min_blue,
                     global_max_blue, pixels_array_norm):

    # Componentes rojos de los píxeles
    for i in range(start, end, 3):
        val_norm_red = int(
            (pixels_array[i] - global_min_red.value) / (global_max_red.value - global_min_red.value) * 255)
        pixels_array_norm[i] = val_norm_red

    # Componentes verdes de los píxeles
    for i in range(start + 1, end, 3):
        val_norm_green = int(
            (pixels_array[i] - global_min_green.value) / (global_max_green.value - global_min_green.value) * 255)
        pixels_array_norm[i] = val_norm_green

    # Componentes azules de los píxeles
    for i in range(start + 2, end, 3):
        val_norm_blue = int(
            (pixels_array[i] - global_min_blue.value) / (global_max_blue.value - global_min_blue.value) * 255)
        pixels_array_norm[i] = val_norm_blue


def writepgm(filename, width, height, max_value, pixels_array_norm):
    filename_splitted = filename.split(".")
    # Para quedarme únicamente con el nombre y no la extensión del archivo
    new_filename = filename_splitted[0]
    with open(new_filename + "_normalizada.ppm", "w") as fout:
        fout.write("P3\n") # Mismo tipo de imagen de salida
        fout.write(f"{width} {height}\n")  # Mismas dimensiones de la imagen
        fout.write(f"{max_value}\n")  # Misma profundidad de color

        for i in range(0, len(pixels_array_norm), width):
            # Escritura de cada línea de píxeles:
            fout.write(
                " ".join(map(str, pixels_array_norm[i: i+width])) + "\n")


def main():
    print("Este programa realiza un tratamiento de mejora de una imagen (fichero"
          " 'ppm' en formato 'ASCII') por medio de la ampliación de su histograma."
          " La ejecución del programa puede realizarse en paralelo con el número"
          " de procesos que indique.")
    filename = input("Por favor, introduzca el nombre del fichero 'ppm' en"
                     " formato 'ASCII' del que desea ampliar su histograma: ")
    processes_num = int(input("Por favor, introduzca el número de procesos de"
                              " ejecución en paralelo: "))

    t0 = time()

    print("*Leyendo fichero...")
    width, height, max_value, pixels_array = readfile(filename)

    # Para el componente rojo de los píxeles
    global_min_red = Value("i", 255, lock=False)
    global_max_red = Value("i", 0, lock=False)

    # Para el componente verde de los píxeles
    global_min_green = Value("i", 255, lock=False)
    global_max_green = Value("i", 0, lock=False)

    # Para el componente azul de los píxeles
    global_min_blue = Value("i", 255, lock=False)
    global_max_blue = Value("i", 0, lock=False)

    print("Total de píxeles(multiplicadox3 por rgb por pixel):")
    print(len(pixels_array))

    ### PARALELIZACIÓN FIND_MIN_MAX ###
    print("*Encontrando los valores máximo y mínimo de cada canal de color...")

    # Número de píxeles de los que se ocupará cada proceso
    fragment_size = (len(pixels_array) // 3) // processes_num

    processes = []
    for i in range(processes_num):
        start = i * 3 * fragment_size  # Cada pixel cuenta con 3 valores (rgb)
        # Si el número total de píxeles no se puede dividir uniformemente entre
        # los procesos, el último proceso podría necesitar manejar más píxeles
        # para abarcar todos los datos.
        if i != processes_num - 1:  # Si no se trata del último proceso
            end = (i + 1) * 3 * fragment_size
        else:  # Si se trata del último proceso
            # Llega hasta el final del array para los posibles píxeles sobrantes
            end = len(pixels_array)

        p = Process(target=find_min_max, args=(start, end, pixels_array, global_min_red,
                    global_max_red, global_min_green, global_max_green, global_min_blue,
                    global_max_blue))
        processes.append(p)
        p.start()

    for p in processes:
        # El proceso padre espera a que finalice la ejecución de los procesos hijos
        p.join()

    ### PARALELIZACIÓN NORMALIZACIÓN PÍXELES ###
    print("*Normalizando la imagen...")
    pixels_array_norm = Array("i", len(pixels_array), lock=False)

    processes = []
    for i in range(processes_num):
        start = i * 3 * fragment_size
        if i != processes_num - 1:
            end = (i + 1) * 3 * fragment_size
        else:
            end = len(pixels_array)

        p = Process(target=normalize_pixels, args=(start, end, pixels_array,
                    global_min_red, global_max_red, global_min_green, global_max_green,
                    global_min_blue, global_max_blue, pixels_array_norm))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    ### Exportación de la imagen normalizada ('mejorada') ###
    writepgm(filename, width, height, max_value, pixels_array_norm)

    t1 = time()
    execution_time = t1 - t0
    print(f"El tiempo de ejecución del programa para {processes_num} procesos"
          f" ha sido: {execution_time} segundos.")


if __name__ == "__main__":
    try:
        main()
        input("\nPulse <Intro> para salir.")
    except Exception as e:
        # Avisamos al usuario de cualquier posible error
        print("Se ha producido un error inesperado:", e)
        input("\nPulse <Intro> para salir.")
