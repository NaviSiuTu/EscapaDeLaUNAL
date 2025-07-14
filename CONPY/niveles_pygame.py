import pygame
import os
import sys
import firebase_admin
from firebase_admin import credentials, db

# Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# UID desde argumentos
if len(sys.argv) >= 2:
    uid = sys.argv[1]
else:
    print("No se proporcionó UID")
    sys.exit()

# Obtener datos del usuario
ref_usuario = db.reference(f'users/{uid}')
usuario_data = ref_usuario.get()
if not usuario_data:
    print("Usuario no encontrado en Firebase")
    sys.exit()

nombre_usuario = usuario_data.get("name", "desconocido")
monedas = usuario_data.get("monedas", 0)

# Pygame
WIDTH, HEIGHT = 420, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Seleccion de Niveles")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 200, 255)
AZUL_HOVER = (100, 255, 255)
AMARILLO = (255, 255, 0)
AMARILLO_OSCURO = (200, 200, 0)
VERDE = (0, 200, 100)
VERDE_HOVER = (0, 255, 150)

# Fuente y fondo
font_path = os.path.join("Assets1", "Minecraft.ttf")
fuente = pygame.font.Font(font_path, 16)
fuente_big = pygame.font.Font(font_path, 22)
fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Búho y diálogos
top_buho = HEIGHT - 60
buho_img = pygame.transform.scale(pygame.image.load("Assets1/Buho test.png"), (40, 40))
buho_rect = buho_img.get_rect(topleft=(10, top_buho))
dialogos = [
    "Bienvenido al laberinto.",
    "Esta es la seccion de niveles.",
    "Selecciona uno para comenzar tu aventura."
]
dialogo_idx = 0
mostrar_dialogo = True

# Botones
boton_nivel_alpha = pygame.Rect(WIDTH//2 - 110, 220, 220, 45)
boton_nivel_beta = pygame.Rect(WIDTH//2 - 110, 270, 220, 45)
boton_bolsa = pygame.Rect(WIDTH//2 - 110, 340, 220, 45)
boton_volver = pygame.Rect(WIDTH//2 - 90, 420, 180, 40)

clock = pygame.time.Clock()
running = True

# Funciones
def render_texto_multilinea(texto, fuente, color, ancho_max):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        test_linea = linea_actual + palabra + " "
        if fuente.size(test_linea)[0] < ancho_max:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    lineas.append(linea_actual)
    superficies = [fuente.render(linea.strip(), True, color) for linea in lineas]
    return superficies

def animacion_entrada():
    paso = 10
    for ancho in range(WIDTH // 2, -1, -paso):
        screen.blit(fondo, (0, 0))
        screen.blit(buho_img, buho_rect)
        pygame.draw.rect(screen, NEGRO, (0, 0, WIDTH, 38))
        texto_jugador = fuente.render(f"Jugador: {nombre_usuario} | Monedas: {monedas}", True, BLANCO)
        screen.blit(texto_jugador, (10, 10))
        titulo = fuente_big.render("SELECCION DE NIVELES", True, BLANCO)
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 80))

        pygame.draw.rect(screen, AZUL, boton_nivel_alpha, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_nivel_alpha, 2, border_radius=8)
        screen.blit(fuente.render("NIVEL ALPHA", True, NEGRO),
                    (boton_nivel_alpha.centerx - 55, boton_nivel_alpha.centery - 10))

        pygame.draw.rect(screen, AZUL, boton_nivel_beta, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_nivel_beta, 2, border_radius=8)
        screen.blit(fuente.render("NIVEL BETA", True, NEGRO),
                    (boton_nivel_beta.centerx - 50, boton_nivel_beta.centery - 10))

        pygame.draw.rect(screen, AMARILLO_OSCURO, boton_bolsa, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_bolsa, 2, border_radius=8)
        screen.blit(fuente.render("BOLSA DE PODERES", True, NEGRO),
                    (boton_bolsa.centerx - 80, boton_bolsa.centery - 10))

        pygame.draw.rect(screen, VERDE, boton_volver, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_volver, 2, border_radius=8)
        screen.blit(fuente.render("VOLVER AL MENU", True, NEGRO),
                    (boton_volver.centerx - 70, boton_volver.centery - 10))

        if mostrar_dialogo:
            cuadro = pygame.Rect(60, HEIGHT - 60, 340, 45)
            pygame.draw.rect(screen, NEGRO, cuadro, border_radius=6)
            pygame.draw.rect(screen, BLANCO, cuadro, 2, border_radius=6)
            texto_lineas = render_texto_multilinea(dialogos[dialogo_idx], fuente, BLANCO, cuadro.width - 20)
            for i, linea_surface in enumerate(texto_lineas):
                screen.blit(linea_surface, (cuadro.x + 10, cuadro.y + 8 + i * 18))

        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))

        pygame.display.flip()
        pygame.time.delay(25)

def animacion_salida():
    paso = 20
    for ancho in range(0, WIDTH // 2 + paso, paso):
        screen.blit(fondo, (0, 0))
        screen.blit(buho_img, buho_rect)
        pygame.draw.rect(screen, NEGRO, (0, 0, WIDTH, 38))
        texto_jugador = fuente.render(f"Jugador: {nombre_usuario} | Monedas: {monedas}", True, BLANCO)
        screen.blit(texto_jugador, (10, 10))
        titulo = fuente_big.render("SELECCION DE NIVELES", True, BLANCO)
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 80))

        pygame.draw.rect(screen, AZUL, boton_nivel_alpha, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_nivel_alpha, 2, border_radius=8)
        screen.blit(fuente.render("NIVEL ALPHA", True, NEGRO),
                    (boton_nivel_alpha.centerx - 55, boton_nivel_alpha.centery - 10))

        pygame.draw.rect(screen, AZUL, boton_nivel_beta, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_nivel_beta, 2, border_radius=8)
        screen.blit(fuente.render("NIVEL BETA", True, NEGRO),
                    (boton_nivel_beta.centerx - 50, boton_nivel_beta.centery - 10))

        pygame.draw.rect(screen, AMARILLO_OSCURO, boton_bolsa, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_bolsa, 2, border_radius=8)
        screen.blit(fuente.render("BOLSA DE PODERES", True, NEGRO),
                    (boton_bolsa.centerx - 80, boton_bolsa.centery - 10))

        pygame.draw.rect(screen, VERDE, boton_volver, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton_volver, 2, border_radius=8)
        screen.blit(fuente.render("VOLVER AL MENU", True, NEGRO),
                    (boton_volver.centerx - 70, boton_volver.centery - 10))

        if mostrar_dialogo:
            cuadro = pygame.Rect(60, HEIGHT - 60, 340, 45)
            pygame.draw.rect(screen, NEGRO, cuadro, border_radius=6)
            pygame.draw.rect(screen, BLANCO, cuadro, 2, border_radius=6)
            texto_lineas = render_texto_multilinea(dialogos[dialogo_idx], fuente, BLANCO, cuadro.width - 20)
            for i, linea_surface in enumerate(texto_lineas):
                screen.blit(linea_surface, (cuadro.x + 10, cuadro.y + 8 + i * 18))

        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))

        pygame.display.flip()
        pygame.time.delay(20)

# Mostrar pantalla inicial con animación
screen.blit(fondo, (0, 0))
pygame.display.flip()
animacion_entrada()

# Bucle principal
while running:
    screen.blit(fondo, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Encabezado
    pygame.draw.rect(screen, NEGRO, (0, 0, WIDTH, 38))
    texto_jugador = fuente.render(f"Jugador: {nombre_usuario} | Monedas: {monedas}", True, BLANCO)
    screen.blit(texto_jugador, (10, 10))

    # Título
    titulo = fuente_big.render("SELECCION DE NIVELES", True, BLANCO)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 80))

    # Botones con hover
    for boton, texto, color_normal, color_hover in [
        (boton_nivel_alpha, "NIVEL ALPHA", AZUL, AZUL_HOVER),
        (boton_nivel_beta, "NIVEL BETA", AZUL, AZUL_HOVER),
        (boton_bolsa, "BOLSA DE PODERES", AMARILLO_OSCURO, AMARILLO),
        (boton_volver, "VOLVER AL MENU", VERDE, VERDE_HOVER)
    ]:
        color = color_hover if boton.collidepoint(mouse_pos) else color_normal
        pygame.draw.rect(screen, color, boton, border_radius=8)
        pygame.draw.rect(screen, NEGRO, boton, 2, border_radius=8)
        texto_render = fuente.render(texto, True, NEGRO)
        screen.blit(texto_render, (boton.centerx - texto_render.get_width() // 2,
                                   boton.centery - texto_render.get_height() // 2))

    # Búho y diálogo
    screen.blit(buho_img, buho_rect)
    if mostrar_dialogo:
        cuadro = pygame.Rect(60, HEIGHT - 60, 340, 45)
        pygame.draw.rect(screen, NEGRO, cuadro, border_radius=6)
        pygame.draw.rect(screen, BLANCO, cuadro, 2, border_radius=6)
        texto_lineas = render_texto_multilinea(dialogos[dialogo_idx], fuente, BLANCO, cuadro.width - 20)
        for i, linea_surface in enumerate(texto_lineas):
            screen.blit(linea_surface, (cuadro.x + 10, cuadro.y + 8 + i * 18))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_nivel_alpha.collidepoint(event.pos):
                animacion_salida()
                pygame.display.quit()
                os.system(f'python "NIVELES Y BOARD/nivel_alpha_juegopygame.py" {uid}')
                sys.exit()

            elif boton_nivel_beta.collidepoint(event.pos):
                animacion_salida()
                pygame.display.quit()
                os.system(f'python "NIVELES Y BOARD/nivel_Beta_juegopygame.py" {uid}')
                sys.exit()

            elif boton_bolsa.collidepoint(event.pos):
                animacion_salida()
                pygame.display.quit()
                os.system(f'python "CONPY/bolsa_poderes_pygame.py" {uid}')
                sys.exit()

            elif boton_volver.collidepoint(event.pos):
                animacion_salida()
                running = False

            elif buho_rect.collidepoint(event.pos):
                dialogo_idx = (dialogo_idx + 1) % len(dialogos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()







