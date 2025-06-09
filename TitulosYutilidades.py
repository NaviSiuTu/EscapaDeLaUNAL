def print_Titulos(text):
    print(f"\n\033[1;44;37m===== {text} =====\033[0m\n")  # Negrita, fondo azul, texto blanco (formato pa los titulos jiji)

def print_confirmado(text):
    print(f"\033[1;32m✓ {text}\033[0m")  # Negrita, texto verde (para confirmación de datos)

def print_error(text):
    print(f"\033[1;31m✗ {text}\033[0m")  # Negrita, texto rojo (para errores)

def print_advertencia(text):
    print(f"\033[1;33m⚠ {text}\033[0m")  # Negrita, texto amarillo(para especificar las condiciones requeridas)

def print_información(text):
    print(f"\033[1;36m➤ {text}\033[0m")  # Negrita, texto cyan

def print_opcion(number, text):
    print(f"\033[1;35m{number}.\033[0m {text}")  # Negrita, texto magenta para el número (opciones para elegir en menu)