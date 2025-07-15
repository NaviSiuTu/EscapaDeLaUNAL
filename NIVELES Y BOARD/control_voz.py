# control_voz.py
import speech_recognition as sr
import threading

ultima_orden = None  # Guarda el último comando reconocido

def iniciar_escucha():
    def escuchar():
        global ultima_orden
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        print("[🎤] Control por voz activado...")

        while True:
            with mic as source:
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.1)
                    print("🎙️ Escuchando...")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=1.2)
                except sr.WaitTimeoutError:
                    continue

            try:
                comando = recognizer.recognize_google(audio, language="es-ES").lower()
                print(f"[👂] Reconocido: {comando}")

                if "arriba" in comando or "sube" in comando or "adelante" in comando:
                    ultima_orden = "w"
                elif "abajo" in comando or "baja" in comando:
                    ultima_orden = "s"
                elif "izquierda" in comando or "izquierdo" in comando:
                    ultima_orden = "a"
                elif "derecha" in comando or "derecho" in comando:
                    ultima_orden = "d"
                else:
                    print("❓ Comando no reconocido")

            except sr.UnknownValueError:
                print("🤷 No entendí lo que dijiste.")
            except sr.RequestError:
                print("🚫 No se pudo conectar con Google.")
            except Exception as e:
                print(f"⚠️ Error inesperado: {e}")

    hilo = threading.Thread(target=escuchar, daemon=True)
    hilo.start()

def obtener_orden():
    global ultima_orden
    orden = ultima_orden
    ultima_orden = None  # limpiar el buffer
    return orden


