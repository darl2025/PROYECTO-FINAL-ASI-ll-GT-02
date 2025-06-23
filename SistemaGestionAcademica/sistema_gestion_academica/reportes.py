#reportes.py
import tkinter as tk
from fpdf import FPDF
import sqlite3
import os
import webbrowser
from datetime import date
from tkinter import messagebox, ttk

# Ruta absoluta al archivo de base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db', 'academico.db')
REPORTE_DIR = os.path.join(BASE_DIR, 'datos', 'reportes_pdf')
os.makedirs(REPORTE_DIR, exist_ok=True)


def ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Generación de Reportes")
    ventana.geometry("600x500")

    def generar_pdf():
        id_est = entrada_id.get()
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, apellido, grado, seccion FROM Estudiante WHERE id_estudiante = ?", (id_est,))
        estudiante = cursor.fetchone()
        cursor.execute("SELECT valor FROM Nota WHERE id_estudiante = ?", (id_est,))
        notas = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Reporte Académico", ln=True, align='C')

        if estudiante:
            pdf.cell(200, 10, txt=f"Estudiante: {estudiante[0]} {estudiante[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Grado: {estudiante[2]} - Sección: {estudiante[3]}", ln=True)
        pdf.cell(200, 10, txt="Notas:", ln=True)
        for nota in notas:
            pdf.cell(200, 10, txt=str(nota[0]), ln=True)

        # Generar nombre del archivo PDF
        if estudiante:
            nombre_archivo = f"reporte_{estudiante[0]}_{estudiante[1]}_{date.today().isoformat()}.pdf"
        else:
            nombre_archivo = f"reporte_{id_est}_{date.today().isoformat()}.pdf"
            pdf.cell(200, 10, txt=str(nota[0]), ln=True)

        # Generar nombre del archivo PDF
        if estudiante:
            nombre_archivo = f"reporte_{estudiante[0]}_{estudiante[1]}_{date.today().isoformat()}.pdf"
        else:
            nombre_archivo = f"reporte_{id_est}_{date.today().isoformat()}.pdf"
            pdf.cell(200, 10, txt=str(nota[0]), ln=True)

        os.makedirs("sistema_gestion_academica/datos/reportes_pdf", exist_ok=True)
        ruta_pdf = os.path.join(REPORTE_DIR, nombre_archivo)
        pdf.output(ruta_pdf)

        cursor.execute("INSERT INTO Reporte (fecha, ruta_pdf) VALUES (?, ?)", (date.today().isoformat(), ruta_pdf))
        conexion.commit()
        conexion.close()
        actualizar_tabla()
        messagebox.showinfo("Éxito", "Reporte generado exitosamente.")

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Reporte")
        for fila in cursor.fetchall():
            tabla.insert("", tk.END, values=fila)
        conexion.close()

    def abrir_pdf(event):
        item = tabla.selection()
        if item:
            ruta = tabla.item(item[0], "values")[2]  # Ruta PDF
            if os.path.exists(ruta):
                webbrowser.open_new(ruta)
            else:
                messagebox.showerror("Error", f"No se encontró el archivo:\n{ruta}")

    tk.Label(ventana, text="ID Estudiante:").pack()
    entrada_id = tk.Entry(ventana)
    entrada_id.pack()

    tk.Button(ventana, text="Generar PDF", command=generar_pdf).pack(pady=10)

    tabla = ttk.Treeview(ventana, columns=("ID Reporte", "Fecha", "Ruta PDF"), show="headings")
    for col in ("ID Reporte", "Fecha", "Ruta PDF"):
        tabla.heading(col, text=col)
        tabla.column(col, width=180)
    tabla.pack(pady=10)
    tabla.bind("<Double-1>", abrir_pdf)

    tk.Button(ventana, text="Regresar al Menú Principal", command=ventana.destroy).pack(pady=10)

    actualizar_tabla()
