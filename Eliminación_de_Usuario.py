from TitulosYutilidades import print_advertencia, print_confirmado, print_error, print_información, print_opcion, print_Titulos
from firebase_admin import db
import re

def delete_user():
    print_Titulos("✖ ELIMINACIÓN DE CUENTA ✖")
    ref = db.reference("users")

    correo = input("\033[3;34m↳ Email: \033[0m").strip()
    password = input("\033[3;34m↳ Contraseña: \033[0m").strip()

    # Validación de email
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        print_error("⚠️ El correo electrónico no tiene una estructura válida.")
        return

    # Validación de contraseña
    if not re.match(r"^[a-zA-Z0-9]+$", password):
        print_error("⚠️ La contraseña solo debe contener letras y números (sin caracteres especiales).")
        return

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