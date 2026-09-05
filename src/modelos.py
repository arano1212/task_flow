from datetime import datetime

class Proyecto:
    def __init__(self, nombre: str, descripcion: str = "", id: int = None, estado: str = ""):
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self._estado = estado 

    @property
    def id(self): return self._id
    @id.setter
    def id(self, valor): self._id = valor
    @property
    def nombre(self): return self._nombre
    @property
    def descripcion(self): return self._descripcion
    @property
    def estado(self): return self._estado

class Tarea:
    def __init__(self, titulo: str, fecha_limite: str, prioridad: str,
                proyecto_id: int, descripcion: str, id: int = None, estado: str = "Pendiente", fecha_creacion: str = None):
        self._id = id
        self._titulo = titulo
        self._descripcion = descripcion
        self._fecha_limite = fecha_limite
        self._fecha_creacion = fecha_creacion if fecha_creacion else datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        self._prioridad = prioridad
        self._estado = estado
        self._proyecto_id = proyecto_id

    
    @property
    def id(self): return self._id
    
    @id.setter
    def id(self, valor): self._id = valor

    @property
    def titulo(self): return self._titulo

    @property
    def descripcion(self): return self._descripcion

    @property
    def prioridad(self): return self._prioridad

    @property
    def estado(self): return self._estado
    
    @property
    def fecha_limite(self): return self._fecha_limite
    
    @property
    def fecha_creacion(self): return self._fecha_creacion
    
    @property
    def proyecto_id(self): return self._proyecto_id

    def marcar_como_completada(self):
        if self._estado != "Completada":
            self._estado = "Completada"
            return True
        return False    