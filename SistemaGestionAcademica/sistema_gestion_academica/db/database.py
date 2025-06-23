#db/database.py
import sqlite3
import os

def crear_bd():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "academico.db")
    os.makedirs(base_dir, exist_ok=True)

    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Estudiante (
        id_estudiante INTEGER PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        grado TEXT,
        seccion TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Nota (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL,
        id_estudiante INTEGER,
        FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Asistencia (
        id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        presente BOOLEAN,
        id_estudiante INTEGER,
        FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante) ON DELETE CASCADE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reporte (
        id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        ruta_pdf TEXT
    )''')

    conexion.commit()
    conexion.close()
