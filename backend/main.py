from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json

app = FastAPI(title="3I-ATLAS Ephemeris API", version="1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todas las cabeceras
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{filename} not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "3I/ATLAS API is running."}

@app.get("/api/vectors")
def get_vectors():
    return load_json("ephem_vectors_fetched.json")

@app.get("/api/deltas/{location}")
def get_deltas(location: str):
    fn = f"ephem_delta_{location.lower()}.json"
    return load_json(fn)

@app.get("/api/orbits")
def get_orbits():
    return load_json("elemental_orbits.json")

@app.get("/api/status")
def get_status():
    files = os.listdir(DATA_DIR)
    latest = max([os.path.getmtime(os.path.join(DATA_DIR, f)) for f in files])
    from datetime import datetime
    return {"last_update": datetime.fromtimestamp(latest).isoformat()}
