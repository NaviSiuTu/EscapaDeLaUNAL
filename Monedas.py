import firebase_admin
from firebase_admin import db, credentials
from TitulosYutilidades import print_advertencia, print_confirmado, print_error, print_información, print_opcion, print_Titulos


cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
})

def agregar_monedas_a_existentes():
    users_ref = db.reference('users')
    users = users_ref.get() or {}

    for user_id, user_data in users.items():
        if 'monedas' not in user_data:
            users_ref.child(user_id).update({"monedas": 1})
            print(f"✔ Monedas añadidas a {user_id}")
        else:
            print(f"🟡 {user_id} ya tenía monedas: {user_data['monedas']}")

agregar_monedas_a_existentes()

def sumar_monedas_a_todos(monedas_extra):
    users_ref = db.reference('users')
    users = users_ref.get() or {}

    for user_id, user_data in users.items():
        monedas_actuales = user_data.get("monedas", 0)  # Si no hay, se asume 0
        nuevas_monedas = monedas_actuales + monedas_extra
        users_ref.child(user_id).update({"monedas": nuevas_monedas})
        print(f"🪙 {user_id} ahora tiene {nuevas_monedas} monedas")
    
sumar_monedas_a_todos(1)

def agregar_monedas(user_id, cantidad):
    try:
        user_ref = db.reference(f'users/{user_id}')
        user_data = user_ref.get()

        if user_data:
            monedas_actuales = user_data.get('monedas', 0)
            nuevas_monedas = monedas_actuales + cantidad
            user_ref.update({'monedas': nuevas_monedas})
            print_confirmado(f"¡Ganaste {cantidad} monedas! Total: {nuevas_monedas} 🪙")
        else:
            print_error("Usuario no encontrado.")
    except Exception as e:
        print_error(f"Error al agregar monedas: {e}")

agregar_monedas("Ivan_Santisteban", 50)

    