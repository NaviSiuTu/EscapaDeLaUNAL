import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import firebase_admin
from firebase_admin import credentials, db
import subprocess
import os

# ============================
# CONFIGURACIÓN FIREBASE
# ============================
if not firebase_admin._apps:
    cred = credentials.Certificate("base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-281358fd83.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"
    })

# ============================
# AUTENTICACIÓN DE USUARIO
# ============================
def authenticate_user(email, password):
    users_ref = db.reference('users')
    users = users_ref.get()

    if not users:
        return None

    for _, user_data in users.items():
        if isinstance(user_data, dict) and user_data.get('email') == email and user_data.get('Contraseña') == password:
            return user_data
    return None

# ============================
# FUNCIÓN DE LOGIN
# ============================
def main():
    global root, username_entry, password_entry

    root = tk.Tk()
    root.title("Login Retro")
    root.geometry("400x500")
    root.resizable(False, False)

    marco_img = Image.open("IMAGENES/Menu.png").resize((417, 497))
    marco_tk = ImageTk.PhotoImage(marco_img)

    logo_img = Image.open("IMAGENES/Menu (1).png").resize((130, 130))
    logo_tk = ImageTk.PhotoImage(logo_img)

    canvas = tk.Canvas(root, width=400, height=500, highlightthickness=0)
    canvas.pack()
    canvas.create_image(200, 250, image=marco_tk)
    canvas.create_image(200, 120, image=logo_tk)

    tk.Label(root, text="EMAIL", font=("Courier", 10, "bold"), bg="#00C000", fg="black").place(x=100, y=180)
    tk.Label(root, text="CONTRASEÑA", font=("Courier", 10, "bold"), bg="#00C000", fg="black").place(x=100, y=230)

    username_entry = tk.Entry(root, font=("Courier", 10), justify="center", bg="#00C000", fg="black")
    password_entry = tk.Entry(root, font=("Courier", 10), show="*", justify="center", bg="#00C000", fg="black")
    username_entry.place(x=100, y=200, width=200, height=30)
    password_entry.place(x=100, y=250, width=200, height=30)

    def intentar_login():
        email = username_entry.get().strip()
        password = password_entry.get().strip()

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Error", "Email debe tener formato válido (usuario@dominio.com).")
            return

        if not re.match(r"^[A-Za-z0-9]+$", password):
            messagebox.showerror("Error", "La contraseña no debe contener caracteres especiales.")
            return

        user = authenticate_user(email, password)
        if user:
            monedas = user.get('monedas') or user.get('Monedas') or 0
            abrir_menu_principal(user['name'], monedas)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(root, text="LOGIN", font=("Courier", 10, "bold"), bg="black", fg="white", command=intentar_login).place(x=150, y=310, width=100, height=35)
    tk.Button(root, text="REGISTRARSE", font=("Courier", 10, "bold"), bg="black", fg="white", command=abrir_ventana_registro).place(x=130, y=360, width=140, height=35)

    root.mainloop()

# ============================
# FUNCIÓN DE REGISTRO
# ============================
def abrir_ventana_registro():
    root.destroy()

    ventana = tk.Tk()
    ventana.title("Registro Retro")
    ventana.geometry("400x500")
    ventana.resizable(False, False)

    marco_img = Image.open("IMAGENES/Menu.png").resize((417, 497))
    marco_tk = ImageTk.PhotoImage(marco_img)

    logo_img = Image.open("IMAGENES/Menu (1).png").resize((130, 130))
    logo_tk = ImageTk.PhotoImage(logo_img)

    canvas = tk.Canvas(ventana, width=400, height=500, highlightthickness=0)
    canvas.pack()
    canvas.create_image(200, 250, image=marco_tk)
    canvas.create_image(200, 120, image=logo_tk)

    etiquetas = [
        ("NOMBRE COMPLETO", 160),
        ("EMAIL", 210),
        ("CONTRASEÑA", 260),
        ("CIUDAD", 310)
    ]
    for texto, y in etiquetas:
        tk.Label(ventana, text=texto, font=("Courier", 10, "bold"), bg="#00C000", fg="black").place(x=100, y=y)

    entry_name = tk.Entry(ventana, font=("Courier", 10), justify="center", bg="#00C000", fg="black")
    entry_email = tk.Entry(ventana, font=("Courier", 10), justify="center", bg="#00C000", fg="black")
    entry_pass = tk.Entry(ventana, font=("Courier", 10), show="*", justify="center", bg="#00C000", fg="black")
    entry_city = tk.Entry(ventana, font=("Courier", 10), justify="center", bg="#00C000", fg="black")

    entry_name.place(x=100, y=180, width=200, height=25)
    entry_email.place(x=100, y=230, width=200, height=25)
    entry_pass.place(x=100, y=280, width=200, height=25)
    entry_city.place(x=100, y=330, width=200, height=25)

    def registrar():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        password = entry_pass.get().strip()
        city = entry_city.get().strip()

        if not all([name, email, password, city]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messagebox.showerror("Error", "El email debe tener formato válido (usuario@dominio.com).")
            return

        if not re.match(r"^[A-Za-z0-9]+$", password):
            messagebox.showerror("Error", "La contraseña no debe contener caracteres especiales.")
            return

        users_ref = db.reference("users")
        users = users_ref.get() or {}

        for _, data in users.items():
            if isinstance(data, dict) and data.get("email") == email:
                messagebox.showerror("Error", "Este email ya está registrado.")
                return

        new_user = {
            "name": name,
            "email": email,
            "Contraseña": password,
            "roles": ["Jugador"],
            "monedas": 100,
            "is_active": True,
            "address": {"city": city}
        }

        user_id = name.replace(" ", "_")
        try:
            db.reference(f"users/{user_id}").set(new_user)
            messagebox.showinfo("Registro Exitoso", "¡Bienvenido al laberinto!")
            ventana.destroy()
            main()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    tk.Button(ventana, text="REGISTRAR", font=("Courier", 10, "bold"), bg="black", fg="white", command=registrar).place(x=150, y=380, width=100, height=30)
    tk.Button(ventana, text="VOLVER", font=("Courier", 10, "bold"), bg="#C00000", fg="white", command=lambda: [ventana.destroy(), main()]).place(x=150, y=420, width=100, height=30)

    ventana.mainloop()

# ============================
# MENÚ PRINCIPAL DESPUÉS DEL LOGIN
# ============================
def abrir_menu_principal(nombre_usuario, monedas):
    root.destroy()

    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("400x500")
    menu.resizable(False, False)

    marco_img = Image.open("IMAGENES/Menu.png").resize((417, 497))
    marco_tk = ImageTk.PhotoImage(marco_img)

    logo_img = Image.open("IMAGENES/Menu (1).png").resize((130, 130))
    logo_tk = ImageTk.PhotoImage(logo_img)

    canvas = tk.Canvas(menu, width=400, height=500, highlightthickness=0)
    canvas.pack()
    canvas.create_image(200, 250, image=marco_tk)
    canvas.create_image(200, 120, image=logo_tk)

    label_usuario = tk.Label(menu, text=f"¡Hola {nombre_usuario}!", font=("Courier", 12, "bold"), bg="#00C000", fg="black")
    label_usuario.place(relx=0.5, y=200, anchor="center")

    label_monedas = tk.Label(menu, text=f"Monedas: {monedas}", font=("Courier", 12), bg="#00C000", fg="black")
    label_monedas.place(relx=0.5, y=230, anchor="center")

    def abrir_seleccion_niveles():
        menu.destroy()
        abrir_menu_niveles()

    def lanzar_tienda():
        menu.destroy()
        abrir_tienda(nombre_usuario)

    tk.Button(menu, text="JUGAR NIVELES", font=("Courier", 10, "bold"), bg="black", fg="white", command=abrir_seleccion_niveles).place(x=130, y=280, width=140, height=35)
    tk.Button(menu, text="TIENDA", font=("Courier", 10, "bold"), bg="#FFA500", fg="black", command=lanzar_tienda).place(x=130, y=330, width=140, height=35)

    menu.mainloop()

# ============================
# MENÚ DE NIVELES
# ============================
def abrir_menu_niveles():
    ventana = tk.Tk()
    ventana.title("Seleccionar Nivel")
    ventana.geometry("400x500")
    ventana.resizable(False, False)

    marco_img = Image.open("IMAGENES/Menu.png").resize((417, 497))
    marco_tk = ImageTk.PhotoImage(marco_img)

    logo_img = Image.open("IMAGENES/Menu (1).png").resize((130, 130))
    logo_tk = ImageTk.PhotoImage(logo_img)

    canvas = tk.Canvas(ventana, width=400, height=500, highlightthickness=0)
    canvas.pack()
    canvas.create_image(200, 250, image=marco_tk)
    canvas.create_image(200, 120, image=logo_tk)

    tk.Label(ventana, text="SELECCIONA UN NIVEL", font=("Courier", 12, "bold"), bg="#00C000", fg="black").place(x=90, y=200)

    def lanzar_nivel_alpha():
        ventana.destroy()
        import sys, os
        sys.path.append(os.path.join(os.getcwd(), "Test_EDUN"))
        import nivel_alpha_juego
        nivel_alpha_juego.main()

    tk.Button(ventana, text="NIVEL ALPHA", font=("Courier", 10, "bold"), bg="#008000", fg="white", command=lanzar_nivel_alpha).place(x=130, y=250, width=140, height=35)
    tk.Button(ventana, text="VOLVER", font=("Courier", 10, "bold"), bg="black", fg="white", command=lambda: [ventana.destroy(), main()]).place(x=130, y=300, width=140, height=35)

    ventana.mainloop()

# ============================
# ABRIR TIENDA
# ============================
def abrir_tienda(nombre_usuario):
    nombre_formateado = nombre_usuario.replace(" ", "_").lower()
    script_path = os.path.join(os.getcwd(), "tienda.py")
    subprocess.Popen(["python", script_path, nombre_formateado])

# ============================
# EJECUCIÓN PRINCIPAL
# ============================
if __name__ == "__main__":
    main()
