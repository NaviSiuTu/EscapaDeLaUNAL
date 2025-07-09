import pygame
import math
import sys
import os
from matriz_nivel_alphapygame import boards

pygame.init()
Ventana_Ancho, Ventana_Altura = 398, 736
Display_Surface = pygame.display.set_mode((Ventana_Ancho, Ventana_Altura))
pygame.display.set_caption("Nivel Alpha")

reloj = pygame.time.Clock()
fps = 60
font = pygame.font.Font("Assets1/Minecraft.ttf", 16)

level = boards
colorTEST = (3, 115, 17)
PI = math.pi

# Tamaño de celda
CELL_WIDTH = Ventana_Ancho // 30
CELL_HEIGHT = (Ventana_Altura - 50) // 32

# ← DETECTAR UID DESDE ARGUMENTO
if len(sys.argv) > 1:
    uid = sys.argv[1]
else:
    uid = "UID_DUMMY"

# ✅ BORRAR PODER ACTIVO AL INICIAR NIVEL
if os.path.exists("poder_activo.txt"):
    os.remove("poder_activo.txt")

# Botones superiores
boton_pausa = pygame.Rect(Ventana_Ancho - 90, 10, 80, 30)
boton_bolsa = pygame.Rect(Ventana_Ancho - 180, 10, 80, 30)

# Cargar sprites
buho_img = pygame.image.load("Assets1/Buho test.png")
cabra_img = pygame.image.load("Assets1/Cabra test.png")
buho_img = pygame.transform.scale(buho_img, (CELL_WIDTH, CELL_HEIGHT))
cabra_img = pygame.transform.scale(cabra_img, (CELL_WIDTH, CELL_HEIGHT))

# Posiciones iniciales
buho_pos = [1, 1]
cabra_pos = [1, 28]

# Movimiento del búho
buho_dir = [0, 0]

# Movimiento cabra
cabra_tick = 0
cabra_tick_max = 15  # más alto = más lenta

def is_wall(row, col):
    if 0 <= row < len(level) and 0 <= col < len(level[0]):
        return level[row][col] in [3, 4, 5, 6, 7, 8, 9]
    return True

def mover_buho():
    nueva_pos = [buho_pos[0] + buho_dir[1], buho_pos[1] + buho_dir[0]]
    if not is_wall(nueva_pos[0], nueva_pos[1]):
        buho_pos[0], buho_pos[1] = nueva_pos

def mover_cabra():
    global cabra_tick
    cabra_tick += 1
    if cabra_tick < cabra_tick_max:
        return
    cabra_tick = 0
    dx = buho_pos[1] - cabra_pos[1]
    dy = buho_pos[0] - cabra_pos[0]
    move_x = 1 if dx > 0 else -1 if dx < 0 else 0
    move_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if abs(dx) > abs(dy):
        if not is_wall(cabra_pos[0], cabra_pos[1] + move_x):
            cabra_pos[1] += move_x
        elif not is_wall(cabra_pos[0] + move_y, cabra_pos[1]):
            cabra_pos[0] += move_y
    else:
        if not is_wall(cabra_pos[0] + move_y, cabra_pos[1]):
            cabra_pos[0] += move_y
        elif not is_wall(cabra_pos[0], cabra_pos[1] + move_x):
            cabra_pos[1] += move_x

def draw_board(lvl):
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            valor = lvl[i][j]
            cx = j * CELL_WIDTH + (0.5 * CELL_WIDTH)
            cy = i * CELL_HEIGHT + (0.5 * CELL_HEIGHT)
            if valor == 1:
                pygame.draw.circle(Display_Surface, "gold1", (cx, cy), 2)
            elif valor == 2:
                pygame.draw.circle(Display_Surface, "gold1", (cx, cy), 6)
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

    pygame.draw.rect(Display_Surface, (0, 0, 0), boton_reanudar, 2, border_radius=6)
    pygame.draw.rect(Display_Surface, (0, 0, 0), boton_salir, 2, border_radius=6)

    txt_reanudar = font.render("REANUDAR", True, (0, 0, 0))
    txt_salir = font.render("SALIR A NIVELES", True, (0, 0, 0))
    Display_Surface.blit(txt_reanudar, (boton_reanudar.centerx - txt_reanudar.get_width()//2,
                                        boton_reanudar.centery - txt_reanudar.get_height()//2))
    Display_Surface.blit(txt_salir, (boton_salir.centerx - txt_salir.get_width()//2,
                                     boton_salir.centery - txt_salir.get_height()//2))
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
    overlay = pygame.Surface((Ventana_Ancho, Ventana_Altura))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    Display_Surface.blit(overlay, (0, 0))

    texto_gameover = font.render("GAME OVER", True, (255, 0, 0))
    Display_Surface.blit(texto_gameover, (Ventana_Ancho//2 - texto_gameover.get_width()//2, 300))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

def main():
    global buho_dir
    corriendo = True
    while corriendo:
        reloj.tick(fps)
        Display_Surface.fill((4, 17, 4))
        draw_board(level)

        # Eventos
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
                    buho_dir = [-1, 0]
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    buho_dir = [1, 0]
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    buho_dir = [0, -1]
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    buho_dir = [0, 1]

        mover_buho()
        mover_cabra()

        # Dibujar sprites
        Display_Surface.blit(buho_img, (buho_pos[1]*CELL_WIDTH, buho_pos[0]*CELL_HEIGHT))
        Display_Surface.blit(cabra_img, (cabra_pos[1]*CELL_WIDTH, cabra_pos[0]*CELL_HEIGHT))

        # Colisión
        if buho_pos == cabra_pos:
            mostrar_game_over()

        # Botón PAUSA
        pygame.draw.rect(Display_Surface, (200, 200, 0), boton_pausa)
        pygame.draw.rect(Display_Surface, (0, 0, 0), boton_pausa, 2)
        txt_pausa = font.render("PAUSA", True, (0, 0, 0))
        Display_Surface.blit(txt_pausa, (boton_pausa.centerx - txt_pausa.get_width()//2,
                                         boton_pausa.centery - txt_pausa.get_height()//2))

        # Botón BOLSA
        pygame.draw.rect(Display_Surface, (0, 200, 0), boton_bolsa)
        pygame.draw.rect(Display_Surface, (0, 0, 0), boton_bolsa, 2)
        txt_bolsa = font.render("BOLSA", True, (0, 0, 0))
        Display_Surface.blit(txt_bolsa, (boton_bolsa.centerx - txt_bolsa.get_width()//2,
                                         boton_bolsa.centery - txt_bolsa.get_height()//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()










