import random
import time

def contar_conflictos(tablero):
    conflictos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1
    return conflictos        

def mostrar_matriz(tablero, titulo="Tablero"):
    print(f"\n--- {titulo} ---")
    print("  " + " ".join(str(c) for c in range(8)))
    for fila in range(8):
        linea = f"{fila} "
        for col in range(8):
            if tablero[col] == fila:
                linea += "Q "
            else:
                linea += ". "
        print(linea)
    print()

def algoritmo_tabu(tablero_inicial=None):
    if tablero_inicial:
        tablero = list(tablero_inicial)
    else:
        tablero = random.sample(range(8), 8)

    mejor_tablero = list(tablero)
    menor_conflictos = contar_conflictos(tablero)   

    lista_tabu = []
    iteraciones = 0
    inicio = time.perf_counter()

    while menor_conflictos > 0 and iteraciones < 500:
        iteraciones += 1

        vecino_seleccionado = None
        conflictos_vecino = 999
        movimiento_seleccionado = None

        # Generar vecinos intercambiando las posiciones
        for i in range(8):
            for j in range(i + 1, 8):
                nuevo_tablero = list(tablero)
                nuevo_tablero[i], nuevo_tablero[j] = nuevo_tablero[j], nuevo_tablero[i]
                conflictos_nuevos = contar_conflictos(nuevo_tablero)
                movimiento = (i, j)

                # Verificar si el movimiento está en la lista tabú
                en_iteraciones = (movimiento in lista_tabu) or ((j, i) in lista_tabu)
                es_mejor = conflictos_nuevos < menor_conflictos

                # Criterio de aceptación
                if not en_iteraciones or es_mejor:
                    if conflictos_nuevos < conflictos_vecino:
                        conflictos_vecino = conflictos_nuevos
                        vecino_seleccionado = nuevo_tablero
                        movimiento_seleccionado = movimiento

        if vecino_seleccionado is None:
            break

        tablero = vecino_seleccionado

        # Actualizar el mejor tablero encontrado
        if conflictos_vecino < menor_conflictos:
            mejor_tablero = list(tablero)
            menor_conflictos = conflictos_vecino

        # Actualizar la lista tabú
        lista_tabu.append(movimiento_seleccionado)
        if len(lista_tabu) > 5:
            lista_tabu.pop(0)

    tiempo_total = time.perf_counter() - inicio
    return mejor_tablero, menor_conflictos, iteraciones, tiempo_total

print("Algoritmo Tabu para el problema de las 8 reinas")
respuesta = input("¿Ingresar un tablero inicial? (s/n): ").strip().lower()

if respuesta == 's':
    entrada = input("Ingrese las posiciones de las reinas (ej: 0 1 2 3 4 5 6 7): ")
    tablero_partida = [int(x) for x in entrada.split()]
else:
    print("Se va a generar un tablero inicial aleatorio")
    tablero_partida = random.sample(range(8), 8)
    print("Tablero aleatorio generado:", tablero_partida)

# Mostrar tablero inicial
mostrar_matriz(tablero_partida, "Tablero Inicial")

# Ejecutar el algoritmo
resultado, total_conflictos, total_iteraciones, tiempo = algoritmo_tabu(tablero_partida)

# Mostrar tablero final y métricas
mostrar_matriz(resultado, "Mejor Tablero Encontrado")
print("Mejor tablero encontrado:", resultado)
print("Total de conflictos:", total_conflictos)
print("Total de iteraciones:", total_iteraciones)
print("Tiempo de ejecución:", round(tiempo, 5), "segundos")