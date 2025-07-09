import pygame
import math
import sys
import os
from matriz_nivel_alpha import boards

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

# Botón de pausa
boton_pausa = pygame.Rect(Ventana_Ancho - 90, 10, 80, 30)

def draw_board(lvl):
    num1 = ((Ventana_Altura - 50) // 32)
    num2 = (Ventana_Ancho // 30)
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            valor = lvl[i][j]
            cx = j * num2 + (0.5 * num2)
            cy = i * num1 + (0.5 * num1)

            if valor == 1:
                pygame.draw.circle(Display_Surface, "gold1", (cx, cy), 2)
            elif valor == 2:
                pygame.draw.circle(Display_Surface, "gold1", (cx, cy), 6)
            elif valor == 3:
                pygame.draw.line(Display_Surface, colorTEST, (cx, i * num1), (cx, i * num1 + num1), 3)
            elif valor == 4:
                pygame.draw.line(Display_Surface, colorTEST, (j * num2, cy), (j * num2 + num2, cy), 3)
            elif valor == 5:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * num2 - (num2 * 0.23)) - 2, cy, num2, num1],
                                0, PI / 2, 3)
            elif valor == 6:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * num2 + (num2 * 0.38)) + 2, cy + 2, num2, num1],
                                PI / 2, PI, 3)
            elif valor == 7:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * num2 + (num2 * 0.52)) + 0.9, (i * num1 - (0.45 * num1)) + 1.3, num2, num1],
                                PI, 3 * PI / 2, 3)
            elif valor == 8:
                pygame.draw.arc(Display_Surface, colorTEST,
                                [(j * num2 - (num2 * 0.105)) - 0.7, (i * num1 - (0.4 * num1)) - 0.7, num2, num1],
                                3 * PI / 2, 2 * PI, 3)
            elif valor == 9:
                pygame.draw.line(Display_Surface, "white", (j * num2, cy), (j * num2 + num2, cy), 3)

def mostrar_pausa():
    # Fondo semi-transparente
    overlay = pygame.Surface((Ventana_Ancho, Ventana_Altura))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    Display_Surface.blit(overlay, (0, 0))

    # Texto de pausa
    texto_pausa = font.render("PAUSA", True, (255, 255, 255))
    Display_Surface.blit(texto_pausa, (Ventana_Ancho//2 - texto_pausa.get_width()//2, 200))

    # Botones de pausa
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
                    return  # Reanudar juego
                elif boton_salir.collidepoint(event.pos):
                    pygame.quit()
                    os.system("python CONPY/niveles_pygame.py UID_DUMMY")  # <- si querés pasar UID real, cambialo
                    sys.exit()

def main():
    corriendo = True
    while corriendo:
        reloj.tick(fps)
        Display_Surface.fill((4, 17, 4))
        draw_board(level)

        # Botón de pausa visible
        pygame.draw.rect(Display_Surface, (200, 200, 0), boton_pausa)
        pygame.draw.rect(Display_Surface, (0, 0, 0), boton_pausa, 2)
        txt_pausa = font.render("PAUSA", True, (0, 0, 0))
        Display_Surface.blit(txt_pausa, (boton_pausa.centerx - txt_pausa.get_width()//2,
                                         boton_pausa.centery - txt_pausa.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_pausa.collidepoint(event.pos):
                    mostrar_pausa()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()





