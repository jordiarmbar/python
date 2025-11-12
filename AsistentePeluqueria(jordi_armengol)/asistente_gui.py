import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END, messagebox
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- SECCIÓN DE ESTILO (TUS COLORES) ---
BG_APP = "#F216A8"      # El color de fondo
TEXT_COLOR = "white"    # El color del texto

BG_CHAT = "#F216A8"      # Fondo del chat
BG_ENTRY = "#F216A8"     # Fondo del cuadro de texto

BUTTON_BG = "#B016F2"    # Botón de enviar
BUTTON_FG = "#FFFFFF"    # Texto del botón enviar
BORDER_COLOR = "#B016F2"   # El color del borde

FONT_MAIN = ("Comic Sans MS", 11)
FONT_BOLD = ("Comic Sans MS", 11, "bold")

load_dotenv()
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    messagebox.showerror("Error",
                         "No se encontró la API_KEY. Asegúrate de crear un archivo .env con 'API_KEY=tu_clave'")
    exit()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    messagebox.showerror("Error de Configuración de API", f"No se pudo configurar la API de Gemini: {e}")
    exit()

try:
    with open("servicios.txt", "r", encoding="utf-8") as f:
        info_peluqueria = f.read()
except FileNotFoundError:
    messagebox.showerror("Error de Archivo", "No se encontró el archivo 'servicios.txt' en la misma carpeta.")
    exit()

contexto_base = f"""
Eres un asistente virtual amable y profesional de la "Peluquería Armengol".
Tu tarea es responder las preguntas de los clientes basándote ÚNICAMENTE en la siguiente información:

--- INFORMACIÓN DE LA PELUQUERÍA ---
{info_peluqueria}
--- FIN DE LA INFORMACIÓN ---

Reglas para responder:
1.  Sé siempre amable y servicial.
2.  Si el cliente pregunta por algo que NO está en la lista (como "manicura" o "citas"),
    debes responder amablemente que no ofreces ese servicio o que no se necesita cita.
3.  No inventes precios ni horarios. Si no sabes la respuesta, di que no tienes esa información.
4.  Responde de forma concisa y clara.
"""

def enviar_consulta():
    pregunta_usuario = entrada_usuario.get()

    if not pregunta_usuario.strip():
        return

    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, "Tú: ", "user_tag")
    area_chat.insert(tk.END, f"{pregunta_usuario}\n\n")
    area_chat.config(state=tk.DISABLED)
    entrada_usuario.delete(0, END)

    prompt_completo = contexto_base + f"Pregunta del cliente: {pregunta_usuario}"

    try:
        area_chat.config(state=tk.NORMAL)
        area_chat.insert(tk.END, "Asistente: Escribiendo...\n\n", "assist_tag")
        area_chat.config(state=tk.DISABLED)
        area_chat.see(tk.END)
        root.update_idletasks()

        response = model.generate_content(prompt_completo)
        respuesta_ia = response.text

        area_chat.config(state=tk.NORMAL)
        area_chat.delete("end-3l", "end-1l")
        area_chat.insert(tk.END, "Asistente: ", "assist_tag_bold")
        area_chat.insert(tk.END, f"{respuesta_ia}\n\n")
        area_chat.config(state=tk.DISABLED)

    except Exception as e:
        area_chat.config(state=tk.NORMAL)
        area_chat.delete("end-3l", "end-1l")
        area_chat.insert(tk.END, f"Asistente: Lo siento, ha ocurrido un error. {e}\n\n", "error_tag")
        area_chat.config(state=tk.DISABLED)

    area_chat.see(tk.END)



root = tk.Tk()
root.title("Asistente de Peluquería Armengol")
root.geometry("500x600")
try:
    root.iconbitmap("icon.ico")
except tk.TclError:
    print("No se pudo encontrar el archivo de ícono 'icon.ico'")
root.config(bg=BG_APP)

frame_principal = tk.Frame(root, padx=10, pady=10, bg=BG_APP)
frame_principal.pack(expand=True, fill=tk.BOTH)


area_chat = scrolledtext.ScrolledText(
    frame_principal,
    wrap=tk.WORD,
    state=tk.DISABLED,
    font=FONT_MAIN,
    bg=BG_CHAT,
    fg=TEXT_COLOR,
    padx=5,
    pady=5,
    relief=tk.FLAT,
    bd=0,
    highlightthickness=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=BORDER_COLOR
)
area_chat.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)


area_chat.tag_configure("user_tag", font=FONT_BOLD, foreground=TEXT_COLOR)
area_chat.tag_configure("assist_tag_bold", font=FONT_BOLD, foreground=TEXT_COLOR)
area_chat.tag_configure("assist_tag", foreground=TEXT_COLOR)
area_chat.tag_configure("error_tag", foreground="#FF0000", font=FONT_BOLD) # Error en ROJO



area_chat.config(state=tk.NORMAL)
area_chat.insert(tk.END, "Asistente: ", "assist_tag_bold")
area_chat.insert(tk.END,
                 "¡Hola! Bienvenido al Asistente de Peluquería Armengol. Escribe tu pregunta abajo.\n\n")
area_chat.config(state=tk.DISABLED)


entrada_usuario = Entry(
    frame_principal,
    font=FONT_MAIN,
    bg=BG_ENTRY,
    fg=TEXT_COLOR,
    relief=tk.FLAT,
    insertbackground=TEXT_COLOR,
    bd=0,
    highlightthickness=2,
    highlightbackground=BORDER_COLOR,
    highlightcolor=BORDER_COLOR
)
entrada_usuario.pack(fill=tk.X, padx=5, pady=5, ipady=8)


boton_enviar = Button(
    frame_principal,
    text="Enviar",
    command=enviar_consulta,
    font=FONT_BOLD,
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    bd=0,
    relief=tk.FLAT,
    activebackground="#8A0BC2",
    activeforeground=BUTTON_FG
)
boton_enviar.pack(fill=tk.X, padx=5, pady=(0, 5), ipady=5)

root.bind('<Return>', lambda event: enviar_consulta())
root.mainloop()