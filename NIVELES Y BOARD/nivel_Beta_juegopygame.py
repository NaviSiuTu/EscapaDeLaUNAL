import pygame
import math
import sys
import os
import heapq
import random
from matriz_nivel_beta import boards_nivelB
import subprocess

pygame.init()

# === Dimensiones base de la ventana ===
BASE_ANCHO = 398
BASE_ALTO = 736
Display_Surface = pygame.display.set_mode((BASE_ANCHO, BASE_ALTO))
pygame.display.set_caption("Nivel Beta")

# === Reloj y fuente ===
reloj = pygame.time.Clock()
fps = 60
font = pygame.font.Font("Assets1/Minecraft.ttf", 16)

# =================== FUNCIONES PANTALLA INICIO ===================
def cortina_entrada(surface, fondo):
    paso = 20
    for ancho in range(BASE_ANCHO // 2, -1, -paso):
        surface.blit(fondo, (0, 0))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, ancho, BASE_ALTO))
        pygame.draw.rect(surface, (0, 0, 0), (BASE_ANCHO - ancho, 0, ancho, BASE_ALTO))
        pygame.display.flip()
        pygame.time.delay(20)

def mostrar_pantalla_inicio():
    frases_buho = [
        "Ey, ya calentaste motores o todavia estas en Bienestar?",
        "Trajiste la tula o vienes sin poderes?",
        "Hoy si le das con toda... o te devuelves al menu?",
        "Pilas, que esta cabra no se doma con un cafecito.",
        "Esto no es clase, aqui si te toca correr.",
        "Con fe, como buscando cupo en electiva libre.",
        "Ni el de fisica II corre tan rapido como la cabra.",
        "Que no se diga que lo tuyo fue relleno.",
        "Un paso mas y te graduas del Nivel Alpha... o no.",
        "No hay simulacro aqui, solo fuego real.",
        "Estas mas listo que cafeteria a las 7 a.m.?",
        "Te crees el mas teso? La cabra tambien.",
        "Aqui no hay recuperatorio, solo una vida."
    ]

    fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png").convert()
    fondo = pygame.transform.scale(fondo, (BASE_ANCHO, BASE_ALTO))

    buho_inicio = pygame.image.load("Assets1/Buho test.png").convert_alpha()
    buho_inicio = pygame.transform.scale(buho_inicio, (80, 80))

    Display_Surface.fill((0, 0, 0))
    cortina_entrada(Display_Surface, fondo)

    frase = random.choice(frases_buho)
    esperando = True

    while esperando:
        Display_Surface.blit(fondo, (0, 0))

        buho_x = 60
        buho_y = BASE_ALTO // 2 - 50
        caja_x = buho_x + 90
        caja_y = buho_y + 10
        caja_w = BASE_ANCHO - caja_x - 30
        caja_h = 80

        Display_Surface.blit(buho_inicio, (buho_x, buho_y))
        pygame.draw.rect(Display_Surface, (0, 0, 0), (caja_x, caja_y, caja_w, caja_h))
        pygame.draw.rect(Display_Surface, (255, 255, 255), (caja_x, caja_y, caja_w, caja_h), 2)

        palabras = frase.split()
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            test = linea_actual + palabra + " "
            if font.size(test)[0] < caja_w - 20:
                linea_actual = test
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)

        for i, linea in enumerate(lineas[:3]):
            texto = font.render(linea.strip(), True, (255, 255, 255))
            Display_Surface.blit(texto, (caja_x + 10, caja_y + 10 + i * 22))

        titulo = font.render("¿Estás listo para comenzar?", True, (255, 255, 255))
        Display_Surface.blit(titulo, (BASE_ANCHO // 2 - titulo.get_width() // 2, 80))

        boton_jugar = pygame.Rect(BASE_ANCHO // 2 - 120, BASE_ALTO - 140, 100, 40)
        boton_volver = pygame.Rect(BASE_ANCHO // 2 + 20, BASE_ALTO - 140, 100, 40)

        pygame.draw.rect(Display_Surface, (0, 255, 0), boton_jugar)
        pygame.draw.rect(Display_Surface, (255, 0, 0), boton_volver)

        txt_jugar = font.render("JUGAR", True, (0, 0, 0))
        txt_volver = font.render("VOLVER", True, (0, 0, 0))

        Display_Surface.blit(txt_jugar, (boton_jugar.centerx - txt_jugar.get_width() // 2,
                                         boton_jugar.centery - txt_jugar.get_height() // 2))
        Display_Surface.blit(txt_volver, (boton_volver.centerx - txt_volver.get_width() // 2,
                                          boton_volver.centery - txt_volver.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    for ancho in range(0, BASE_ANCHO // 2 + 20, 20):
                        Display_Surface.blit(fondo, (0, 0))
                        pygame.draw.rect(Display_Surface, (0, 0, 0), (0, 0, ancho, BASE_ALTO))
                        pygame.draw.rect(Display_Surface, (0, 0, 0), (BASE_ANCHO - ancho, 0, ancho, BASE_ALTO))
                        pygame.display.flip()
                        pygame.time.delay(20)
                    esperando = False
                elif boton_volver.collidepoint(event.pos):
                    pygame.quit()
                    os.system(f"python CONPY/niveles_pygame.py {uid}")
                    sys.exit()

# =================== BLOQUE DE EJECUCIÓN ===================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        uid = sys.argv[1]
    else:
        uid = "UID_DUMMY"

    mostrar_pantalla_inicio()

    # === Solo después del búho aplicamos el zoom del nivel ===
    ESCALA = 1.2
    level = boards_nivelB

    colorTEST = (3, 115, 17)
    PI = math.pi

    CELDAS_H = len(level[0])
    CELDAS_V = len(level)

    CELL_WIDTH = int((BASE_ANCHO // CELDAS_H) * ESCALA)
    CELL_HEIGHT = int(((BASE_ALTO - 50) // CELDAS_V) * ESCALA)

    Ventana_Ancho = CELL_WIDTH * CELDAS_H
    Ventana_Altura = CELL_HEIGHT * CELDAS_V + 50
    Display_Surface = pygame.display.set_mode((Ventana_Ancho, Ventana_Altura))


if len(sys.argv) > 1:
    uid = sys.argv[1]
else:
    uid = "UID_DUMMY"

# === Poderes ===
poder_tula = False
poder_tinto = False
poder_sticker = False
poder_tinto_timer = 0
poder_sticker_timer = 0
puntaje = 0

if os.path.exists("poder_activo.txt"):
    with open("poder_activo.txt", "r") as f:
        poder = f.read().strip()
        if poder == "Tula Bienestar UN":
            poder_tula = True
        elif poder == "Tinto cafeteria UNAL":
            poder_tinto = True
            poder_tinto_timer = pygame.time.get_ticks()
        elif poder == "Sticker UNAL":
            poder_sticker = True
            poder_sticker_timer = pygame.time.get_ticks()
    os.remove("poder_activo.txt")

# === Botones ===
boton_pausa = pygame.Rect(Ventana_Ancho - 90, 10, 80, 30)
boton_bolsa = pygame.Rect(Ventana_Ancho - 180, 10, 80, 30)

# === Imágenes ===
buho_img = pygame.image.load("Assets1/Buho test.png")
buho_img = pygame.transform.scale(buho_img, (CELL_WIDTH, CELL_HEIGHT))

cabra_img = pygame.image.load("Assets1/Cabra test.png")
cabra_img = pygame.transform.scale(cabra_img, (CELL_WIDTH, CELL_HEIGHT))

moneda_pequeña = pygame.image.load("Assets1/MonedaP_test.png").convert_alpha()
moneda_grande = pygame.image.load("Assets1/Moneda_test.png").convert_alpha()
moneda_pequeña = pygame.transform.scale(moneda_pequeña, (12, 12))
moneda_grande = pygame.transform.scale(moneda_grande, (20, 20))


# =================== CLASE JUGADOR ===================
class Jugador:
    def __init__(self, img, fila, col):
        self.imagen = img
        self.fila = fila
        self.col = col
        self.dir = [0, 0]
        self.deslizando = False
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

    def actualizar(self):
        global puntaje, poder_tula
        pasos = 5 if poder_tinto else 3
        for _ in range(pasos):
            if self.deslizando:
                nueva_fila = self.fila + self.dir[1]
                nueva_col = self.col + self.dir[0]
                if not is_wall(nueva_fila, nueva_col):
                    self.agregar_estela()
                    self.fila, self.col = nueva_fila, nueva_col
                    if [self.fila, self.col] == cabra_pos:
                        if poder_tula:
                            poder_tula = False
                        else:
                            mostrar_game_over()
                    valor = level[self.fila][self.col]
                    if valor == 1:
                        puntaje += 1
                        level[self.fila][self.col] = 0
                    elif valor == 2:
                        puntaje += 5
                        level[self.fila][self.col] = 0
                else:
                    self.deslizando = False

    def mover(self, dx, dy):
        self.dir = [dx, dy]
        self.deslizando = True

    def dibujar(self):
        x = self.col * CELL_WIDTH
        y = self.fila * CELL_HEIGHT
        Display_Surface.blit(self.imagen, (x, y))

# Buscar primer espacio con moneda amarilla (valor 1)
pos_inicial = next(((i, j) for i in range(len(level)) for j in range(len(level[0])) if level[i][j] == 1), (2, 2))
jugador = Jugador(buho_img, pos_inicial[0], pos_inicial[1])


# === Cabra enemiga ===
bolitas = [(i, j) for i in range(len(level)) for j in range(len(level[0])) if level[i][j] == 1]
cabra_pos = list(random.choice(bolitas))
cabra_tick = 0
cabra_tick_max = 10

def is_wall(row, col):
    if 0 <= row < len(level) and 0 <= col < len(level[0]):
        return level[row][col] in [3, 4, 5, 6, 7, 8, 9]
    return True

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
    cabra_tick = 6

    if poder_sticker:
        dx = cabra_pos[0] - jugador.fila
        dy = cabra_pos[1] - jugador.col
        nueva = (cabra_pos[0] + dx, cabra_pos[1] + dy)
        if not is_wall(*nueva):
            cabra_pos = list(nueva)
    else:
        camino = astar(tuple(cabra_pos), (jugador.fila, jugador.col))
        if camino and len(camino) > 0:
            siguiente = camino[0]
            cabra_pos = list(siguiente)

def draw_board(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            valor = lvl[i][j]
            cx = j * CELL_WIDTH + (0.5 * CELL_WIDTH)
            cy = i * CELL_HEIGHT + (0.5 * CELL_HEIGHT)
            if valor == 1:
                Display_Surface.blit(moneda_pequeña, (cx - 6, cy - 6))
            elif valor == 2:
                Display_Surface.blit(moneda_grande, (cx - 10, cy - 10))
            elif valor == 3:
                pygame.draw.line(Display_Surface, colorTEST, (cx, i * CELL_HEIGHT), (cx, i * CELL_HEIGHT + CELL_HEIGHT), 3)
            elif valor == 4:
                pygame.draw.line(Display_Surface, colorTEST, (j * CELL_WIDTH, cy), (j * CELL_WIDTH + CELL_WIDTH, cy), 3)
            elif valor == 5:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * CELL_WIDTH - (CELL_WIDTH * 0.23)) - 2, cy, CELL_WIDTH, CELL_HEIGHT],
                                0, PI / 2, 3)
            elif valor == 6:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * CELL_WIDTH + (CELL_WIDTH * 0.38)) + 2, cy + 2, CELL_WIDTH, CELL_HEIGHT],
                                PI / 2, PI, 3)
            elif valor == 7:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * CELL_WIDTH + (CELL_WIDTH * 0.52)) + 0.9, (i * CELL_HEIGHT - (0.45 * CELL_HEIGHT)) + 1.3, CELL_WIDTH, CELL_HEIGHT],
                                PI, 3 * PI / 2, 3)
            elif valor == 8:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * CELL_WIDTH - (CELL_WIDTH * 0.105)) - 0.7, (i * CELL_HEIGHT - (0.4 * CELL_HEIGHT)) - 0.7, CELL_WIDTH, CELL_HEIGHT],
                                3 * PI / 2, 2 * PI, 3)
            elif valor == 9:
                pygame.draw.line(Display_Surface, "white", (j * CELL_WIDTH, cy), (j * CELL_WIDTH + CELL_WIDTH, cy), 3)

def mostrar_pausa():
    overlay = pygame.Surface((Ventana_Ancho, Ventana_Altura))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    Display_Surface.blit(overlay, (0, 0))
    texto_pausa = font.render("PAUSA", True, (255, 255, 255))
    Display_Surface.blit(texto_pausa, (Ventana_Ancho//2 - texto_pausa.get_width()//2, 200))

    boton_reanudar = pygame.Rect(Ventana_Ancho//2 - 100, 280, 200, 40)
    boton_salir = pygame.Rect(Ventana_Ancho//2 - 100, 340, 200, 40)
    pygame.draw.rect(Display_Surface, (0, 192, 0), boton_reanudar, border_radius=6)
    pygame.draw.rect(Display_Surface, (255, 0, 0), boton_salir, border_radius=6)

    txt_reanudar = font.render("REANUDAR", True, (0, 0, 0))
    txt_salir = font.render("SALIR A NIVELES", True, (0, 0, 0))
    Display_Surface.blit(txt_reanudar, (boton_reanudar.centerx - txt_reanudar.get_width()//2, boton_reanudar.centery - txt_reanudar.get_height()//2))
    Display_Surface.blit(txt_salir, (boton_salir.centerx - txt_salir.get_width()//2, boton_salir.centery - txt_salir.get_height()//2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reanudar.collidepoint(event.pos):
                    return
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    os.system(f"python CONPY/niveles_pygame.py {uid}")
                    sys.exit()

def mostrar_game_over():
    while True:
        overlay = pygame.Surface((Ventana_Ancho, Ventana_Altura))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        Display_Surface.blit(overlay, (0, 0))

        texto_gameover = font.render("GAME OVER", True, (255, 0, 0))
        Display_Surface.blit(texto_gameover, (Ventana_Ancho//2 - texto_gameover.get_width()//2, 200))

        boton_reintentar = pygame.Rect(Ventana_Ancho//2 - 100, 280, 200, 40)
        boton_salir = pygame.Rect(Ventana_Ancho//2 - 100, 340, 200, 40)
        pygame.draw.rect(Display_Surface, (255, 255, 0), boton_reintentar, border_radius=6)
        pygame.draw.rect(Display_Surface, (255, 0, 0), boton_salir, border_radius=6)

        txt_reintentar = font.render("REINTENTAR", True, (0, 0, 0))
        txt_salir = font.render("SALIR A NIVELES", True, (0, 0, 0))

        Display_Surface.blit(txt_reintentar, (boton_reintentar.centerx - txt_reintentar.get_width()//2, boton_reintentar.centery - txt_reintentar.get_height()//2))
        Display_Surface.blit(txt_salir, (boton_salir.centerx - txt_salir.get_width()//2, boton_salir.centery - txt_salir.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reintentar.collidepoint(event.pos):
                    pygame.quit()
                    subprocess.run([sys.executable, os.path.abspath(__file__), uid])
                    sys.exit()
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    os.system(f"python CONPY/niveles_pygame.py {uid}")
                    sys.exit()

def cortina_entrada(surface, fondo):
    paso = 20
    for ancho in range(Ventana_Ancho // 2, -1, -paso):
        surface.blit(fondo, (0, 0))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, ancho, Ventana_Altura))
        pygame.draw.rect(surface, (0, 0, 0), (Ventana_Ancho - ancho, 0, ancho, Ventana_Altura))
        pygame.display.flip()
        pygame.time.delay(20)

def mostrar_pantalla_inicio():
    frases_buho = [
        "Ey, ya calentaste motores o todavia estas en Bienestar?",
        "Trajiste la tula o vienes sin poderes?",
        "Hoy si le das con toda... o te devuelves al menu?",
        "Pilas, que esta cabra no se doma con un cafecito.",
        "Esto no es clase, aqui si te toca correr.",
        "Con fe, como buscando cupo en electiva libre.",
        "Ni el de fisica II corre tan rapido como la cabra.",
        "Que no se diga que lo tuyo fue relleno.",
        "Un paso mas y te graduas del Nivel Alpha... o no.",
        "No hay simulacro aqui, solo fuego real.",
        "Estas mas listo que cafeteria a las 7 a.m.?",
        "Te crees el mas teso? La cabra tambien.",
        "Aqui no hay recuperatorio, solo una vida."
    ]

    fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png").convert()
    fondo = pygame.transform.scale(fondo, (Ventana_Ancho, Ventana_Altura))

    buho_inicio = pygame.image.load("Assets1/Buho test.png").convert_alpha()
    buho_inicio = pygame.transform.scale(buho_inicio, (80, 80))

    Display_Surface.fill((0, 0, 0))
    cortina_entrada(Display_Surface, fondo)

    frase = random.choice(frases_buho)
    esperando = True

    while esperando:
        Display_Surface.blit(fondo, (0, 0))

        # Posiciones
        buho_x = 60
        buho_y = Ventana_Altura // 2 - 50
        caja_x = buho_x + 90
        caja_y = buho_y + 10
        caja_w = Ventana_Ancho - caja_x - 30
        caja_h = 80

        # Dibujar búho
        Display_Surface.blit(buho_inicio, (buho_x, buho_y))

        # Caja de texto
        pygame.draw.rect(Display_Surface, (0, 0, 0), (caja_x, caja_y, caja_w, caja_h))
        pygame.draw.rect(Display_Surface, (255, 255, 255), (caja_x, caja_y, caja_w, caja_h), 2)

        # Frase dividida en líneas
        palabras = frase.split()
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            test = linea_actual + palabra + " "
            if font.size(test)[0] < caja_w - 20:
                linea_actual = test
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)

        for i, linea in enumerate(lineas[:3]):
            texto = font.render(linea.strip(), True, (255, 255, 255))
            Display_Surface.blit(texto, (caja_x + 10, caja_y + 10 + i * 22))

        # Título
        titulo = font.render("¿Estás listo para comenzar?", True, (255, 255, 255))
        Display_Surface.blit(titulo, (Ventana_Ancho // 2 - titulo.get_width() // 2, 80))

        # Botones
        boton_jugar = pygame.Rect(Ventana_Ancho // 2 - 120, Ventana_Altura - 140, 100, 40)
        boton_volver = pygame.Rect(Ventana_Ancho // 2 + 20, Ventana_Altura - 140, 100, 40)

        pygame.draw.rect(Display_Surface, (0, 255, 0), boton_jugar)
        pygame.draw.rect(Display_Surface, (255, 0, 0), boton_volver)

        txt_jugar = font.render("JUGAR", True, (0, 0, 0))
        txt_volver = font.render("VOLVER", True, (0, 0, 0))

        Display_Surface.blit(txt_jugar, (boton_jugar.centerx - txt_jugar.get_width() // 2,
                                         boton_jugar.centery - txt_jugar.get_height() // 2))
        Display_Surface.blit(txt_volver, (boton_volver.centerx - txt_volver.get_width() // 2,
                                          boton_volver.centery - txt_volver.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    for ancho in range(0, Ventana_Ancho // 2 + 20, 20):
                        Display_Surface.blit(fondo, (0, 0))
                        pygame.draw.rect(Display_Surface, (0, 0, 0), (0, 0, ancho, Ventana_Altura))
                        pygame.draw.rect(Display_Surface, (0, 0, 0), (Ventana_Ancho - ancho, 0, ancho, Ventana_Altura))
                        pygame.display.flip()
                        pygame.time.delay(20)
                    esperando = False
                elif boton_volver.collidepoint(event.pos):
                    pygame.quit()
                    os.system(f"python CONPY/niveles_pygame.py {uid}")
                    sys.exit()


# =================== MAIN ===================
def main():
    global poder_tinto, poder_tula, poder_sticker
    corriendo = True
    while corriendo:
        reloj.tick(fps)
        Display_Surface.fill((4, 17, 4))
        draw_board(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_pausa.collidepoint(event.pos):
                    mostrar_pausa()
                elif boton_bolsa.collidepoint(event.pos):
                    os.system(f"python CONPY/bolsa_poderes_pygame.py {uid}")
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    jugador.mover(-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    jugador.mover(1, 0)
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    jugador.mover(0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    jugador.mover(0, 1)

        tiempo_actual = pygame.time.get_ticks()
        if poder_tinto and tiempo_actual - poder_tinto_timer > 5000:
            poder_tinto = False
        if poder_sticker and tiempo_actual - poder_sticker_timer > 5000:
            poder_sticker = False

        jugador.actualizar()
        mover_cabra()
        jugador.dibujar_estela()
        jugador.dibujar()
        Display_Surface.blit(cabra_img, (cabra_pos[1]*CELL_WIDTH, cabra_pos[0]*CELL_HEIGHT))

        if [jugador.fila, jugador.col] == cabra_pos:
            if poder_tula:
                poder_tula = False
            else:
                mostrar_game_over()

        # Dibujar botones
        pygame.draw.rect(Display_Surface, (200, 200, 0), boton_pausa)
        pygame.draw.rect(Display_Surface, (0, 0, 0), boton_pausa, 2)
        txt_pausa = font.render("PAUSA", True, (0, 0, 0))
        Display_Surface.blit(txt_pausa, (boton_pausa.centerx - txt_pausa.get_width()//2, boton_pausa.centery - txt_pausa.get_height()//2))

        pygame.draw.rect(Display_Surface, (0, 200, 0), boton_bolsa)
        pygame.draw.rect(Display_Surface, (0, 0, 0), boton_bolsa, 2)
        txt_bolsa = font.render("BOLSA", True, (0, 0, 0))
        Display_Surface.blit(txt_bolsa, (boton_bolsa.centerx - txt_bolsa.get_width()//2, boton_bolsa.centery - txt_bolsa.get_height()//2))

        # Estado de poder activo
        if poder_tula:
            texto_poder = font.render("🛡 Tula activa", True, (255, 255, 255))
        elif poder_tinto:
            texto_poder = font.render("⚡ Tinto activo", True, (255, 255, 255))
        elif poder_sticker:
            texto_poder = font.render("🚫 Sticker activo", True, (255, 255, 255))
        else:
            texto_poder = None

        if texto_poder:
            Display_Surface.blit(texto_poder, (10, 10))

        # Puntaje
        texto_puntaje = font.render(f"Monedas: {puntaje}", True, (255, 255, 255))
        Display_Surface.blit(texto_puntaje, (10, 30))

        pygame.display.flip()

    pygame.quit()

# =================== EJECUCIÓN ===================
if __name__ == "__main__":
    mostrar_pantalla_inicio()
    main()
















