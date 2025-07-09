import pygame
import os
import sys
import firebase_admin
from firebase_admin import credentials, db

# Inicializar Firebase (si no está ya)
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# Leer UID desde argumentos
if len(sys.argv) >= 2:
    uid = sys.argv[1]
else:
    print("No se proporcionó UID")
    sys.exit()

# Obtener datos del usuario desde Firebase
ref_usuario = db.reference(f'users/{uid}')
usuario_data = ref_usuario.get()

if not usuario_data:
    print("Usuario no encontrado en Firebase")
    sys.exit()

# ✅ Mostrar el nombre real (no el email)
nombre_usuario = usuario_data.get("name", "desconocido")
monedas = usuario_data.get("monedas", 0)

# Pygame config
WIDTH, HEIGHT = 417, 497
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal")

# Colores y fuente
VERDE = (0, 192, 0)
VERDE_CLARO = (0, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
font_path = os.path.join("Assets1", "Minecraft.ttf")
font = pygame.font.Font(font_path, 16)
font_small = pygame.font.Font(font_path, 12)

# Fondos
fondo = pygame.image.load("IMAGENES/Menu.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
logo = pygame.image.load("IMAGENES/Menu (1).png")
logo = pygame.transform.scale(logo, (130, 130))

# Botones
boton_tienda = pygame.Rect(130, 220, 160, 35)
boton_nivel = pygame.Rect(130, 270, 160, 35)
boton_salir = pygame.Rect(130, 320, 160, 35)

clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(fondo, (0, 0))

    # Logo y etiquetas
    screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 60))
    texto_usuario = font_small.render(f"Usuario: {nombre_usuario}", True, NEGRO)
    texto_monedas = font_small.render(f"Monedas: {monedas}", True, NEGRO)
    screen.blit(texto_usuario, (10, 10))
    screen.blit(texto_monedas, (WIDTH - texto_monedas.get_width() - 10, 10))

    # Botones
    for boton, texto in [(boton_tienda, "TIENDA"), (boton_nivel, "SELECCIONAR NIVEL"), (boton_salir, "SALIR")]:
        color = VERDE_CLARO if boton.collidepoint(mouse_pos) else VERDE
        pygame.draw.rect(screen, color, boton)
        pygame.draw.rect(screen, NEGRO, boton, 2)
        texto_render = font_small.render(texto, True, NEGRO)
        screen.blit(texto_render, (boton.centerx - texto_render.get_width() // 2, boton.centery - 8))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_salir.collidepoint(event.pos):
                running = False
            elif boton_tienda.collidepoint(event.pos):
                pygame.quit()
                os.system(f"python CONPY/tienda_pygame.py {uid}")
                sys.exit()
            elif boton_nivel.collidepoint(event.pos):
                pygame.quit()
                os.system(f"python CONPY/niveles_pygame.py {uid}")
                sys.exit()

    clock.tick(30)

pygame.quit()





