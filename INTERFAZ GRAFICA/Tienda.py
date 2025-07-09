import pygame
import firebase_admin
from firebase_admin import credentials, db
import datetime
import sys

# ========================
# Obtener usuario desde args
# ========================
usuario_id = sys.argv[1] if len(sys.argv) > 1 else "usuario_prueba"

# ========================
# Inicializar Firebase
# ========================
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# ========================
# Funciones Firebase
# ========================
def obtener_monedas(usuario_id):
    try:
        ref = db.reference(f'users/{usuario_id}/monedas')
        monedas = ref.get()
        return int(monedas) if monedas is not None else 0
    except Exception as e:
        print(f"Error al obtener monedas: {e}")
        return 0

def registrar_compra(usuario_id, producto):
    try:
        ref = db.reference(f'users/{usuario_id}/compras')
        nueva = {
            "item": producto["nombre"],
            "precio": producto["precio"],
            "fecha": datetime.datetime.now().isoformat()
        }
        ref.push(nueva)
        return True
    except Exception as e:
        print(f"Error al registrar compra: {e}")
        return False

# ========================
# Función principal de la tienda
# ========================
def lanzar_tienda():
    pygame.init()
    ANCHO, ALTO = 300, 500
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("TIENDA DE MEJORAS")
    reloj = pygame.time.Clock()

    # Cargar fondo
    try:
        fondo = pygame.image.load("Assets1/pixil-frame-02 (2).png")
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    except:
        fondo = pygame.Surface((ANCHO, ALTO))
        fondo.fill((0, 0, 0))

    # Cargar fuentes
    fuente = pygame.font.Font("Assets1/DePixelHalbfett.ttf", 15)
    fuente_saldo = pygame.font.Font("Assets1/DePixelHalbfett.ttf", 12)
    fuente_desc = pygame.font.Font("Assets1/DePixelHalbfett.ttf", 10)

    productos = [
        {"nombre": "Velocidad+", "precio": 100, "descripcion": "Aumenta la velocidad del personaje"},
        {"nombre": "Escudo",        "precio": 80,  "descripcion": "Protección contra enemigos"},
        {"nombre": "Multiplicador XP", "precio": 100, "descripcion": "Doble experiencia por 1 hora"},
    ]

    botones = []
    saldo_jugador = obtener_monedas(usuario_id)
    mensaje = ""
    mensaje_timer = 0
    corriendo = True

    def dividir_texto(texto, max_car):
        palabras = texto.split()
        lineas, actual = [], ""
        for p in palabras:
            if len(actual + " " + p) <= max_car:
                actual += (" " + p) if actual else p
            else:
                lineas.append(actual); actual = p
        if actual: lineas.append(actual)
        return lineas

    def dibujar(pos_mouse=None):
        pantalla.blit(fondo, (0, 0))
        y = 90
        botones.clear()

        # Saldo
        sal = fuente_saldo.render(f"Monedas: {saldo_jugador}", True, (255, 255, 0))
        pantalla.blit(sal, (ANCHO//2 - sal.get_width()//2, 20))

        # Mensaje
        if mensaje:
            color = (0,255,0) if "Compra" in mensaje else (255,0,0)
            txt = fuente.render(mensaje, True, color)
            rect = txt.get_rect(center=(ANCHO//2, ALTO-30))
            pantalla.blit(txt, rect)

        for prod in productos:
            t = fuente.render(f"{prod['nombre']} - ${prod['precio']}", True, (255,255,255))
            rect_t = t.get_rect(center=(ANCHO//2, y))
            pantalla.blit(t, rect_t)

            lines = dividir_texto(prod["descripcion"], 28)
            for i, ln in enumerate(lines):
                dt = fuente_desc.render(ln, True, (220,220,220))
                pantalla.blit(dt, (ANCHO//2 - dt.get_width()//2, y + 20 + i*12))

            btn_w, btn_h = 120, 30
            bx = (ANCHO - btn_w)//2
            by = y + 20 + len(lines)*12 +5
            rect_btn = pygame.Rect(bx, by, btn_w, btn_h)
            botones.append((rect_btn, prod))

            clr = (8,255,0) if saldo_jugador >= prod["precio"] else (250,100,100)
            if pos_mouse and rect_btn.collidepoint(pos_mouse):
                clr = (100,255,100) if saldo_jugador >= prod["precio"] else (255,80,80)

            pygame.draw.rect(pantalla, clr, rect_btn, border_radius=5)
            bt = fuente.render("COMPRAR", True, (0,0,0))
            pantalla.blit(bt, bt.get_rect(center=rect_btn.center))

            y += 120

        pygame.display.flip()

    # Bucle principal
    while corriendo:
        pos = pygame.mouse.get_pos()
        click = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                corriendo = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                click = True
                for rect_btn, prod in botones:
                    if rect_btn.collidepoint(pos):
                        if saldo_jugador >= prod["precio"]:
                            nuevo_saldo = saldo_jugador - prod["precio"]
                            if registrar_compra(usuario_id, prod):
                                db.reference(f'users/{usuario_id}').update({"monedas": nuevo_saldo})
                                saldo_jugador = nuevo_saldo
                                mensaje = f"¡Compra exitosa! {prod['nombre']}"
                            else:
                                mensaje = "Error al registrar compra"
                        else:
                            mensaje = "No tienes suficientes monedas"
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




