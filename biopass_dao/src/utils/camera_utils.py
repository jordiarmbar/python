import cv2
import numpy as np


class CameraUtils:

    @staticmethod
    def detectar_rostro(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            return faces[0]
        return None

    @staticmethod
    def convertir_a_bytes(imagen_cv2):

        success, encoded_img = cv2.imencode('.jpg', imagen_cv2)
        if success:
            return encoded_img.tobytes()
        return None

    @staticmethod
    def bytes_a_imagen(img_bytes):

        if isinstance(img_bytes, memoryview):
            img_bytes = bytes(img_bytes)

        nparr = np.frombuffer(img_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def entrenar_y_predecir(lista_usuarios, foto_actual_gris):

        if not lista_usuarios:
            return "Sin usuarios"

        rostros = []
        etiquetas = []
        mapa_nombres = {}


        for usuario in lista_usuarios:
            user_id, nombre, foto_data = usuario
            rostro = CameraUtils.bytes_a_imagen(foto_data)

            if rostro is not None:

                rostro = cv2.equalizeHist(rostro)

                rostro = cv2.resize(rostro, (100, 100))
                rostros.append(rostro)
                etiquetas.append(user_id)
                mapa_nombres[user_id] = nombre

        if not rostros:
            return "Error Datos"


        reconocedor = cv2.face.LBPHFaceRecognizer_create()
        reconocedor.train(rostros, np.array(etiquetas))


        foto_actual_gris = cv2.equalizeHist(foto_actual_gris)

        foto_actual_resized = cv2.resize(foto_actual_gris, (100, 100))
        label, confianza = reconocedor.predict(foto_actual_resized)

        print(f"DEBUG -> Usuario: {mapa_nombres.get(label)} | Distancia: {confianza}")


        if confianza < 100:
            return mapa_nombres.get(label, "Desconocido")
        else:
            return "Desconocido"