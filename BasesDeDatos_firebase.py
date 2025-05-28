import firebase_admin
from firebase_admin import credentials, db


cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
firebase_admin.initialize_app(cred, {
    #"databaseURL": "https://testpoo-59c96-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
})

# Referencia al nodo en la base de datos
ref = db.reference("nodo1")  # Cambia "nodo_principal" por tu ruta

# Escribe datos en tiempo real
ref.set({
    "mensaje": "Ya tenemos base de datos team",
    "activo": True
    
})

# Escucha cambios en tiempo real
def escuchar_eventos(event):
    print(f"Cambio detectado: {event.data}")

ref.listen(escuchar_eventos)

# Escucha cambios en tiempo real
def escuchar_eventos(event):
    print(f"Cambio detectado: {event.data}")

ref.listen(escuchar_eventos)

user_data = {
    "name": "Daniela Jojoa",
    "email": "dajojoap@unal.edu.co",
    "is_active": True,
    "roles": ["editor", "viewer"],
}

# Asumiendo 'ref' es una referencia a un nodo padre (ej: db.reference('/users'))
new_user_ref = ref.push()
new_user_ref.set(user_data)
print(f"Nuevo usuario añadido con clave: {new_user_ref.key}") # .key contiene la clave push

# Usando el ID del usuario como clave personalizada
user_id = "Daniela Jojoa"
db.reference(f'users/{user_id}').set(user_data)
print(f"Datos de usuario con ID {user_id} establecidos.")

user_data = {
    "name": "Juan Sanchez",
    "email": "juasanchezva@unal.edu.co",
    "is_active": True,
    "roles": ["editor", "viewer"],
}

# Asumiendo 'ref' es una referencia a un nodo padre (ej: db.reference('/users'))
new_user_ref = ref.push()
new_user_ref.set(user_data)
print(f"Nuevo usuario añadido con clave: {new_user_ref.key}") # .key contiene la clave push

# Usando el ID del usuario como clave personalizada
user_id = "Juan Sanchez"
db.reference(f'users/{user_id}').set(user_data)
print(f"Datos de usuario con ID {user_id} establecidos.")

user_data = {
    "name": "Ivan Santiesteban",
    "email": "isantiesteban@unal.edu.co",
    "is_active": True,
    "roles": ["editor", "viewer"],
}

# Asumiendo 'ref' es una referencia a un nodo padre (ej: db.reference('/users'))
new_user_ref = ref.push()
new_user_ref.set(user_data)
print(f"Nuevo usuario añadido con clave: {new_user_ref.key}") # .key contiene la clave push

# Usando el ID del usuario como clave personalizada
user_id = "Ivan Santiesteban"
db.reference(f'users/{user_id}').set(user_data)
print(f"Datos de usuario con ID {user_id} establecidos.")


# Leer datos de un nodo específico
try:
    data = db.reference('/name').get() # Ejemplo leyendo el valor de un nodo 'name'
    print(f"Valor en /name: {data}")

    # Leer un nodo completo
    user_id = "Juan Sanchez"
    user_data_read = db.reference(f'users/{user_id}').get()
    if user_data_read:
         print(f"Datos del usuario {user_id}: {user_data_read}")
    else:
         print(f"No se encontraron datos para el usuario {user_id}.")

except Exception as e:
    print(f"Error al leer datos: {e}")

# Leer datos de un nodo específico
try:
    data = db.reference('/name').get() # Ejemplo leyendo el valor de un nodo 'name'
    print(f"Valor en /name: {data}")

    # Leer un nodo completo
    user_id = "Daniela Jojoa"
    user_data_read = db.reference(f'users/{user_id}').get()
    if user_data_read:
         print(f"Datos del usuario {user_id}: {user_data_read}")
    else:
         print(f"No se encontraron datos para el usuario {user_id}.")

except Exception as e:
    print(f"Error al leer datos: {e}")

# Leer datos de un nodo específico
try:
    data = db.reference('/name').get() # Ejemplo leyendo el valor de un nodo 'name'
    print(f"Valor en /name: {data}")

    # Leer un nodo completo
    user_id = "Ivan Santiesteban"
    user_data_read = db.reference(f'users/{user_id}').get()
    if user_data_read:
         print(f"Datos del usuario {user_id}: {user_data_read}")
    else:
         print(f"No se encontraron datos para el usuario {user_id}.")

except Exception as e:
    print(f"Error al leer datos: {e}") 

#Actualizar el nombre y añadir un campo de ciudad para un usuario específico,
user_id = "Daniela Jojoa"
updates = {
    "name": "Daniela Jojoa",
    "address/city": "Bogota DC"
}
db.reference(f'users/{user_id}').update(updates)
print(f"Datos del usuario {user_id} actualizados.")

#Actualizar el nombre y añadir un campo de ciudad para un usuario específico,
user_id = "Ivan Santiesteban"
updates = {
    "name": "Ivan Santiesteban",
    "address/city": "Bogota DC"
}
db.reference(f'users/{user_id}').update(updates)
print(f"Datos del usuario {user_id} actualizados.")

#Actualizar el nombre y añadir un campo de ciudad para un usuario específico,
user_id = "Juan Sanchez"
updates = {
    "name": "Juan Sanchez",
    "address/city": "Bogota DC"
}
db.reference(f'users/{user_id}').update(updates)
print(f"Datos del usuario {user_id} actualizados.")

# Eliminar un campo específico (ej: la edad de un usuario)
user_id = "Juan Sanchez"
db.reference(f'users/{user_id}/address/city').delete()
print(f"Campo 'address/city' eliminado para el usuario {user_id}.")

# Eliminar un nodo completo (ej: un usuario completo)
# db.reference(f'users/{user_id}').delete()
# print(f"Usuario {user_id} eliminado.")

########################################################################