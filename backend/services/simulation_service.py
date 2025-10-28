import math
import json
from datetime import datetime, timedelta
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../../data/ephemerides.json")

def simulate_orbit(days=10):
    """
    Simula una órbita circular simple y guarda los datos en JSON.
    days: cantidad de días a proyectar
    """
    orbit_data = []
    start_date = datetime.utcnow()
    
    for day in range(days):
        date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
        for degree in range(0, 360, 10):
            radians = math.radians(degree)
            x = round(math.cos(radians), 4)
            y = round(math.sin(radians), 4)
            orbit_data.append({"date": date, "angle": degree, "x": x, "y": y})
    
    # Guardar en JSON
    with open(DATA_FILE, "w") as f:
        json.dump(orbit_data, f, indent=4)
    
    return orbit_data
