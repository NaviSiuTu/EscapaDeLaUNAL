from TitulosYutilidades import print_advertencia, print_confirmado, print_error, print_información, print_opcion, print_Titulos
from firebase_admin import db
import re

def authenticate_user(email, password):
    try:
        users_ref = db.reference('users')
        users = users_ref.get()

        if not users:
            print_error("No hay usuarios registrados en la base de datos")
            return None

        for user_id, user_data in users.items():
            if user_data.get('email') == email:
                # Aquí validamos también la contraseña
                if user_data.get('Contraseña') == password:
                    return user_data
                else:
                    return None  # Contraseña incorrecta

        return None  # Email no encontrado

    except Exception as e:
        print_error(f"Error al autenticar: {e}")
        return None

def login():
    print_Titulos("⎈ INICIO DE SESIÓN ⎈")

    while True:
        # Validar formato del email
        while True:
            email = input("\033[3;34m↳ Email: \033[0m").strip()
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                print_error("Formato de email inválido. Ejemplo válido: usuario@dominio.com")
            else:
                break

        # Validar contraseña (solo letras y números)
        while True:
            password = input("\033[3;34m↳ Contraseña (solo letras y números): \033[0m").strip()
            if not password:
                print_error("La contraseña no puede estar vacía.")
            elif not re.match(r"^[A-Za-z0-9]+$", password):
                print_error("La contraseña no debe contener caracteres especiales.")
            else:
                break

        # Aquí se hace la autenticación
        user = authenticate_user(email, password)

        if user:
            print_confirmado(f"¡Bienvenido, {user['name']}!")
            print_información(f"Email: {user['email']}")
            print_información(f"Roles: {', '.join(user['roles'])}")
            if 'address' in user and 'city' in user['address']:
                print_información(f"Ciudad: {user['address']['city']}")
            break
        else:
            print_advertencia("⚠ Credenciales incorrectas. Intente nuevamente.\n")

def registrar_():
    print_Titulos("📝 REGISTRO DE USUARIO")
    
    name = input("\033[3;34m↳ Nombre completo: \033[0m").strip()
    
    # Validar email
    while True:
        email = input("\033[3;34m↳ Email: \033[0m").strip()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            print_error("Formato de email inválido. Ejemplo válido: usuario@dominio.com")
        else:
            break

    # Validar contraseña
    while True:
        password = input("\033[3;34m↳ Contraseña (solo letras y números): \033[0m").strip()
        if not password:
            print_error("La contraseña no puede estar vacía.")
        elif not re.match(r"^[A-Za-z0-9]+$", password):
            print_error("La contraseña no debe contener caracteres especiales.")
        else:
            break

    city = input("\033[3;34m↳ Ciudad: \033[0m").strip()
    
    if not all([name, email, password, city]):
        print_error("Todos los campos son obligatorios para entrar al laberinto")
        return
    
    users_ref = db.reference('users')
    users = users_ref.get() or {}
    
    for user_id, user_data in users.items():
        if user_data.get('email') == email:
            print_error("Este email ya está registrado")
            return
    
    new_user = {
        "name": name,
        "email": email,
        "is_active": True,
        "Contraseña": password,
        "roles": ["viewer"],
        "address": {
            "city": city
        }
    }
    
    try:
        user_id = name.replace(" ", "_")
        db.reference(f'users/{user_id}').set(new_user)
        print_confirmado("¡Bienvenido al laberinto! Ahora puedes iniciar sesión.")
    except Exception as e:
        print_error(f"Error al registrar: {e}")