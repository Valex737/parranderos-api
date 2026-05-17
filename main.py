from datetime import datetime
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
app = FastAPI()

# Configuración de CORS para permitir peticiones desde cualquier cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# Configuración de Base de Datos
# ==========================================

# NOTA: Para despliegue, utilice la variable de entorno MONGO_URI:
# client = MongoClient(os.environ["MONGO_URI"])

# TODO: Conectarse al cluster Admonsis para desarrollo local
# client = MongoClient("mongodb://<usuario>:<contraseña>@157.253.236.88:8087")
client = MongoClient("mongodb://ISIS2304J17202610:hgOTjLcY6HmB@157.253.236.88:8087")

# TODO: Especificar el nombre de la base de datos asignada
# db = client["ISIS*******"]
db = client["ISIS2304J17202610"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def inicio():
    """Endpoint de verificación de estado."""
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    """Retorna la lista de comentarios asociados a un bar."""
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}))
    return [fix_id(c) for c in comentarios]

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    """Crea un nuevo comentario para un bar específico."""
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    """Retorna todos los eventos asociados a un bar."""
    eventos = list(db["eventos"].find({"bar_id": bar_id}))
    return [fix_id(e) for e in eventos]

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    """Crea un nuevo evento para un bar específico."""
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento guardado'}
