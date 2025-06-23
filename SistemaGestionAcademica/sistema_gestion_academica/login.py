# login.py
import tkinter as tk
from tkinter import messagebox

def validar_login(usuario, clave):
    return usuario == "admin" and clave == "1234"

def mostrar_login(abrir_menu):
    ventana = tk.Tk()
    ventana.title("Login")
    ventana.geometry("300x150")

    tk.Label(ventana, text="Usuario").pack()
    usuario = tk.Entry(ventana)
    usuario.pack()

    tk.Label(ventana, text="Contraseña").pack()
    clave = tk.Entry(ventana, show="*")
    clave.pack()

    def login():
        if validar_login(usuario.get(), clave.get()):
            ventana.destroy()
            abrir_menu()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(ventana, text="Ingresar", command=login).pack()
    ventana.mainloop()