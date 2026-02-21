import tkinter as tk
from tkinter import messagebox
from voice_service import VoiceService
from auth_dao import AuthDAO


class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit System")
        self.voice = VoiceService()
        self.dao = AuthDAO()

        # UI Básica
        tk.Label(root, text="Usuario:").pack()
        self.ent_user = tk.Entry(root)
        self.ent_user.pack()

        tk.Button(root, text="Registrar con Voz", command=self.registrar).pack(pady=5)
        tk.Button(root, text="Login por Voz", command=self.login).pack(pady=5)
        tk.Button(root, text="Ver Auditoría Crítica", command=self.auditoria).pack(pady=5)

        self.txt_logs = tk.Text(root, height=10, width=50)
        self.txt_logs.pack()

    def registrar(self):
        user = self.ent_user.get()
        frase, confianza, lat = self.voice.capturar_frase()
        if frase:
            confirmar = messagebox.askyesno("Confirmar", f"¿Tu frase es: '{frase}'?")
            if confirmar:
                log_ini = {"status": "OK", "confianza": confianza, "latencia": f"{lat}s"}
                self.dao.registrar_usuario(user, frase, log_ini)
                messagebox.showinfo("Éxito", "Usuario registrado")

    def login(self):
        user = self.ent_user.get()
        frase, confianza, lat = self.voice.capturar_frase()
        res = self.dao.verificar_login(user, frase, confianza, lat)
        messagebox.showinfo("Resultado", res)

    def auditoria(self):
        registros = self.dao.obtener_auditoria()
        self.txt_logs.delete('1.0', tk.END)
        for r in registros:
            self.txt_logs.insert(tk.END, f"Usuario: {r[0]} | Status: {r[1]} | Data: {r[2]}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()