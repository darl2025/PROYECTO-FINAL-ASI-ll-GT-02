#notas.py
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'academico.db')


def ventana_notas():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Notas")
    ventana.geometry("600x450")

    def guardar_nota():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Nota (valor, id_estudiante) VALUES (?, ?)",
                       (entrada_nota.get(), entrada_id_estudiante.get()))
        conexion.commit()
        conexion.close()
        limpiar_campos()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Nota guardada correctamente.")

    def buscar_nota():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Nota WHERE id_nota = ?", (entrada_nota_id.get(),))
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            entrada_id_estudiante.delete(0, tk.END)
            entrada_nota.delete(0, tk.END)
            entrada_id_estudiante.insert(0, resultado[2])
            entrada_nota.insert(0, resultado[1])
        else:
            messagebox.showerror("Error", "Nota no encontrada.")

    def modificar_nota():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("UPDATE Nota SET valor = ?, id_estudiante = ? WHERE id_nota = ?",
                       (entrada_nota.get(), entrada_id_estudiante.get(), entrada_nota_id.get()))
        conexion.commit()
        conexion.close()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Nota modificada correctamente.")

    def eliminar_nota():
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Nota WHERE id_nota = ?", (entrada_nota_id.get(),))
        conexion.commit()
        conexion.close()
        limpiar_campos()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Nota eliminada correctamente.")

    def limpiar_campos():
        entrada_nota_id.delete(0, tk.END)
        entrada_id_estudiante.delete(0, tk.END)
        entrada_nota.delete(0, tk.END)

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Nota")
        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)
        conexion.close()

    tk.Label(ventana, text="ID Nota:").pack()
    entrada_nota_id = tk.Entry(ventana)
    entrada_nota_id.pack()

    tk.Label(ventana, text="ID Estudiante:").pack()
    entrada_id_estudiante = tk.Entry(ventana)
    entrada_id_estudiante.pack()

    tk.Label(ventana, text="Nota:").pack()
    entrada_nota = tk.Entry(ventana)
    entrada_nota.pack()

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=guardar_nota).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Buscar", command=buscar_nota).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Modificar", command=modificar_nota).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_nota).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=4, padx=5)

    tabla = ttk.Treeview(ventana, columns=("ID", "Nota", "ID Estudiante"), show="headings")
    for col in ("ID", "Nota", "ID Estudiante"):
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(pady=10)

    tk.Button(ventana, text="Regresar al Menú Principal", command=ventana.destroy).pack(pady=5)
    actualizar_tabla()