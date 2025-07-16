import random
from matriz_nivel_beta import boards_nivelB
from collections import deque

def generar_laberinto():
    filas = len(boards_nivelB)
    columnas = len(boards_nivelB[0])

    zona_cruz = [[1 if boards_nivelB[i][j] != 0 else 0 for j in range(columnas)] for i in range(filas)]
    matriz = [[9 for _ in range(columnas)] for _ in range(filas)]

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

        random.shuffle(celdas_cruz)
        for posible_inicio in celdas_cruz:
            f, c = posible_inicio
            if any(
                1 <= f + dr < filas - 1 and 1 <= c + dc < columnas - 1 and zona_cruz[f + dr][c + dc] == 1
                for dr, dc in dirs
            ):
                inicio = posible_inicio
                break
        else:
            return generar()

        dfs(*inicio)

        def bfs_mas_lejano(desde):
            queue = deque([(desde, 0)])
            visitados = {desde}
            mas_lejano = (desde, 0)
            while queue:
                nodo, dist = queue.popleft()
                if dist > mas_lejano[1]:
                    mas_lejano = (nodo, dist)
                for vecino in conexiones.get(nodo, []):
                    if vecino not in visitados:
                        visitados.add(vecino)
                        queue.append((vecino, dist + 1))
            return mas_lejano[0], visitados

        _, alcanzables = bfs_mas_lejano(inicio)

        # 🧠 Elegir la mejor salida estratégica
        def elegir_salida_inteligente():
            candidatos = []
            for (i, j) in alcanzables:
                if matriz[i][j] == 0:
                    conexiones_vecinas = sum(
                        1 for dr, dc in dirs
                        if (i + dr, j + dc) in alcanzables and matriz[i + dr // 2][j + dc // 2] == 0
                    )
                    en_borde = i == 1 or i == filas - 2 or j == 1 or j == columnas - 2
                    puntuacion = (conexiones_vecinas + (0 if en_borde else 2))  # penaliza zonas centrales
                    candidatos.append(((i, j), puntuacion))

            candidatos.sort(key=lambda x: x[1])
            return candidatos[0][0] if candidatos else random.choice(list(alcanzables))

        salida = elegir_salida_inteligente()

        # ✅ RECONEXIÓN INTELIGENTE PARA ELIMINAR CALLEJONES
        def reconectar_callejones():
            for (i, j) in list(conexiones.keys()):
                if len(conexiones[(i, j)]) < 2:
                    random.shuffle(dirs)
                    for dr, dc in dirs:
                        ni, nj = i + dr, j + dc
                        pi, pj = i + dr // 2, j + dc // 2
                        if (
                            1 <= ni < filas - 1 and 1 <= nj < columnas - 1 and
                            zona_cruz[ni][nj] == 1 and
                            matriz[ni][nj] == 0 and
                            (ni, nj) not in conexiones[(i, j)]
                        ):
                            conexiones[(i, j)].append((ni, nj))
                            conexiones[(ni, nj)].append((i, j))
                            matriz[pi][pj] = 0
                            break

        reconectar_callejones()
        reconectar_callejones()

        sf, sc = salida
        matriz[sf][sc] = 10  # salida

        for i in range(filas):
            for j in range(columnas):
                if matriz[i][j] == 0:
                    matriz[i][j] = random.choices([1, 2], [0.9, 0.1])[0]
                elif zona_cruz[i][j] == 1 and matriz[i][j] not in [1, 2, 10]:
                    matriz[i][j] = 4
                elif zona_cruz[i][j] == 0:
                    matriz[i][j] = 9

        return matriz

    return generar()
















