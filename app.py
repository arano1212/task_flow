from flask import Flask, render_template, request, redirect, url_for
from src.database import DBManager
from src.modelos import Tarea

app = Flask(__name__)
db = DBManager()

@app.route("/")
def index():
    tareas = db.obtener_tareas()
    return render_template("index.html", tasks=tareas)

@app.route("/create", methods=["POST"])
def create_task():
    titulo = request.form.get("title")
    descripcion = request.form.get("description")
    prioridad = request.form.get("priority", "Media")
    estado = request.form.get("status", "Pendiente")
    fecha_limite = request.form.get("fecha_limite", "Sin fecha")

    nueva_tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        prioridad=prioridad,
        estado=estado,
        fecha_limite=fecha_limite,
        proyecto_id=0
    )
    
    db.crear_tarea(nueva_tarea)
    return redirect(url_for("index"))

@app.route("/move/<int:task_id>/<string:new_status>", methods=["POST"])
def move_task(task_id, new_status):
    db.actualizar_estado(task_id, new_status)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    db.eliminar_tarea(task_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)