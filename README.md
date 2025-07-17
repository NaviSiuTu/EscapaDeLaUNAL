# 👑 Escapa de la UNAL: El videojuego 🐐

> Una aventura interactiva desarrollada en Python donde debes escapar del campus UNAL (Universidad Nacional de Colombia) pasando a través de diferentes mapas de edificios icónicos de la misma superando laberintos y evadiendo a la Cabra de la UniAndes... con ayuda de tus poderes tematizados de acuerdo a la Universidad, BIENVENIDO!!

---

## GAMEPLAY DE LA DEMO

![Click para ver la demo](https://github.com/user-attachments/assets/5b4e4508-f6ad-4508-835e-a49ea079c293) <!-- Puedes cambiar esto por un GIF o video tuyo -->

---

##  Tecnologías y librerías usadas para la realización de este proyecto:

* Python 3.13
* Pygame 2.5.5
* SpeechRecognition (control por voz)
* Firebase Realtime Database (bolsa y tienda)
* Generador DFS adaptado a los limites de los mapas

---

##  Características principales

* Laberintos aleatorios con estructura laberíntica estratégica (el jugador debe saber que movimientos hacer para moverse en el laberinto)
* Control de jugador con teclado o voz
* Bolsa visual con botones interactivos (aquí se encuentran los poderes
* Poderes:

  * **Tula Bienestar UN**: te protege de un golpe y activa inmunidad temporal
  * **Tinto cafetería UNAL**: aumenta velocidad del jugador
  * **Sticker UNAL**: ralentiza a la cabra (enemigo)
* Enemigo con IA que sigue tu rastro como en el juego *Tomb of the Mask*
* Movimiento del jugador estilo *Tomb of the Mask*
---

##  Controles

| Acción        | Tecla / Voz          |
| ------------- | -------------------- |
| Moverse       | W / A / S / D o voz  |
| Pausar juego  | P o botón visual     |
| Abrir Bolsa   | B o botón visual     |
| Activar Poder | Botón desde la bolsa |

Comandos por voz soportados: "arriba, sube o adelante" , "abajo o baja", "izquierda o izquierdo", "derecha o derecho"

---

##  Instalación

```bash
# Clona el repositorio
Puedes descargar los archivos del juego descargando el .zip de este repositorio

# Entra al directorio
cd escapa-unal
también puedes usar Visual Studio Code

# Instala dependencias
pip install pygame
pip install SpeechRecognition
pip install pyaudio       # Para capturar audio (requerido por SpeechRecognition)
pip install firebase-admin

# Ejecuta el juego
python login.py
```

---

##  Ideas futuras

*  Diálogos narrativos entre niveles
*  Más mapas: edificios icónicos de la Universidad
*  Sistema de movimiento por voz más robusto
*  Tabla global de monedas

---

##  Autores

Desarrollado por **Iván Santisteban**, **Daniela Pantoja**, **Eduardo Sanchez**

## 🎇ARCHIVO DE DOCUMENTACIÓN DEL PROYECTO:
![Click para ver la documentación]

💬 "La educación es la clave... pero escapar también cuenta"

---
