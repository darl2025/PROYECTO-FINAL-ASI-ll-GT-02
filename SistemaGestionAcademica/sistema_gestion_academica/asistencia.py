#asistencia.py
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk
from datetime import date
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'academico.db')


def ventana_asistencia():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Asistencia")
    ventana.geometry("600x450")

    def guardar_asistencia():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Asistencia (fecha, presente, id_estudiante) VALUES (?, ?, ?)",
                       (entrada_fecha.get(), presente_var.get(), entrada_id_estudiante.get()))
        conexion.commit()
        conexion.close()
        limpiar_campos()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")

    def buscar_asistencia():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Asistencia WHERE id_asistencia = ?", (entrada_asistencia_id.get(),))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            entrada_fecha.delete(0, tk.END)
            entrada_id_estudiante.delete(0, tk.END)
            presente_var.set(bool(resultado[2]))
            entrada_fecha.insert(0, resultado[1])
            entrada_id_estudiante.insert(0, resultado[3])
        else:
            messagebox.showerror("Error", "Asistencia no encontrada.")

    def modificar_asistencia():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("UPDATE Asistencia SET fecha = ?, presente = ?, id_estudiante = ? WHERE id_asistencia = ?",
                       (entrada_fecha.get(), presente_var.get(), entrada_id_estudiante.get(), entrada_asistencia_id.get()))
        conexion.commit()
        conexion.close()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Asistencia modificada correctamente.")

    def eliminar_asistencia():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Asistencia WHERE id_asistencia = ?", (entrada_asistencia_id.get(),))
        conexion.commit()
        conexion.close()
        limpiar_campos()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Asistencia eliminada correctamente.")

    def limpiar_campos():
        entrada_asistencia_id.delete(0, tk.END)
        entrada_fecha.delete(0, tk.END)
        entrada_id_estudiante.delete(0, tk.END)
        presente_var.set(False)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Asistencia")
        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)
        conexion.close()

    tk.Label(ventana, text="ID Asistencia:").pack()
    entrada_asistencia_id = tk.Entry(ventana)
    entrada_asistencia_id.pack()

    tk.Label(ventana, text="Fecha (AAAA-MM-DD):").pack()
    entrada_fecha = tk.Entry(ventana)
    entrada_fecha.insert(0, date.today().isoformat())
    entrada_fecha.pack()

    tk.Label(ventana, text="ID Estudiante:").pack()
    entrada_id_estudiante = tk.Entry(ventana)
    entrada_id_estudiante.pack()

    presente_var = tk.BooleanVar()
    tk.Checkbutton(ventana, text="Presente", variable=presente_var).pack()

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=guardar_asistencia).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Buscar", command=buscar_asistencia).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Modificar", command=modificar_asistencia).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_asistencia).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=4, padx=5)

    tabla = ttk.Treeview(ventana, columns=("ID", "Fecha", "Presente", "ID Estudiante"), show="headings")
    for col in ("ID", "Fecha", "Presente", "ID Estudiante"):
        tabla.heading(col, text=col)
        tabla.column(col, width=130)
    tabla.pack(pady=10)

    tk.Button(ventana, text="Regresar al Menú Principal", command=ventana.destroy).pack(pady=5)
    actualizar_tabla()