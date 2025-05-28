import firebase_admin
from firebase_admin import credentials, db

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
                return user_data
                
        print_error("Usuario no encontrado")
        return None
        
    except Exception as e:
        print_error(f"Error al autenticar: {e}")
        return None

def login():
    print_Titulos("⎈ INICIO DE SESIÓN ⎈")
    
    while True:
        email = input("\033[3;34m↳ Email: \033[0m").strip()  # Negrita, texto azul
        password = input("\033[3;34m↳ Contraseña: \033[0m").strip()
    
        user = authenticate_user(email, password)
        
        if user:
            print_confirmado(f"¡Bienvenido, {user['name']}!")
            print_información(f"Email: {user['email']}")
            print_información(f"Roles: {', '.join(user['roles'])}")
            if 'address' in user and 'city' in user['address']:
                print_información(f"Ciudad: {user['address']['city']}")
            break
        else:
            print_advertencia("Credenciales incorrectas. Intente nuevamente.\n")

def register_user():
    print_Titulos("REGISTRO DE USUARIO")
    
    name = input("\033[3;34m↳ Nombre completo: \033[0m").strip()
    email = input("\033[3;34m↳ Email: \033[0m").strip()
    password = input("\033[3;34m↳ Contraseña: \033[0m").strip()
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

def main_menu():
    while True:
        print_Titulos("MENÚ PRINCIPAL")
        print_opcion("1", "Iniciar sesión")
        print_opcion("2", "Registrarse")
        print_opcion("3", "Salir")
        
        choice = input("\n\033[1;33m↳ Selecciona una opción (1-3): \033[0m").strip()
        
        if choice == "1":
            login()
        elif choice == "2":
            register_user()
        elif choice == "3":
            print_confirmado("¡Buena suerte aventurero! Has salido del laberinto.")
            break
        else:
            print_error("Opción no válida. Por favor ingrese 1, 2 o 3.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n\033[1;31mOperación cancelada por el jugador\033[0m")
    except Exception as e:
        print_error(f"Error inesperado: {e}")
