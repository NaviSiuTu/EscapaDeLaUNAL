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

# Fuentes
font_path = os.path.join("Assets1", "Minecraft.ttf")
fuente = pygame.font.Font(font_path, 16)
fuente_big = pygame.font.Font(font_path, 22)

# Fondo
fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Búho
icono_buho = pygame.image.load("Assets1/Buho test.png")
buho_img = pygame.transform.scale(icono_buho, (40, 40))
buho_rect = buho_img.get_rect(topleft=(10, HEIGHT - 60))
dialogos = [
    "Bienvenido al laberinto.",
    "Esta es la seccion de niveles.",
    "Selecciona uno para comenzar tu aventura."
]
dialogo_idx = 0
mostrar_dialogo = True

# Botones centrados
boton_nivel_alpha = pygame.Rect(WIDTH//2 - 110, 220, 220, 45)
boton_bolsa = pygame.Rect(WIDTH//2 - 110, 290, 220, 45)
boton_volver = pygame.Rect(WIDTH//2 - 90, 370, 180, 40)

clock = pygame.time.Clock()
running = True

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

while running:
    screen.blit(fondo, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Encabezado
    pygame.draw.rect(screen, NEGRO, (0, 0, WIDTH, 38))
    texto_jugador = fuente.render(f"Jugador: {nombre_usuario} | Monedas: {monedas}", True, BLANCO)
    screen.blit(texto_jugador, (10, 10))

    # Título
    titulo = fuente_big.render("SELECCIÓN DE NIVELES", True, BLANCO)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 80))

    # Botón Nivel Alpha
    color_alpha = AZUL_HOVER if boton_nivel_alpha.collidepoint(mouse_pos) else AZUL
    pygame.draw.rect(screen, color_alpha, boton_nivel_alpha, border_radius=8)
    pygame.draw.rect(screen, NEGRO, boton_nivel_alpha, 2, border_radius=8)
    texto_alpha = fuente.render("NIVEL ALPHA", True, NEGRO)
    screen.blit(texto_alpha, (boton_nivel_alpha.centerx - texto_alpha.get_width() // 2,
                               boton_nivel_alpha.centery - texto_alpha.get_height() // 2))

    # Botón Bolsa de Poderes
    color_bolsa = AMARILLO if boton_bolsa.collidepoint(mouse_pos) else AMARILLO_OSCURO
    pygame.draw.rect(screen, color_bolsa, boton_bolsa, border_radius=8)
    pygame.draw.rect(screen, NEGRO, boton_bolsa, 2, border_radius=8)
    texto_bolsa = fuente.render("BOLSA DE PODERES", True, NEGRO)
    screen.blit(texto_bolsa, (boton_bolsa.centerx - texto_bolsa.get_width() // 2,
                               boton_bolsa.centery - texto_bolsa.get_height() // 2))

    # Botón Volver
    color_volver = VERDE_HOVER if boton_volver.collidepoint(mouse_pos) else VERDE
    pygame.draw.rect(screen, color_volver, boton_volver, border_radius=8)
    pygame.draw.rect(screen, NEGRO, boton_volver, 2, border_radius=8)
    texto_volver = fuente.render("VOLVER AL MENÚ", True, NEGRO)
    screen.blit(texto_volver, (boton_volver.centerx - texto_volver.get_width() // 2,
                                boton_volver.centery - texto_volver.get_height() // 2))

    # Búho y cuadro de diálogo
    screen.blit(buho_img, buho_rect)
    if mostrar_dialogo:
        cuadro = pygame.Rect(60, HEIGHT - 60, 340, 45)
        pygame.draw.rect(screen, NEGRO, cuadro, border_radius=6)
        pygame.draw.rect(screen, BLANCO, cuadro, 2, border_radius=6)
        texto_lineas = render_texto_multilinea(dialogos[dialogo_idx], fuente, BLANCO, cuadro.width - 20)
        for i, linea_surface in enumerate(texto_lineas):
            screen.blit(linea_surface, (cuadro.x + 10, cuadro.y + 8 + i * 18))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_nivel_alpha.collidepoint(event.pos):
                pygame.quit()
                os.system(f'python "CONPY/nivel_alpha_juegopygame.py" {uid}')
                sys.exit()
            elif boton_bolsa.collidepoint(event.pos):
                pygame.quit()
                os.system(f'python "CONPY/bolsa_poderes_pygame.py" {uid}')
                sys.exit()
            elif boton_volver.collidepoint(event.pos):
                pygame.quit()
                os.system(f'python "CONPY/menu_principal.py" {uid} {nombre_usuario} {monedas}')
                sys.exit()
            elif buho_rect.collidepoint(event.pos):
                dialogo_idx = (dialogo_idx + 1) % len(dialogos)
                mostrar_dialogo = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


