import random
from board_mapa_453 import board as nivel_453
from collections import deque

def generar_laberinto_con_salida():
    filas = len(nivel_453)
    columnas = len(nivel_453[0])

    zona_cruz = [[1 if nivel_453[i][j] != 0 else 0 for j in range(columnas)] for i in range(filas)]
    matriz = [[9 for _ in range(columnas)] for _ in range(filas)]  # 9 = pared por defecto

    dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    celdas_cruz = [(i, j) for i in range(filas) for j in range(columnas)
                   if zona_cruz[i][j] == 1 and i % 2 == 1 and j % 2 == 1]

    def generar():
        visitado = set()
        conexiones = {}

        def es_valida(f, c):
            return (
                1 <= f < filas - 1 and
                1 <= c < columnas - 1 and
                zona_cruz[f][c] == 1 and
                (f, c) not in visitado
            )

        def dfs(f, c):
            visitado.add((f, c))
            matriz[f][c] = 0
            conexiones[(f, c)] = []
            vecinos = dirs[:]
            random.shuffle(vecinos)
            for dr, dc in vecinos:
                nf, nc = f + dr, c + dc
                pf, pc = f + dr // 2, c + dc // 2
                if es_valida(nf, nc):
                    matriz[pf][pc] = 0
                    conexiones[(f, c)].append((nf, nc))
                    conexiones.setdefault((nf, nc), []).append((f, c))
                    dfs(nf, nc)

        # Elegir un punto de inicio válido
        random.shuffle(celdas_cruz)
        for posible_inicio in celdas_cruz:
            f, c = posible_inicio
            vecinos_disponibles = 0
            for dr, dc in dirs:
                nf, nc = f + dr, c + dc
                if 1 <= nf < filas-1 and 1 <= nc < columnas-1 and zona_cruz[nf][nc] == 1:
                    vecinos_disponibles += 1
            if vecinos_disponibles > 0:
                inicio = posible_inicio
                break
        else:
            return generar()  # intenta de nuevo si no encuentra inicio válido

        dfs(*inicio)

        # BFS para encontrar punto más lejano como salida
        def bfs_mas_lejano(desde):
            queue = deque([(desde, 0)])
            visitados = {desde}
            mas_lejano = (desde, 0)
            while queue:
                (nodo, dist) = queue.popleft()
                if dist > mas_lejano[1]:
                    mas_lejano = (nodo, dist)
                for vecino in conexiones.get(nodo, []):
                    if vecino not in visitados:
                        visitados.add(vecino)
                        queue.append((vecino, dist + 1))
            return mas_lejano[0], visitados

        salida, alcanzables = bfs_mas_lejano(inicio)

        if salida not in alcanzables:
            return generar()  # reinicia si no hay salida válida

        sf, sc = salida
        matriz[sf][sc] = 10  # marca la salida

        # Rellenar con monedas, poderes y paredes
        for i in range(filas):
            for j in range(columnas):
                if matriz[i][j] == 0:
                    matriz[i][j] = random.choices([1, 2], [0.9, 0.1])[0]
                elif zona_cruz[i][j] == 1 and matriz[i][j] not in [1, 2, 10]:
                    matriz[i][j] = 4  # pared secundaria
                elif zona_cruz[i][j] == 0:
                    matriz[i][j] = 9  # pared total

        return matriz

    return generar()
