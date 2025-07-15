import pygame
import firebase_admin
from firebase_admin import credentials, db
import datetime
import sys
import os
import random

# === UID desde argumentos ===
usuario_id = sys.argv[1] if len(sys.argv) > 1 else "usuario_prueba"
print(f"[DEBUG] Usuario logueado: {usuario_id}")

# === Inicializar Firebase ===
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# === Funciones Firebase ===
def obtener_monedas(usuario_id):
    try:
        ref = db.reference(f'users/{usuario_id}')
        datos = ref.get()
        return datos.get("monedas", 0) if datos else 0
    except Exception as e:
        print(f"[ERROR] al obtener monedas: {e}")
        return 0

def registrar_compra(usuario_id, producto):
    try:
        ref_user = db.reference(f'users/{usuario_id}')
        datos = ref_user.get()
        if datos:
            compras_ref = db.reference(f'users/{usuario_id}/compras')
            nueva = {
                "item": producto["nombre"],
                "precio": producto["precio"],
                "fecha": datetime.datetime.now().isoformat()
            }
            compras_ref.push(nueva)
            nuevo_saldo = datos.get("monedas", 0) - producto["precio"]
            ref_user.update({"monedas": nuevo_saldo})
            return nuevo_saldo
        return None
    except Exception as e:
        print(f"[ERROR] al registrar compra: {e}")
        return None

def obtener_bolsa(usuario_id):
    ref = db.reference(f'users/{usuario_id}/compras')
    compras = ref.get()
    return compras if compras else {}

def usar_item(uid, id_item):
    ref = db.reference(f'users/{uid}/compras/{id_item}')
    ref.delete()

# === Lanzar Tienda ===
def lanzar_tienda():
    pygame.init()
    ANCHO, ALTO = 400, 500
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("TIENDA UNAL")
    reloj = pygame.time.Clock()

    fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    font_path = os.path.join("Assets1", "Minecraft.ttf")
    fuente = pygame.font.Font(font_path, 16)
    fuente_peque = pygame.font.Font(font_path, 12)

    productos = [
        {"nombre": "Tula Bienestar UN", "precio": 100, "descripcion": "Absorbe un golpe: contiene cafe, pan y esperanza."},
        {"nombre": "Tinto cafeteria UNAL", "precio": 80, "descripcion": "Te vas a mover como en dia de parciales!"},
        {"nombre": "Sticker UNAL", "precio": 60, "descripcion": "Esa cabra huye de los verdaderos logos!"}
    ]

    botones = []
    saldo_jugador = obtener_monedas(usuario_id)
    mensaje = ""
    mensaje_timer = 0
    corriendo = True

    boton_volver = pygame.Rect(10, 10, 80, 30)
    buho_img = pygame.transform.scale(pygame.image.load("Assets1/Buho test.png"), (40, 40))
    buho_rect = buho_img.get_rect(topleft=(10, ALTO - 60))

    bolsa_img = pygame.transform.scale(pygame.image.load("Assets1/Bolsa (2).png"), (32, 32))
    bolsa_rect = bolsa_img.get_rect(topright=(ANCHO - 12, 12))

    dialogos = [
        "Bienvenido a la tienda UNAL joven de pregrado.",
        "Aqui puedes adquirir objetos para huir de la cabra.",
        "Haz clic en COMPRAR si tienes monedas.",
        "Cuando termines, presiona VOLVER."
    ]
    dialogo_idx = 0
    mostrar_dialogo = True

    dialogos_no_monedas = [
        "Con ese saldo, ni en el SIA te dejan inscribir materias.",
        "Ese bolsillo esta mas vacio que la cafeteria un viernes.",
        "Con ese bolsillo ni el buho se anima a aconsejarte",
        "Con ese saldo, ni los de primer semestre se impresionan.",
        "Tus monedas? Se fueron con el ultimo transmilenio.",
        "Tal vez si haces fila en Bienestar, te den algo...",
        "Ni rezando en la capilla te alcanza para comprar eso.",
        "Toca hacer vaquita con los del grupo de trabajo.",
        "Mas pelado que estudiante saliendo de parcial.",
        "Ese saldo esta mas triste que un lunes con parcial sorpresa.",
        "Ese bolsillo esta haciendo huelga.",
    ]

    def dividir_texto(texto, max_car):
        palabras = texto.split()
        lineas, actual = [], ""
        for p in palabras:
            if len(actual + " " + p) <= max_car:
                actual += (" " + p) if actual else p
            else:
                lineas.append(actual)
                actual = p
        if actual:
            lineas.append(actual)
        return lineas

    def mostrar_bolsa():
        bolsa_raw = obtener_bolsa(usuario_id)
        ventana_w, ventana_h = 340, 300
        ventana = pygame.Surface((ventana_w, ventana_h))
        ventana.fill((30, 30, 30))
        pygame.draw.rect(ventana, (255, 255, 255), ventana.get_rect(), 3)

        # Contar ítems repetidos
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

        # Botón cerrar
        cerrar_rect = pygame.Rect(ventana_w // 2 - 40, ventana_h - 40, 80, 25)
        pygame.draw.rect(ventana, (255, 0, 0), cerrar_rect)
        pygame.draw.rect(ventana, (0, 0, 0), cerrar_rect, 2)
        cerrar_txt = fuente_peque.render("CERRAR", True, (0, 0, 0))
        ventana.blit(cerrar_txt, (cerrar_rect.centerx - cerrar_txt.get_width() // 2,
                                cerrar_rect.centery - cerrar_txt.get_height() // 2))

        # Mostrar modal centrado
        pos_modal = ((ANCHO - ventana_w) // 2, (ALTO - ventana_h) // 2)
        pantalla.blit(ventana, pos_modal)
        pygame.display.flip()

        esperando = True
        while esperando:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    esperando = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_rel = (ev.pos[0] - pos_modal[0], ev.pos[1] - pos_modal[1])
                    if cerrar_rect.collidepoint(mouse_rel):
                        esperando = False
            pygame.time.delay(50)

    def dibujar(pos_mouse=None):
        if pos_mouse is None:
            pos_mouse = pygame.mouse.get_pos()

        pantalla.blit(fondo, (0, 0))
        y = 90
        botones.clear()

        saldo_txt = fuente.render(f"Monedas: {saldo_jugador}", True, (255, 255, 0))
        pantalla.blit(saldo_txt, (ANCHO // 2 - saldo_txt.get_width() // 2, 20))

        if mensaje:
            color = (0, 255, 0) if "Compra" in mensaje else (255, 0, 0)
            txt = fuente_peque.render(mensaje, True, color)
            pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, 40))

        for prod in productos:
            t = fuente.render(f"{prod['nombre']} - ${prod['precio']}", True, (255, 255, 255))
            pantalla.blit(t, (ANCHO // 2 - t.get_width() // 2, y))

            desc_lines = dividir_texto(prod["descripcion"], 32)
            for i, ln in enumerate(desc_lines):
                dt = fuente_peque.render(ln, True, (200, 200, 200))
                pantalla.blit(dt, (ANCHO // 2 - dt.get_width() // 2, y + 25 + i * 12))

            btn_w, btn_h = 120, 30
            bx = (ANCHO - btn_w) // 2
            by = y + 30 + len(desc_lines) * 12
            rect_btn = pygame.Rect(bx, by, btn_w, btn_h)
            botones.append((rect_btn, prod))

            color_btn = (8, 255, 0) if saldo_jugador >= prod["precio"] else (255, 100, 100)
            if rect_btn.collidepoint(pos_mouse):
                color_btn = (100, 255, 100) if saldo_jugador >= prod["precio"] else (255, 80, 80)

            pygame.draw.rect(pantalla, color_btn, rect_btn, border_radius=5)
            txt_btn = fuente_peque.render("COMPRAR", True, (0, 0, 0))
            pantalla.blit(txt_btn, (bx + btn_w // 2 - txt_btn.get_width() // 2, by + 5))

            y += 120

        pygame.draw.rect(pantalla, (0, 255, 0) if boton_volver.collidepoint(pos_mouse) else (0, 192, 0), boton_volver)
        pygame.draw.rect(pantalla, (0, 0, 0), boton_volver, 2)
        pantalla.blit(fuente_peque.render("VOLVER", True, (0, 0, 0)),
                      (boton_volver.centerx - 22, boton_volver.centery - 8))

        pantalla.blit(buho_img, buho_rect)
        pantalla.blit(bolsa_img, bolsa_rect)

        if mostrar_dialogo:
            cuadro = pygame.Rect(60, ALTO - 60, 320, 45)
            pygame.draw.rect(pantalla, (0, 0, 0), cuadro, border_radius=6)
            pygame.draw.rect(pantalla, (255, 255, 255), cuadro, 2, border_radius=6)
            texto_lineas = dividir_texto(dialogos[dialogo_idx], 34)
            for i, linea in enumerate(texto_lineas):
                render = fuente_peque.render(linea.strip(), True, (255, 255, 255))
                pantalla.blit(render, (cuadro.x + 10, cuadro.y + 8 + i * 16))

        pygame.display.flip()

    def animacion_entrada(pantalla, fondo, dibujar_func):
        paso = 20
        for ancho in range(ANCHO // 2, -1, -paso):
            dibujar_func()
            pygame.draw.rect(pantalla, (0, 0, 0), (0, 0, ancho, ALTO))
            pygame.draw.rect(pantalla, (0, 0, 0), (ANCHO - ancho, 0, ancho, ALTO))
            pygame.display.flip()
            pygame.time.delay(20)

    def animacion_salida(pantalla, fondo, dibujar_func):
        paso = 20
        for ancho in range(0, ANCHO // 2 + paso, paso):
            dibujar_func()
            pygame.draw.rect(pantalla, (0, 0, 0), (0, 0, ancho, ALTO))
            pygame.draw.rect(pantalla, (0, 0, 0), (ANCHO - ancho, 0, ancho, ALTO))
            pygame.display.flip()
            pygame.time.delay(20)

    dibujar()
    animacion_entrada(pantalla, fondo, lambda: dibujar())

    while corriendo:
        pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(pos):
                    animacion_salida(pantalla, fondo, lambda: dibujar(pos))
                    pygame.quit()
                    os.system(f"python CONPY/menu_pygame.py {usuario_id}")
                    sys.exit()
                elif buho_rect.collidepoint(pos):
                    dialogo_idx = (dialogo_idx + 1) % len(dialogos)
                    mostrar_dialogo = True
                elif bolsa_rect.collidepoint(pos):
                    mostrar_bolsa()
                for rect_btn, prod in botones:
                    if rect_btn.collidepoint(pos):
                        if saldo_jugador >= prod["precio"]:
                            nuevo = registrar_compra(usuario_id, prod)
                            if nuevo is not None:
                                saldo_jugador = nuevo
                                mensaje = f"Compra exitosa: {prod['nombre']}"
                                dialogos.append(f"Buenisima esa compra: {prod['nombre']}, joven.")
                                dialogo_idx = len(dialogos) - 1
                            else:
                                mensaje = "Error al registrar"
                        else:
                            mensaje = "Monedas insuficientes"
                            dialogos.append(random.choice(dialogos_no_monedas))
                            dialogo_idx = len(dialogos) - 1
                        mensaje_timer = 120

        if mensaje_timer > 0:
            mensaje_timer -= 1
        else:
            mensaje = ""

        dibujar(pos)
        reloj.tick(60)

    pygame.quit()

if __name__ == "__main__":
    lanzar_tienda()












