import speech_recognition as sr
import time


class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def capturar_frase(self):
        """Fachada: gestiona micro, ruido y traducción en un solo paso."""
        inicio = time.time()
        with self.mic as source:
            print("Calibrando ruido ambiente...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Escuchando...")
            audio = self.recognizer.listen(source)

        fin = time.time()
        latencia = round(fin - inicio, 2)

        try:
            # Llamada al motor de Google (Facade oculta esta complejidad)
            data = self.recognizer.recognize_google(audio, language="es-ES", show_all=True)

            if not data or 'alternative' not in data:
                return None, 0, latencia

            mejor_opcion = data['alternative'][0]
            texto = mejor_opcion['transcript'].lower()
            confianza = mejor_opcion.get('confidence', 0.0)

            return texto, confianza, latencia
        except Exception:
            return None, 0, latencia