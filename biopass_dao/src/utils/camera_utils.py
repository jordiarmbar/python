import cv2
import numpy as np


class CameraUtils:

    @staticmethod
    def detectar_rostro(frame):
        """Devuelve las coordenadas (x,y,w,h) de la cara"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Usamos el clasificador pre-entrenado de Haar
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            return faces[0]
        return None

    @staticmethod
    def convertir_a_bytes(imagen_cv2):
        """Codifica la imagen a formato JPG en bytes para la BD"""
        success, encoded_img = cv2.imencode('.jpg', imagen_cv2)
        if success:
            return encoded_img.tobytes()
        return None

    @staticmethod
    def bytes_a_imagen(img_bytes):
        """Decodifica los bytes de la BD de vuelta a imagen OpenCV"""
        # Convertir memoryview a bytes si es necesario
        if isinstance(img_bytes, memoryview):
            img_bytes = bytes(img_bytes)

        nparr = np.frombuffer(img_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def entrenar_y_predecir(lista_usuarios, foto_actual_gris):
        """Entrena el modelo LBPH al vuelo y predice la foto actual"""
        if not lista_usuarios:
            return "Sin usuarios"

        rostros = []
        etiquetas = []
        mapa_nombres = {}

        # 1. Preparar datos de entrenamiento
        for usuario in lista_usuarios:
            user_id, nombre, foto_data = usuario
            rostro = CameraUtils.bytes_a_imagen(foto_data)

            if rostro is not None:
                # TRUCO 1: Ecualizar histograma (Mejora el contraste y la luz)
                rostro = cv2.equalizeHist(rostro)

                rostro = cv2.resize(rostro, (100, 100))
                rostros.append(rostro)
                etiquetas.append(user_id)
                mapa_nombres[user_id] = nombre

        if not rostros:
            return "Error Datos"

        # 2. Entrenar reconocedor
        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.train(rostros, np.array(etiquetas))

        # 3. Predecir
        # TRUCO 1 (Aplicado también a la foto actual)
        foto_actual_gris = cv2.equalizeHist(foto_actual_gris)

        foto_actual_resized = cv2.resize(foto_actual_gris, (100, 100))
        label, confianza = reconocedor.predict(foto_actual_resized)

        print(f"DEBUG -> Usuario: {mapa_nombres.get(label)} | Distancia: {confianza}")

        # TRUCO 2: Subir el límite de tolerancia (De 70 a 90 o 100)
        # Menor confianza = Más parecido. Si ponemos 100, es más fácil entrar.
        if confianza < 100:
            return mapa_nombres.get(label, "Desconocido")
        else:
            return "Desconocido"