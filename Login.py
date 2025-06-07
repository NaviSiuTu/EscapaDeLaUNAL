import firebase_admin
from firebase_admin import credentials, db
import re

# Inicialización de Firebase
cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
})

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


def register_user():
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
    
def delete_user():
    print_Titulos("✖ ELIMINACIÓN DE CUENTA ✖")
    ref = db.reference("users")

    correo = input("\033[3;34m↳ Email: \033[0m").strip()
    password = input("\033[3;34m↳ Contraseña: \033[0m").strip()

    usuarios = ref.get()
    encontrado = False

    if not usuarios:
        print_error("No hay usuarios registrados.")
        return

    for id_usuario, datos in usuarios.items():
        email_db = datos.get("email")
        password_db = datos.get("Contraseña")  

        if correo == email_db and password == password_db:
            encontrado = True
            print_advertencia(f"Se encontró una cuenta asociada al correo: {correo}")
            print_información(f"Usuario: {id_usuario}")
            print_información(f"Nombre: {datos.get('name')}")
            print_información(f"Ciudad: {datos.get('address', {}).get('city', 'No registrada')}")

            confirmar = input("\n\033[1;31m¿Estás seguro de que deseas eliminar esta cuenta? (y/n): \033[0m").strip().lower()
            if confirmar == "y":
                ref.child(id_usuario).delete()
                print_confirmado(f"Usuario '{id_usuario}' ha sido eliminado del laberinto.")
            else:
                print_advertencia("Eliminación cancelada por el usuario.")
            break

    if not encontrado:
        print_error("⚠️ Credenciales incorrectas o usuario no encontrado.")



def main_menu():
    while True:
        print_Titulos("MENÚ PRINCIPAL")
        print_opcion("1", "Iniciar sesión")
        print_opcion("2", "Registrarse")
        print_opcion("3", "Salir")
        print_opcion("4", "Eliminar Usuario")
        
        choice = input("\n\033[1;33m↳ Selecciona una opción (1-4): \033[0m").strip()
        
        if choice == "1":
            login()
        elif choice == "2":
            register_user()
        elif choice == "3":
            print_confirmado("¡Buena suerte aventurero! Has salido del laberinto.")
        elif choice == "4":
            delete_user()
            break
        else:
            print_error("Opción no válida. Por favor ingrese 1, 2, 3 o 4.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n\033[1;31mOperación cancelada por el jugador\033[0m")
    except Exception as e:
        print_error(f"Error inesperado: {e}")
