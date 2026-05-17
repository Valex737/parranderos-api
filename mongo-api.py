from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = "mongodb://ISIS2304J17202610:hgOTjLcY6HmB@157.253.236.88:8087"
client = MongoClient(MONGO_URI)
db = client["ISIS2304J17202610"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ------ COMENTARIOS ------

@app.get("/bares/{bar_id}/comentarios")
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}))
    return [fix_id(c) for c in comentarios]

@app.post("/bares/{bar_id}/comentarios")
def post_comentario(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["date"] = datetime.utcnow()
    result = db["comentarios_bares"].insert_one(datos)
    return {"inserted_id": str(result.inserted_id)}

# ------ EVENTOS ------

@app.get("/bares/{bar_id}/eventos")
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find({"bar_id": bar_id}))
    return [fix_id(e) for e in eventos]

@app.post("/bares/{bar_id}/eventos")
def post_evento(bar_id: int, datos: dict):
    datos["bar_id"] = bar_id
    datos["fecha_creacion"] = datetime.utcnow()
    result = db["eventos"].insert_one(datos)
    return {"inserted_id": str(result.inserted_id)}