# estudiantes.py
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

# Ruta absoluta al archivo de base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'academico.db')

def ventana_estudiantes():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Estudiantes")
    ventana.geometry("600x550")
    ventana.grab_set()

    # --- Funciones ---
    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_apellido.delete(0, tk.END)
        entrada_grado.delete(0, tk.END)
        entrada_seccion.delete(0, tk.END)

    def actualizar_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Estudiante")
        for row in cursor.fetchall():
            tabla.insert("", tk.END, values=row)
        conexion.close()

    def guardar_estudiante():
        id_est = entrada_id.get()
        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()
        grado = entrada_grado.get()
        seccion = entrada_seccion.get()

        if not (id_est and nombre and apellido and grado and seccion):
            messagebox.showwarning("Campos incompletos", "Complete todos los campos.")
            return
        if not id_est.isdigit():
            messagebox.showerror("Error", "El ID debe ser numérico.")
            return

        id_est = int(id_est)

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Estudiante WHERE id_estudiante = ?", (id_est,))
        if cursor.fetchone():
            messagebox.showerror("ID duplicado", f"Ya existe un estudiante con ID {id_est}")
        else:
            cursor.execute("INSERT INTO Estudiante (id_estudiante, nombre, apellido, grado, seccion) VALUES (?, ?, ?, ?, ?)",
                           (id_est, nombre, apellido, grado, seccion))
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante guardado.")
            actualizar_tabla()
            limpiar()
        conexion.close()

    def buscar_estudiante():
        id_est = entrada_id.get()
        if not id_est.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido.")
            return
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Estudiante WHERE id_estudiante = ?", (id_est,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            entrada_nombre.delete(0, tk.END)
            entrada_apellido.delete(0, tk.END)
            entrada_grado.delete(0, tk.END)
            entrada_seccion.delete(0, tk.END)

            entrada_nombre.insert(0, resultado[1])
            entrada_apellido.insert(0, resultado[2])
            entrada_grado.insert(0, resultado[3])
            entrada_seccion.insert(0, resultado[4])
        else:
            messagebox.showinfo("No encontrado", "Estudiante no existe.")

    def modificar_estudiante():
        id_est = entrada_id.get()
        if not id_est.isdigit():
            messagebox.showerror("Error", "ID inválido.")
            return

        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()
        grado = entrada_grado.get()
        seccion = entrada_seccion.get()

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("""UPDATE Estudiante 
                          SET nombre = ?, apellido = ?, grado = ?, seccion = ?
                          WHERE id_estudiante = ?""",
                       (nombre, apellido, grado, seccion, id_est))
        if cursor.rowcount == 0:
            messagebox.showwarning("Error", "No se encontró ese ID para modificar.")
        else:
            messagebox.showinfo("Modificado", "Estudiante actualizado.")
        conexion.commit()
        conexion.close()
        actualizar_tabla()
        limpiar()

    def eliminar_estudiante():
        id_est = entrada_id.get()
        if not id_est.isdigit():
            messagebox.showerror("Error", "ID inválido.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este estudiante?")
        if respuesta:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Estudiante WHERE id_estudiante = ?", (id_est,))
            if cursor.rowcount == 0:
                messagebox.showwarning("Error", "No se encontró ese ID para eliminar.")
            else:
                messagebox.showinfo("Eliminado", "Estudiante eliminado.")
            conexion.commit()
            conexion.close()
            actualizar_tabla()
            limpiar()

    # --- Widgets ---
    tk.Label(ventana, text="ID Estudiante (manual)").pack()
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()

    tk.Label(ventana, text="Nombre").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Apellido").pack()
    entrada_apellido = tk.Entry(ventana)
    entrada_apellido.pack()

    tk.Label(ventana, text="Grado").pack()
    entrada_grado = tk.Entry(ventana)
    entrada_grado.pack()

    tk.Label(ventana, text="Sección").pack()
    entrada_seccion = tk.Entry(ventana)
    entrada_seccion.pack()

    # Botones funcionales
    tk.Button(ventana, text="Guardar", command=guardar_estudiante).pack(pady=3)
    tk.Button(ventana, text="Buscar", command=buscar_estudiante).pack(pady=3)
    tk.Button(ventana, text="Modificar", command=modificar_estudiante).pack(pady=3)
    tk.Button(ventana, text="Eliminar", command=eliminar_estudiante).pack(pady=3)
    tk.Button(ventana, text="Limpiar", command=limpiar).pack(pady=3)

    # Tabla
    tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Apellido", "Grado", "Sección"), show="headings")
    for col in ("ID", "Nombre", "Apellido", "Grado", "Sección"):
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(pady=10)

    # Botón regresar en esquina inferior derecha
    tk.Button(ventana, text="Regresar al Menú Principal", command=ventana.destroy)\
        .place(relx=0.95, rely=0.95, anchor="se")

    actualizar_tabla()

