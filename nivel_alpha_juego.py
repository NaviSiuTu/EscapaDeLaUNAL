from matriz_nivel_alpha import boards
import pygame
import math

pygame.init()
Ventana_Ancho, Ventana_Altura = 398, 736
Display_Surface = pygame.display.set_mode((Ventana_Ancho, Ventana_Altura))
pygame.display.set_caption("Nivel Alpha")

# Ajustes generales
reloj = pygame.time.Clock()
fps = 60
font = pygame.font.Font("Assets1\\Minecraft.ttf", 20)

level = boards
colorTEST = (3, 115, 17)
PI = math.pi

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

def main():
    corriendo = True
    while corriendo:
        reloj.tick(fps)
        Display_Surface.fill((4, 17, 4))
        draw_board(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        pygame.display.flip()

    pygame.quit()

# Esto permite que se ejecute de forma independiente también
if __name__ == "__main__":
    main()



