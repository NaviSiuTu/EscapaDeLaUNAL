import random
from matriz_nivel_beta import boards_nivelB
from collections import deque

def generar_laberinto_con_salida():
    filas = len(boards_nivelB)
    columnas = len(boards_nivelB[0])

    zona_cruz = [[1 if boards_nivelB[i][j] != 0 else 0 for j in range(columnas)] for i in range(filas)]
    matriz = [[9 for _ in range(columnas)] for _ in range(filas)]

    dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    celdas_cruz = [(i, j) for i in range(filas) for j in range(columnas)
                   if zona_cruz[i][j] == 1 and i % 2 == 1 and j % 2 == 1]
    
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

    # === Paso 1: DFS desde centro ===
    centro = len(celdas_cruz) // 2
    inicio = celdas_cruz[centro]
    dfs(*inicio)

    # === Paso 2: BFS para encontrar el punto más lejano ===
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
        return mas_lejano[0]

    salida = bfs_mas_lejano(inicio)
    sf, sc = salida
    matriz[sf][sc] = 10  # salida

    # === Paso 3: Rellenar con monedas ===
    for i in range(filas):
        for j in range(columnas):
            if matriz[i][j] == 0:
                matriz[i][j] = random.choices([1, 2], [0.9, 0.1])[0]
            elif zona_cruz[i][j] == 1 and matriz[i][j] not in [1, 2, 10]:
                matriz[i][j] = 4  # muro interno
            elif zona_cruz[i][j] == 0:
                matriz[i][j] = 9  # fondo

    return matriz














