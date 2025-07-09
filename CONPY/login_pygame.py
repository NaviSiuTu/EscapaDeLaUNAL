import pygame
import re
import firebase_admin
from firebase_admin import credentials, db
import os
import sys

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
pygame.display.set_caption("Login Retro")

# Colores y fuente
VERDE = (0, 192, 0)
VERDE_CLARO = (0, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
font_path = os.path.join("Assets1", "Minecraft.ttf")
font = pygame.font.Font(font_path, 16)
font_small = pygame.font.Font(font_path, 12)

# Cargar imágenes
fondo = pygame.image.load("IMAGENES/Menu.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
logo = pygame.image.load("IMAGENES/Menu (1).png")
logo = pygame.transform.scale(logo, (130, 130))

# Clase de entrada de texto
class InputBox:
    def __init__(self, x, y, w, h, text='', password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.base_color = VERDE
        self.hover_color = VERDE_CLARO
        self.color = self.base_color
        self.text = text
        self.password = password
        self.txt_surface = font.render(text, True, NEGRO)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                self.text += event.unicode
            display_text = '*' * len(self.text) if self.password else self.text
            self.txt_surface = font.render(display_text, True, NEGRO)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        self.color = self.hover_color if self.active else self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        display_text = '*' * len(self.text) if self.password else self.text
        max_width = self.rect.width - 10
        rendered_text = font.render(display_text, True, NEGRO)

        if rendered_text.get_width() > max_width:
            i = 0
            while font.size(display_text[i:])[0] > max_width:
                i += 1
            trimmed_text = display_text[i:]
        else:
            trimmed_text = display_text

        trimmed_surface = font.render(trimmed_text, True, NEGRO)
        screen.blit(trimmed_surface, (self.rect.x + 5, self.rect.y + 5))
        border_width = 3 if self.active else 2
        pygame.draw.rect(screen, NEGRO, self.rect, border_width)

    def get_text(self):
        return self.text.strip()

# Firebase auth
def authenticate_user(email, password):
    users_ref = db.reference('users')
    users = users_ref.get()
    if not users:
        return None
    for uid, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get('email') == email and user_data.get('password') == password:
            user_data["uid"] = uid
            return user_data
    return None

def mostrar_mensaje(texto):
    mensaje = font_small.render(texto, True, (255, 0, 0))
    screen.blit(mensaje, (WIDTH // 2 - mensaje.get_width() // 2, 440))

def abrir_registro():
    pygame.quit()
    os.system("python CONPY/registro_pygame.py")
    sys.exit()

def abrir_menu(usuario_id):
    pygame.quit()
    os.system(f"python CONPY/menu_pygame.py {usuario_id}")
    sys.exit()

# Cajas de texto
email_box = InputBox(110, 190, 200, 30)
pass_box = InputBox(110, 240, 200, 30, password=True)

clock = pygame.time.Clock()
error_texto = ''
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(fondo, (0, 0))

    screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 40))

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Etiquetas
    screen.blit(font_small.render("EMAIL", True, NEGRO), (110, 175))
    screen.blit(font_small.render("CONTRASEÑA", True, NEGRO), (110, 225))

    # Cajas de entrada
    email_box.update(mouse_pos)
    pass_box.update(mouse_pos)
    email_box.draw(screen)
    pass_box.draw(screen)

    # Botón LOGIN
    login_rect = pygame.Rect(150, 330, 100, 35)
    login_hover = login_rect.collidepoint(mouse_pos)
    login_color = (50, 50, 50) if login_hover else NEGRO
    pygame.draw.rect(screen, login_color, login_rect)
    login_text = font_small.render("LOGIN", True, BLANCO)
    screen.blit(login_text, (login_rect.centerx - login_text.get_width() // 2, login_rect.centery - 10))

    # Botón REGISTRARSE
    reg_rect = pygame.Rect(130, 380, 140, 35)
    reg_hover = reg_rect.collidepoint(mouse_pos)
    reg_color = (50, 50, 50) if reg_hover else NEGRO
    pygame.draw.rect(screen, reg_color, reg_rect)
    reg_text = font_small.render("REGISTRARSE", True, BLANCO)
    screen.blit(reg_text, (reg_rect.centerx - reg_text.get_width() // 2, reg_rect.centery - 10))

    # Mensaje de error
    if error_texto:
        mostrar_mensaje(error_texto)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        email_box.handle_event(event)
        pass_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if login_rect.collidepoint(event.pos):
                email = email_box.get_text()
                password = pass_box.get_text()

                if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                    error_texto = "Email invalido"
                    continue
                if not re.match(r"^[A-Za-z0-9]+$", password):
                    error_texto = "Password sin caracteres especiales"
                    continue

                user = authenticate_user(email, password)
                if user:
                    abrir_menu(user['uid'])
                else:
                    error_texto = "Credenciales incorrectas"

            elif reg_rect.collidepoint(event.pos):
                abrir_registro()

    clock.tick(30)

pygame.quit()





