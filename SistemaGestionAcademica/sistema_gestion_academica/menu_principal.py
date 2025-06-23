# menu_principal.py
import tkinter as tk
from tkinter import messagebox
from sistema_gestion_academica.estudiantes import ventana_estudiantes
from sistema_gestion_academica.notas import ventana_notas
from sistema_gestion_academica.asistencia import ventana_asistencia
from sistema_gestion_academica.reportes import ventana_reportes

def abrir_menu():
    root = tk.Tk()
    root.title("Sistema de Gestión Académica")
    root.geometry("400x350")

    tk.Button(root, text="Estudiantes", command=ventana_estudiantes).pack(pady=10)
    tk.Button(root, text="Notas", command=ventana_notas).pack(pady=10)
    tk.Button(root, text="Asistencia", command=ventana_asistencia).pack(pady=10)
    tk.Button(root, text="Generar Reportes", command=ventana_reportes).pack(pady=10)

    # Botón de salir con confirmación
    def confirmar_salida():
        if messagebox.askokcancel("Salir", "¿Estás seguro que deseas salir del sistema?"):
            root.destroy()

    boton_salir = tk.Button(root, text="Salir", command=confirmar_salida)
    boton_salir.place(relx=0.95, rely=0.95, anchor="se")

    root.mainloop()
