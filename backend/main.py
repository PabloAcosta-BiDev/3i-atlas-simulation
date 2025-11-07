from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, json

app = FastAPI(title="3I-ATLAS Ephemeris API", version="1.0")

# Configurar CORS (orígenes configurables vía variables de entorno)
# FRONTEND_ORIGIN: (por ejemplo) https://<your-org>.github.io
# RENDER_URL: la URL pública de Render: https://<your-render-service>.onrender.com
frontend_origin = os.getenv("FRONTEND_ORIGIN")
render_url = os.getenv("RENDER_URL")

allowed_origins = ["http://localhost:8080", "http://127.0.0.1:8080"]
if frontend_origin:
    allowed_origins.append(frontend_origin)
if render_url:
    allowed_origins.append(render_url)

# Deduplicar manteniendo orden
seen = set()
allowed = []
for o in allowed_origins:
    if o and o not in seen:
        seen.add(o)
        allowed.append(o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS allowed_origins:", allowed)

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


@app.get("/api/planets")
def get_planets():
    """Get heliocentric positions for all planets.
    Returns a dict with all planet positions from pre-generated JSON files.
    """
    result = {
        "bodies": {},
        "times": None
    }
    
    # Read all planet JSONs from data/planets/
    for name in ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]:
        try:
            data = load_json(os.path.join("planets", f"{name}.json"))
            if result["times"] is None:
                result["times"] = data["times"]
            result["bodies"][name] = data["positions"]
        except Exception as e:
            print(f"Error loading {name}.json: {e}")
            continue
    
    return JSONResponse(content=result)


@app.get("/api/planets/{name}")
def get_planet_file(name: str):
    # serve cached/generated planet JSON under data/planets/{name}.json
    fn = os.path.join("planets", f"{name.lower()}.json")
    return load_json(fn)

@app.get("/api/status")
def get_status():
    files = os.listdir(DATA_DIR)
    latest = max([os.path.getmtime(os.path.join(DATA_DIR, f)) for f in files])
    from datetime import datetime
    return {"last_update": datetime.fromtimestamp(latest).isoformat()}
