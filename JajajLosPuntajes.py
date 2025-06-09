import firebase_admin
from firebase_admin import credentials, db
from TitulosYutilidades import print_advertencia, print_confirmado, print_error, print_información, print_opcion, print_Titulos
from Eliminación_de_Usuario import delete_user
from Registro_de_usuario import register_user
from Login_de_usuario import authenticate_user
from Login_de_usuario import login


def ver_tabla_puntajes():
    print_Titulos("📊 TOP GLOBAL DE MONEDAS")

    users_ref = db.reference('users')
    users = users_ref.get()

    if not users:
        print_error("No hay usuarios registrados en Firebase.")
        return

    # Crear una lista con nombre y monedas
    puntajes = []
    for user_id, data in users.items():
        nombre = data.get('name', 'Desconocido')
        monedas = data.get('monedas', 0)
        puntajes.append((nombre, monedas))

    # Ordenar de mayor a menor por monedas
    puntajes.sort(key=lambda x: x[1], reverse=True)

    # Imprimir tabla
    for i, (nombre, monedas) in enumerate(puntajes, start=1):
        print(f"{i}. {nombre} — 🪙 {monedas} monedas")



