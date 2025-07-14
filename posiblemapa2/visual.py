import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Colores personalizados (puedes cambiarlos a gusto)
color_map = {
    0: "#000000",  # fondo (negro)
    1: "#FFFFFF",  # camino o píldora blanca
    2: "#FFAAAA",  # especial (puede ser checkpoint, etc)
    3: "#0044AA",  # muro
    4: "#AAAAAA",  # camino gris claro
    5: "#0055FF",  # esquina derecha
    6: "#0055FF",  # esquina izquierda
    7: "#0055FF",  # esquina arriba
    8: "#0055FF",  # esquina abajo
    9: "#888888",  # otro tipo de muro
}

# Usar el board que enviaste
board = [...]  # (copiar el board gigante aquí)

# Convertir el board en una imagen usando los colores
height = len(board)
width = len(board[0])
image = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
    for x in range(width):
        hex_color = color_map.get(board[y][x], "#000000")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        image[y, x] = rgb

# Mostrar la imagen
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis('off')
plt.title("Visualización del Board Píxel")
plt.show()
