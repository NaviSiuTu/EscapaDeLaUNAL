# Main.py
import firebase_admin
from firebase_admin import credentials, db
import re
from TitulosYutilidades import (
    print_advertencia,
    print_confirmado,
    print_error,
    print_información,
    print_opcion,
    print_Titulos
)

from Eliminación_de_Usuario import delete_user
from Login_de_usuario import login, authenticate_user, registrar_
from Login_de_usuario import registrar_
from JajajLosPuntajes import ver_tabla_puntajes
#from JajajLosPuntajes import mostrar_tabla_puntajes  # ✅ Asegúrate de que esta función exista
# Inicialización de Firebase
cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
})


def main_menu():
    while True:
        print_Titulos("MENÚ PRINCIPAL")
        print_opcion("1", "Iniciar sesión")
        print_opcion("2", "Registrarse")
        print_opcion("3", "Eliminar Usuario")
        print_opcion("4", "Ver Top Global de monedas")
        print_opcion("5", "Salir")
        
        choice = input("\n\033[1;33m↳ Selecciona una opción (1-5): \033[0m").strip()
        
        if choice == "1":
            login()
        elif choice == "2":
            registrar_()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            ver_tabla_puntajes()
        elif choice == "5":
            print_confirmado("¡Gracias por jugar!")
            break
        else:
            print_error("Opción no válida. Por favor ingresa un número entre 1 y 5.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n\033[1;31mOperación cancelada por el jugador\033[0m")
    except Exception as e:
        print_error(f"Error inesperado: {e}")
