import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import subprocess
import sys

# Ruta al GIF
gif_path = "IMAGENES/Splashjiji.gif"
app_path = "APP_INTERFAZ.py"  # Cambia esto por el nombre real de tu app

# Verificar si el gif y la app existen
if not os.path.exists(gif_path):
    print(f"✗ ERROR: No se encontró el archivo '{gif_path}'")
    sys.exit(1)

if not os.path.exists(app_path):
    print(f"✗ ERROR: No se encontró el archivo principal '{app_path}'")
    sys.exit(1)

# Crear ventana splash
splash = tk.Tk()
splash.title("Bienvenido al laberinto")
splash.geometry("400x500")
splash.overrideredirect(True)

# Cargar los frames del GIF
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

canvas = tk.Canvas(splash, width=400, height=500, highlightthickness=0)
canvas.pack()
gif_frame = canvas.create_image(200, 250, image=frames[0])

# Variable de control
animacion_terminada = False

# Función para lanzar la app principal
def lanzar_app_principal(event=None):
    if animacion_terminada:
        splash.destroy()
        subprocess.Popen(["python", app_path])

# Animación del GIF
def reproducir_gif(frame_idx=0):
    global animacion_terminada
    if frame_idx < len(frames):
        canvas.itemconfig(gif_frame, image=frames[frame_idx])
        splash.after(33, reproducir_gif, frame_idx + 1)
    else:
        animacion_terminada = True
        canvas.itemconfig(gif_frame, image=frames[-1])  # Queda en el último frame
        canvas.bind("<Button-1>", lanzar_app_principal)  # Espera clic

# Iniciar animación
reproducir_gif()
splash.mainloop()




