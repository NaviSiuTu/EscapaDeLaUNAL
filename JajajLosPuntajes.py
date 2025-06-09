import firebase_admin
from firebase_admin import credentials, db
from TitulosYutilidades import print_advertencia, print_confirmado, print_error, print_información, print_opcion, print_Titulos
from Eliminación_de_Usuario import delete_user
from Registro_de_usuario import register_user
from Login_de_usuario import authenticate_user
from Login_de_usuario import login


def registrar_puntaje(usuario_id, nombre, puntaje):
    try:
        scores_ref = db.reference("Puntajes")
        scores_ref.child(usuario_id).set({
            "name": nombre,
            "Puntaje": puntaje
        })
        print_confirmado("✅ Puntaje registrado correctamente.")
    except Exception as e:
        print_error(f"Error al registrar puntaje: {e}")

def mostrar_tabla_puntajes():
    print_Titulos("🏆 TABLA DE PUNTAJES 🏆")
    try:
        scores_ref = db.reference("scores")
        puntajes = scores_ref.get()

        if not puntajes:
            print_advertencia("Aún no hay puntajes registrados.")
            return

        # Ordenar de mayor a menor
        lista_ordenada = sorted(puntajes.items(), key=lambda x: x[1]['score'], reverse=True)

        for i, (user_id, data) in enumerate(lista_ordenada, start=1):
            print(f"\033[1;35m{i}. {data['name']}: {data['score']} puntos\033[0m")
    except Exception as e:
        print_error(f"Error al obtener la tabla: {e}")


# Supón que esto ocurre después de un reto
usuario_id = "Ivan Santisteban"  # Debe coincidir con el ID en Firebase
nombre = "Ivan Santisteban"
puntaje = 2000

registrar_puntaje(usuario_id, nombre, puntaje)

mostrar_tabla_puntajes()


