import pygame
import os
import firebase_admin
from firebase_admin import credentials, db
import re
import sys

# Firebase init
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# Config
WIDTH, HEIGHT = 417, 497
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Registro Retro")

# Colores y fuente
VERDE = (0, 192, 0)
VERDE_CLARO = (0, 255, 0)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)

font_path = os.path.join("Assets1", "Minecraft.ttf")
font = pygame.font.Font(font_path, 16)
font_small = pygame.font.Font(font_path, 12)

# Fondo y logo
fondo = pygame.image.load("Assets1/Menu.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
logo = pygame.image.load("Assets1/Menu (1).png")
logo = pygame.transform.scale(logo, (100, 100))
logo_rect = logo.get_rect(center=(WIDTH // 2, 90))

# 🎬 Efecto cortina de entrada
def cortina_entrada(screen, fondo, logo, logo_rect):
    paso = 20
    for ancho in range(WIDTH // 2, -1, -paso):
        screen.blit(fondo, (0, 0))
        screen.blit(logo, logo_rect)
        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))  # Izquierda
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))  # Derecha
        pygame.display.flip()
        pygame.time.delay(20)

# 🎬 Efecto cortina de salida
def cortina_salida(screen, fondo, logo, logo_rect):
    paso = 20
    for ancho in range(0, WIDTH // 2 + paso, paso):
        screen.blit(fondo, (0, 0))
        screen.blit(logo, logo_rect)

        screen.blit(font_small.render("NOMBRE", True, NEGRO), (110, 135))
        screen.blit(font_small.render("EMAIL", True, NEGRO), (110, 185))
        screen.blit(font_small.render("PASSWORD", True, NEGRO), (110, 235))
        screen.blit(font_small.render("CIUDAD", True, NEGRO), (110, 285))

        for box in [nombre_box, email_box, pass_box, ciudad_box]:
            box.draw(screen)

        pygame.draw.rect(screen, NEGRO, reg_rect)
        pygame.draw.rect(screen, ROJO, volver_rect)
        screen.blit(font_small.render("REGISTRAR", True, BLANCO), (reg_rect.centerx - 40, reg_rect.centery - 8))
        screen.blit(font_small.render("VOLVER", True, BLANCO), (volver_rect.centerx - 30, volver_rect.centery - 8))

        pygame.draw.rect(screen, NEGRO, (0, 0, ancho, HEIGHT))  # Izquierda
        pygame.draw.rect(screen, NEGRO, (WIDTH - ancho, 0, ancho, HEIGHT))  # Derecha
        pygame.display.flip()
        pygame.time.delay(20)

# Clase InputBox
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = VERDE
        self.active_color = VERDE_CLARO
        self.color = self.base_color
        self.text = text
        self.active = False
        self.padding = 5
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        self.color = self.active_color if self.active else self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, NEGRO)
        max_width = self.rect.width - 2 * self.padding
        cropped_text = self.text

        while self.font.size(cropped_text)[0] > max_width and len(cropped_text) > 0:
            cropped_text = cropped_text[1:]

        text_surface = self.font.render(cropped_text, True, NEGRO)
        screen.blit(text_surface, (self.rect.x + self.padding, self.rect.y + self.padding))
        pygame.draw.rect(screen, NEGRO, self.rect, 3 if self.active else 2)

    def get_text(self):
        return self.text.strip()

# Ir a login con salida animada
def volver_login():
    cortina_salida(screen, fondo, logo, logo_rect)
    pygame.quit()
    os.environ["SPLASH_DONE"] = "1"
    os.system("python CONPY/login_pygame.py")

# Registrar usuario en Firebase
def registrar_usuario(nombre, email, password, ciudad):
    ref = db.reference("users")
    username = email.split("@")[0]
    user_ref = ref.child(username)
    if user_ref.get() is not None:
        return False
    user_ref.set({
        "name": nombre,
        "email": email,
        "password": password,
        "is_active": True,
        "monedas": 400,
        "compras": {}
    })
    return True

# Cajas de texto
nombre_box = InputBox(110, 150, 200, 30)
email_box = InputBox(110, 200, 200, 30)
pass_box = InputBox(110, 250, 200, 30)
ciudad_box = InputBox(110, 300, 200, 30)

reg_rect = pygame.Rect(WIDTH // 2 - 60, 350, 120, 35)
volver_rect = pygame.Rect(WIDTH // 2 - 60, 400, 120, 35)

clock = pygame.time.Clock()
mensaje_error = ''

# Entrada
cortina_entrada(screen, fondo, logo, logo_rect)

running = True
while running:
    screen.blit(fondo, (0, 0))
    screen.blit(logo, logo_rect)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    mouse_pos = pygame.mouse.get_pos()

    screen.blit(font_small.render("NOMBRE", True, NEGRO), (110, 135))
    screen.blit(font_small.render("EMAIL", True, NEGRO), (110, 185))
    screen.blit(font_small.render("PASSWORD", True, NEGRO), (110, 235))
    screen.blit(font_small.render("CIUDAD", True, NEGRO), (110, 285))

    for box in [nombre_box, email_box, pass_box, ciudad_box]:
        box.update(mouse_pos)
        box.draw(screen)

    pygame.draw.rect(screen, NEGRO, reg_rect)
    pygame.draw.rect(screen, ROJO if volver_rect.collidepoint(mouse_pos) else (180, 0, 0), volver_rect)

    screen.blit(font_small.render("REGISTRAR", True, BLANCO), (reg_rect.centerx - 40, reg_rect.centery - 8))
    screen.blit(font_small.render("VOLVER", True, BLANCO), (volver_rect.centerx - 30, volver_rect.centery - 8))

    if mensaje_error:
        msg_surface = font_small.render(mensaje_error, True, ROJO)
        screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, 450))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cortina_salida(screen, fondo, logo, logo_rect)
            running = False

        for box in [nombre_box, email_box, pass_box, ciudad_box]:
            box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if reg_rect.collidepoint(event.pos):
                nombre = nombre_box.get_text()
                email = email_box.get_text()
                password = pass_box.get_text()
                ciudad = ciudad_box.get_text()

                if nombre and email and password and ciudad:
                    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                        mensaje_error = "Email inválido"
                    elif not re.match(r"^[A-Za-z0-9]+$", password):
                        mensaje_error = "Password sin caracteres especiales"
                    else:
                        if registrar_usuario(nombre, email, password, ciudad):
                            mensaje_error = "¡Registrado con éxito!"
                        else:
                            mensaje_error = "Email ya registrado."
                else:
                    mensaje_error = "Completa todos los campos."

            elif volver_rect.collidepoint(event.pos):
                volver_login()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()











