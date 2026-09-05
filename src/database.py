import sqlite3
from .modelos import Tarea, Proyecto
import os

DATABASE_NAME = 'tareas.db'

def get_conection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla():
    conn = get_conection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            estado TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEXT,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
        )
    """)

    try:
        cursor.execute(
            "INSERT INTO proyectos(id, nombre, descripcion, estado) VALUES (0, 'Tareas generales', 'tareas sin clasificar', 'Activo')"
        )
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()


class DBManager:
    def __init__(self):
        crear_tabla()

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_conection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tareas(titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, 
            (tarea.titulo, tarea.descripcion, tarea.fecha_creacion, tarea.fecha_limite, tarea.prioridad, tarea.estado, tarea.proyecto_id)
        )
        
        conn.commit()
        tarea.id = cursor.lastrowid
        conn.close()
        return tarea
    
    def obtener_proyectos(self):
        conn = get_conection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyectos")
        filas = cursor.fetchall()
        conn.close()

        return [Proyecto(nombre=fila['nombre'], descripcion=fila['descripcion'], id=fila['id'], estado=fila['estado']) for fila in filas]

    def obtener_tareas(self, estado=None):
        conn = get_conection()
        cursor = conn.cursor()

        sql = "SELECT * FROM tareas "
        params = []

        if estado:
            sql += "WHERE estado = ? "
            params.append(estado)

        sql += "ORDER BY id DESC"

        cursor.execute(sql, params)
        filas = cursor.fetchall()
        conn.close()

        tareas = []
        for fila in filas:
            t = Tarea(
                titulo=fila['titulo'],
                fecha_limite=fila['fecha_limite'],
                prioridad=fila['prioridad'],
                proyecto_id=fila['proyecto_id'],
                descripcion=fila['descripcion'],
                id=fila['id'],
                estado=fila['estado'],
                fecha_creacion=fila['fecha_creacion']
            )
            tareas.append(t)
        return tareas

    def actualizar_estado(self, tarea_id: int, nuevo_estado: str):
        conn = get_conection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", (nuevo_estado, tarea_id))
        conn.commit()
        conn.close()

    def eliminar_tarea(self, tarea_id: int):
        conn = get_conection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        conn.commit()
        conn.close()