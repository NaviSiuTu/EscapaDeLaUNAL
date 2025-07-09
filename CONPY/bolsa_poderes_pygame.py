import pygame
import sys
import os
import firebase_admin
from firebase_admin import credentials, db
from collections import Counter

# Inicializar Firebase si no está
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# Leer UID
if len(sys.argv) < 2:
    print("Falta UID como argumento")
    sys.exit()
uid = sys.argv[1]

# Leer compras
ref = db.reference(f"users/{uid}/compras")
compras_data = ref.get()

# Agrupar por nombre y guardar IDs
agrupados = Counter()
id_por_item = {}
if compras_data:
    for compra_id, datos in compras_data.items():
        item = datos.get("item", "?")
        agrupados[item] += 1
        id_por_item.setdefault(item, []).append(compra_id)

# Comprobar si ya se usó un poder
poder_usado = os.path.exists("poder_activo.txt")

# Pygame setup
pygame.init()
ANCHO, ALTO = 400, 700
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bolsa de Poderes")
font = pygame.font.Font("Assets1/Minecraft.ttf", 16)

VERDE = (0, 255, 0)
GRIS = (120, 120, 120)
NEGRO = (0, 0, 0)
AZUL = (0, 200, 255)
ROJO = (255, 0, 0)

# Botones
boton_volver = pygame.Rect(ANCHO//2 - 60, ALTO - 50, 120, 35)
botones_poderes = []
poderes = list(agrupados.items())
for i, (item, cantidad) in enumerate(poderes):
    rect = pygame.Rect(40, 80 + i * 60, 320, 40)
    botones_poderes.append((rect, item, cantidad))

clock = pygame.time.Clock()
running = True


def mostrar_confirmacion(item):
    confirmando = True
    confirm_rect = pygame.Rect(50, 200, 300, 160)
    si_btn = pygame.Rect(80, 300, 100, 35)
    no_btn = pygame.Rect(220, 300, 100, 35)

    while confirmando:
        pygame.draw.rect(screen, (30, 30, 30), confirm_rect, border_radius=8)
        pygame.draw.rect(screen, VERDE, si_btn, border_radius=6)
        pygame.draw.rect(screen, ROJO, no_btn, border_radius=6)

        texto_msg = font.render(f"¿Usar '{item}'?", True, (255, 255, 255))
        texto_si = font.render("SÍ", True, NEGRO)
        texto_no = font.render("NO", True, NEGRO)

        screen.blit(texto_msg, (confirm_rect.centerx - texto_msg.get_width()//2, 220))
        screen.blit(texto_si, (si_btn.centerx - texto_si.get_width()//2, si_btn.centery - texto_si.get_height()//2))
        screen.blit(texto_no, (no_btn.centerx - texto_no.get_width()//2, no_btn.centery - texto_no.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if si_btn.collidepoint(event.pos):
                    return True
                elif no_btn.collidepoint(event.pos):
                    return False

        clock.tick(30)


while running:
    screen.fill((10, 30, 10))

    # Título
    pygame.draw.rect(screen, VERDE, (20, 20, 360, 40), border_radius=6)
    texto = font.render("BOLSA DE PODERES", True, (255, 255, 255))
    screen.blit(texto, (ANCHO//2 - texto.get_width()//2, 30))

    # Dibujar poderes
    for rect, item, cantidad in botones_poderes:
        color = GRIS if poder_usado else VERDE
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, NEGRO, rect, 2, border_radius=6)
        texto = font.render(f"{item} x{cantidad}", True, NEGRO)
        screen.blit(texto, (rect.centerx - texto.get_width()//2, rect.centery - texto.get_height()//2))

    # Botón Volver
    pygame.draw.rect(screen, AZUL, boton_volver, border_radius=6)
    pygame.draw.rect(screen, NEGRO, boton_volver, 2, border_radius=6)
    volver_txt = font.render("VOLVER", True, NEGRO)
    screen.blit(volver_txt, (boton_volver.centerx - volver_txt.get_width()//2,
                             boton_volver.centery - volver_txt.get_height()//2))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(event.pos):
                running = False

            elif not poder_usado:
                for rect, item, cantidad in botones_poderes:
                    if rect.collidepoint(event.pos):
                        confirmar = mostrar_confirmacion(item)
                        if confirmar:
                            with open("poder_activo.txt", "w") as f:
                                f.write(item)
                            primer_id = id_por_item[item][0]
                            db.reference(f"users/{uid}/compras/{primer_id}").delete()
                            running = False
                            break

    clock.tick(30)

pygame.quit()



