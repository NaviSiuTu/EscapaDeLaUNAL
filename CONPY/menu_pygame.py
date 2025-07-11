import pygame
import os
import sys
import firebase_admin
from firebase_admin import credentials, db

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# Configuración
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

# Fondo y logo
fondo = pygame.image.load("IMAGENES/Menu.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
logo = pygame.image.load("IMAGENES/Menu (1).png")
logo = pygame.transform.scale(logo, (130, 130))
logo_pos = (WIDTH // 2 - logo.get_width() // 2, 60)

# Cortina de entrada
def animacion_entrada(screen, fondo):
    paso = 20
    for ancho in range(WIDTH // 2, -1, -paso):
        screen.blit(fondo, (0, 0))
        screen.blit(logo, logo_pos)
        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))  # Izquierda
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))  # Derecha
        pygame.display.flip()
        pygame.time.delay(20)

# Cortina de salida
def animacion_salida(screen, fondo):
    paso = 20
    for ancho in range(0, WIDTH // 2 + paso, paso):
        screen.blit(fondo, (0, 0))
        screen.blit(logo, logo_pos)
        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))  # Izquierda
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))  # Derecha
        pygame.display.flip()
        pygame.time.delay(20)

# Leer UID desde sys.argv
if len(sys.argv) >= 2:
    uid = sys.argv[1]
else:
    print("No se proporcionó UID")
    sys.exit()

# Cargar datos del usuario
ref_usuario = db.reference(f'users/{uid}')
usuario_data = ref_usuario.get()
if not usuario_data:
    print("Usuario no encontrado")
    sys.exit()

nombre_usuario = usuario_data.get("name", "desconocido")
monedas = usuario_data.get("monedas", 0)

# Mostrar fondo inicial y ejecutar entrada
screen.blit(fondo, (0, 0))
pygame.display.flip()
animacion_entrada(screen, fondo)

# Botones
boton_tienda = pygame.Rect(130, 220, 160, 35)
boton_nivel = pygame.Rect(130, 270, 160, 35)
boton_salir = pygame.Rect(130, 320, 160, 35)

clock = pygame.time.Clock()
running = True

def lanzar_vista(nombre_archivo):
    animacion_salida(screen, fondo)
    pygame.quit()
    os.system(f"python CONPY/{nombre_archivo} {uid}")
    sys.exit()

# Loop principal
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(fondo, (0, 0))
    screen.blit(logo, logo_pos)

    # Texto de usuario y monedas
    texto_usuario = font_small.render(f"Usuario: {nombre_usuario}", True, NEGRO)
    texto_monedas = font_small.render(f"Monedas: {monedas}", True, NEGRO)
    screen.blit(texto_usuario, (10, 10))
    screen.blit(texto_monedas, (WIDTH - texto_monedas.get_width() - 10, 10))

    # Dibujar botones
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
                animacion_salida(screen, fondo)
                running = False
            elif boton_tienda.collidepoint(event.pos):
                lanzar_vista("tienda_pygame.py")
            elif boton_nivel.collidepoint(event.pos):
                lanzar_vista("niveles_pygame.py")

    clock.tick(30)

pygame.quit()










