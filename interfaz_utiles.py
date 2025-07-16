import pygame
from firebase_admin import db

def obtener_bolsa(usuario_id):
    ref = db.reference(f'users/{usuario_id}/compras')
    compras = ref.get()
    return compras if compras else {}

def mostrar_bolsa(pantalla, usuario_id, fuente, fuente_peque):
    bolsa_raw = obtener_bolsa(usuario_id)
    ANCHO, ALTO = pantalla.get_size()
    ventana_w, ventana_h = 340, 300
    ventana = pygame.Surface((ventana_w, ventana_h))
    ventana.fill((30, 30, 30))
    pygame.draw.rect(ventana, (255, 255, 255), ventana.get_rect(), 3)

    conteo = {}
    for item in bolsa_raw.values():
        nombre = item['item']
        if nombre in conteo:
            conteo[nombre]['cantidad'] += 1
        else:
            conteo[nombre] = {
                'precio': item['precio'],
                'cantidad': 1
            }

    y = 10
    if conteo:
        for nombre, data in conteo.items():
            txt = f"{nombre} x{data['cantidad']} - ${data['precio'] * data['cantidad']}"
            texto = fuente_peque.render(txt, True, (0, 255, 0))
            ventana.blit(texto, (10, y))
            y += 25
    else:
        sin_txt = fuente_peque.render("No hay poderes aún.", True, (255, 0, 0))
        ventana.blit(sin_txt, (10, y))
        y += 30

    cerrar_rect = pygame.Rect(ventana_w // 2 - 40, ventana_h - 40, 80, 25)
    pygame.draw.rect(ventana, (255, 0, 0), cerrar_rect)
    pygame.draw.rect(ventana, (0, 0, 0), cerrar_rect, 2)
    cerrar_txt = fuente_peque.render("CERRAR", True, (0, 0, 0))
    ventana.blit(cerrar_txt, (cerrar_rect.centerx - cerrar_txt.get_width() // 2,
                              cerrar_rect.centery - cerrar_txt.get_height() // 2))

    pos_modal = ((ANCHO - ventana_w) // 2, (ALTO - ventana_h) // 2)
    pantalla.blit(ventana, pos_modal)
    pygame.display.flip()

    esperando = True
    while esperando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                esperando = False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_rel = (ev.pos[0] - pos_modal[0], ev.pos[1] - pos_modal[1])
                if cerrar_rect.collidepoint(mouse_rel):
                    esperando = False
        pygame.time.delay(50)
