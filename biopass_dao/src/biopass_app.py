import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
from src.usuario_dao import UsuarioDAO
from src.utils.camera_utils import CameraUtils


class BioPassApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BioPass DAO - Control de Acceso")
        self.root.geometry("800x600")

        # Label para el video
        self.lbl_video = tk.Label(root)
        self.lbl_video.pack(pady=10)

        # Botones
        self.btn_registrar = tk.Button(root, text="📷 Registrar Usuario", command=self.registrar_usuario,
                                       bg="#007bff", fg="white", font=("Arial", 12))
        self.btn_registrar.pack(side=tk.LEFT, padx=50, pady=20)

        self.btn_login = tk.Button(root, text="🔓 Entrar (Login)", command=self.login_usuario,
                                   bg="#28a745", fg="white", font=("Arial", 12))
        self.btn_login.pack(side=tk.RIGHT, padx=50, pady=20)

        # Iniciar Cámara
        self.cap = cv2.VideoCapture(0)
        self.actualizar_camara()

    def actualizar_camara(self):
        ret, frame = self.cap.read()
        if ret:

            rostro = CameraUtils.detectar_rostro(frame)


            if rostro is not None:
                x, y, w, h = rostro
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.lbl_video.imgtk = img_tk
            self.lbl_video.configure(image=img_tk)

        self.root.after(10, self.actualizar_camara)

    def registrar_usuario(self):

        nombre = simpledialog.askstring("Registro", "Introduce tu nombre:")
        if not nombre: return


        ret, frame = self.cap.read()
        if ret:
            rostro = CameraUtils.detectar_rostro(frame)

            # CORRECCIÓN AQUÍ
            if rostro is not None:
                x, y, w, h = rostro
                cara_recortada = frame[y:y + h, x:x + w]

                # 3. Procesar imagen
                foto_bytes = CameraUtils.convertir_a_bytes(cara_recortada)

                # 4. Guardar usando el DAO
                if foto_bytes:
                    UsuarioDAO.registrar_usuario(nombre, foto_bytes)
                    messagebox.showinfo("Éxito", f"Usuario {nombre} registrado.")
            else:
                messagebox.showerror("Error", "No se detecta ninguna cara.")

    def login_usuario(self):
        # 1. Obtener datos de BD (DAO)
        usuarios = UsuarioDAO.obtener_todos()
        if not usuarios:
            messagebox.showwarning("Aviso", "No hay usuarios registrados.")
            return

        # 2. Capturar foto actual
        ret, frame = self.cap.read()
        if ret:
            rostro = CameraUtils.detectar_rostro(frame)

            # CORRECCIÓN AQUÍ
            if rostro is not None:
                x, y, w, h = rostro
                cara_gris = cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)

                # 3. Reconocimiento
                resultado = CameraUtils.entrenar_y_predecir(usuarios, cara_gris)

                if resultado != "Desconocido" and resultado != "Error Datos":
                    messagebox.showinfo("ACCESO CONCEDIDO", f"Bienvenido, {resultado} ✅")
                else:
                    messagebox.showerror("ACCESO DENEGADO", "No te reconozco ❌")
            else:
                messagebox.showerror("Error", "Ponte frente a la cámara.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BioPassApp(root)
    root.mainloop()