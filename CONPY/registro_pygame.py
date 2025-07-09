import pygame
import os
import firebase_admin
from firebase_admin import credentials, db

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
fondo = pygame.image.load("IMAGENES/Menu.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

logo = pygame.image.load("IMAGENES/Menu (1).png")
logo = pygame.transform.scale(logo, (100, 100 ))
logo_rect = logo.get_rect(center=(WIDTH // 2, 90))  # ✅ Centramos el logo

# InputBox class


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = VERDE
        self.active_color = VERDE_CLARO
        self.color = self.base_color
        self.text = text
        self.active = False

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
        txt = font.render(self.text, True, NEGRO)
        screen.blit(txt, (self.rect.x + 5, self.rect.y + 5))

        border_width = 3 if self.active else 2
        pygame.draw.rect(screen, NEGRO, self.rect, border_width)

    def get_text(self):
        return self.text.strip()




# Ir a login
def volver_login():
    pygame.quit()
    os.system("python CONPY/login_pygame.py")

# Firebase registrar
def registrar_usuario(nombre, email, password, ciudad):
    ref = db.reference("users")
    users = ref.get() or {}
    for u in users.values():
        if u.get("email") == email:
            return False
    new_user = {
        "name": nombre,
        "email": email,
        "password": password,
        "city": ciudad,
        "coins": 100,
        "items": {}
    }
    ref.push(new_user)
    return True

# Input boxes
nombre_box = InputBox(110, 150, 200, 30)
email_box = InputBox(110, 200, 200, 30)
pass_box = InputBox(110, 250, 200, 30)
ciudad_box = InputBox(110, 300, 200, 30)

clock = pygame.time.Clock()
mensaje_error = ''
running = True

while running:
    screen.blit(fondo, (0, 0))
    screen.blit(logo, logo_rect)  # ✅ Logo centrado arriba
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    mouse_pos = pygame.mouse.get_pos()

    # Etiquetas
    screen.blit(font_small.render("NOMBRE", True, NEGRO), (110, 135))
    screen.blit(font_small.render("EMAIL", True, NEGRO), (110, 185))
    screen.blit(font_small.render("CONTRASEÑA", True, NEGRO), (110, 235))
    screen.blit(font_small.render("CIUDAD", True, NEGRO), (110, 285))

    # Inputs
    for box in [nombre_box, email_box, pass_box, ciudad_box]:
        box.update(mouse_pos)
        box.draw(screen)

    # Botón REGISTRAR
    reg_rect = pygame.Rect(WIDTH//2 - 60, 350, 120, 35)
    reg_hover = reg_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, NEGRO, reg_rect)
    screen.blit(font_small.render("REGISTRAR", True, BLANCO),
                (reg_rect.centerx - 40, reg_rect.centery - 8))

    # Botón VOLVER
    volver_rect = pygame.Rect(WIDTH//2 - 60, 400, 120, 35)
    volver_hover = volver_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, ROJO if volver_hover else (180, 0, 0), volver_rect)
    screen.blit(font_small.render("VOLVER", True, BLANCO),
                (volver_rect.centerx - 30, volver_rect.centery - 8))

    # Mensaje
    if mensaje_error:
        msg_surface = font_small.render(mensaje_error, True, ROJO)
        screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, 450))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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
                    exito = registrar_usuario(nombre, email, password, ciudad)
                    if exito:
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








