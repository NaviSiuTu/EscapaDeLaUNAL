import pygame
import math
import sys
import os
import heapq
import random
from board_mapa_453 import board as level

pygame.init()

# Tamaño de celda
CELL_COLS = len(level[0])
CELL_ROWS = len(level)
CELL_WIDTH = 16
CELL_HEIGHT = 16
Ventana_Ancho = CELL_COLS * CELL_WIDTH
Ventana_Altura = CELL_ROWS * CELL_HEIGHT + 50

Display_Surface = pygame.display.set_mode((Ventana_Ancho, Ventana_Altura))
pygame.display.set_caption("Nivel Mapa 453")

reloj = pygame.time.Clock()
fps = 60
PI = math.pi

uid = "UID_DUMMY"
puntaje = 0

# ======== CARGA DE IMÁGENES ========
buho_img = pygame.transform.scale(pygame.image.load("Assets1/Buho test.png"), (CELL_WIDTH, CELL_HEIGHT))
cabra_img = pygame.transform.scale(pygame.image.load("Assets1/Cabra test.png"), (CELL_WIDTH, CELL_HEIGHT))

def is_wall(row, col):
    if 0 <= row < len(level) and 0 <= col < len(level[0]):
        return level[row][col] in [3, 4, 5, 6, 7, 8, 9]
    return True

class Jugador:
    def __init__(self, img, fila, col):
        self.imagen = img
        self.fila = fila
        self.col = col
        self.dir = [0, 0]
        self.intencion = [0, 0]
        self.trail = []

    def agregar_estela(self):
        self.trail.append({"fila": self.fila, "col": self.col, "alpha": 255})

    def dibujar_estela(self):
        for p in self.trail:
            surf = pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
            surf.set_alpha(p["alpha"])
            surf.fill((255, 255, 0))
            Display_Surface.blit(surf, (p["col"] * CELL_WIDTH, p["fila"] * CELL_HEIGHT))
            p["alpha"] -= 25
        self.trail = [p for p in self.trail if p["alpha"] > 0]

    def mover(self, dx, dy):
        self.intencion = [dx, dy]

    def actualizar(self):
        global puntaje

        nueva_fila = self.fila + self.intencion[1]
        nueva_col = self.col + self.intencion[0]
        if not is_wall(nueva_fila, nueva_col):
            self.dir = self.intencion

        nueva_fila = self.fila + self.dir[1]
        nueva_col = self.col + self.dir[0]
        if not is_wall(nueva_fila, nueva_col):
            self.agregar_estela()
            self.fila, self.col = nueva_fila, nueva_col

            if [self.fila, self.col] == cabra_pos:
                pygame.quit()
                sys.exit()

            valor = level[self.fila][self.col]
            if valor == 1:
                puntaje += 1
                level[self.fila][self.col] = 0
            elif valor == 2:
                puntaje += 5
                level[self.fila][self.col] = 0

    def dibujar(self):
        Display_Surface.blit(self.imagen, (self.col * CELL_WIDTH, self.fila * CELL_HEIGHT))

spawn_tiles = [(i, j) for i in range(len(level)) for j in range(len(level[0])) if level[i][j] == 1]
spawn_fila, spawn_col = random.choice(spawn_tiles)
jugador = Jugador(buho_img, spawn_fila, spawn_col)

# Cabra
bolitas = [(i, j) for i in range(len(level)) for j in range(len(level[0])) if level[i][j] == 1]
cabra_pos = list(random.choice(bolitas))
cabra_tick = 0
cabra_tick_max = 10

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristica(start, goal)}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        vecinos = [(current[0]+1, current[1]), (current[0]-1, current[1]),
                   (current[0], current[1]+1), (current[0], current[1]-1)]
        for vecino in vecinos:
            if is_wall(*vecino):
                continue
            temp_g = g_score[current] + 1
            if vecino not in g_score or temp_g < g_score[vecino]:
                came_from[vecino] = current
                g_score[vecino] = temp_g
                f_score[vecino] = temp_g + heuristica(vecino, goal)
                heapq.heappush(open_set, (f_score[vecino], vecino))
    return []

def mover_cabra():
    global cabra_tick, cabra_pos
    cabra_tick += 1
    if cabra_tick < cabra_tick_max:
        return
    cabra_tick = 0
    camino = astar(tuple(cabra_pos), (jugador.fila, jugador.col))
    if camino and len(camino) > 0:
        siguiente = camino[0]
        cabra_pos = list(siguiente)

def draw_board(lvl):
    colorTEST = (3, 115, 17)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            valor = lvl[i][j]
            cx = j * CELL_WIDTH + (0.5 * CELL_WIDTH)
            cy = i * CELL_HEIGHT + (0.5 * CELL_HEIGHT)
            if valor == 1:
                pygame.draw.circle(Display_Surface, (255, 255, 0), (int(cx), int(cy)), 4)
            elif valor == 2:
                pygame.draw.circle(Display_Surface, (255, 165, 0), (int(cx), int(cy)), 7)
            elif valor == 3:
                pygame.draw.line(Display_Surface, colorTEST, (cx, i * CELL_HEIGHT), (cx, i * CELL_HEIGHT + CELL_HEIGHT), 3)
            elif valor == 4:
                pygame.draw.line(Display_Surface, colorTEST, (j * CELL_WIDTH, cy), (j * CELL_WIDTH + CELL_WIDTH, cy), 3)
            elif valor == 5:
                pygame.draw.arc(Display_Surface, colorTEST, [(j * CELL_WIDTH - (CELL_WIDTH * 0.23)) - 2, cy, CELL_WIDTH, CELL_HEIGHT], 0, PI / 2, 3)
            elif valor == 6:
                pygame.draw.arc(Display_Surface, colorTEST, [(j * CELL_WIDTH + (CELL_WIDTH * 0.38)) + 2, cy + 2, CELL_WIDTH, CELL_HEIGHT], PI / 2, PI, 3)
            elif valor == 7:
                pygame.draw.arc(Display_Surface, colorTEST, [(j * CELL_WIDTH + (CELL_WIDTH * 0.52)) + 0.9, (i * CELL_HEIGHT - (0.45 * CELL_HEIGHT)) + 1.3, CELL_WIDTH, CELL_HEIGHT], PI, 3 * PI / 2, 3)
            elif valor == 8:
                pygame.draw.arc(Display_Surface, colorTEST, [(j * CELL_WIDTH - (CELL_WIDTH * 0.105)) - 0.7, (i * CELL_HEIGHT - (0.4 * CELL_HEIGHT)) - 0.7, CELL_WIDTH, CELL_HEIGHT], 3 * PI / 2, 2 * PI, 3)
            elif valor == 9:
                pygame.draw.line(Display_Surface, "white", (j * CELL_WIDTH, cy), (j * CELL_WIDTH + CELL_WIDTH, cy), 3)

def main():
    corriendo = True
    while corriendo:
        reloj.tick(fps)
        Display_Surface.fill((4, 17, 4))
        draw_board(level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    jugador.mover(-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    jugador.mover(1, 0)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    jugador.mover(0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    jugador.mover(0, 1)

        jugador.actualizar()
        mover_cabra()
        jugador.dibujar_estela()
        jugador.dibujar()

        # Dibuja la cabra
        Display_Surface.blit(cabra_img, (cabra_pos[1] * CELL_WIDTH, cabra_pos[0] * CELL_HEIGHT))

        # Colisión
        if [jugador.fila, jugador.col] == cabra_pos:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()

